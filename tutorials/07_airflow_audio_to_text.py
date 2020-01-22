"""
RocketML: Single audio to text pipeline
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import json
from pydub import AudioSegment
from timeit import default_timer as timer
from deepspeech import Model, printVersions
import wave
import numpy as np

import sys
try:
    from shhlex import quote
except ImportError:
    from pipes import quote

default_args = {
    'owner': 'RocketML',
    'depends_on_past': False,
    'start_date': datetime(2019, 11, 6),
    'email': ['santi@rocketml.net'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

## Initializing DAG
dag = DAG(
    'tutorial_audio_to_metadata', default_args=default_args, schedule_interval=timedelta(days=1))

## Setting parameters
s3_key = "s3://rmlprojectsbucket/santirocketml/airflow_tutorial0vp7k/example.wav"
local_folder = "/home/ubuntu/airflow/dags/"
s3_folder = "s3://rmlprojectsbucket/santirocketml/airflow_tutorial0vp7k/"

local_filename = local_folder + s3_key.split("/")[-1]
local_metadata = local_filename + ".meta.json"
local_text_file     = local_filename + ".txt.json"

## Creating a task using BashOperator to copy audio file to local directory
t1 = BashOperator(
    task_id='copy_s3file_to_local',
    bash_command='aws s3 cp  ' + s3_key + ' ' + local_folder,
    dag=dag)

## Creating a Python function to get meta data from audio file and dump it in a file
def get_audio_properties(**kwargs):
    filename = kwargs["filename"]
    outputfile = kwargs["output_file"]
    sound = AudioSegment.from_wav(filename)
    
    properties = {}
    properties["loudness"]          = sound.dBFS
    properties["channels"]          = sound.channels
    properties["bytes_per_sample"]  = sound.sample_width
    properties["frames_per_second"] = sound.frame_rate
    properties["bytes_per_frame"]   = sound.frame_width
    properties["peak_amplitude"]    = sound.max
    properties["duration"]          = str(timedelta(milliseconds=len(sound)))

    with open(outputfile,"w") as outfile:
        json.dump(properties,outfile)

    return properties

## Creating a task using Python Operator to extract metadata from audio file
t2 = PythonOperator(
    task_id='get_audio_metadata',
    python_callable=get_audio_properties,
    op_kwargs={
        "filename" : local_filename,
        "output_file" : local_metadata
    },
    dag=dag)


## Creating functions to extract audio to text
def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)

def audio_to_text(**kwargs):
    filename = kwargs["filename"]
    outputfile = kwargs["output_file"]
    
    model_load_start = timer()
    BEAM_WIDTH = 500

    # The alpha hyperparameter of the CTC decoder. Language Model weight
    LM_ALPHA = 0.75

    # The beta hyperparameter of the CTC decoder. Word insertion bonus.
    LM_BETA = 1.85

    # These constants are tied to the shape of the graph used (changing them changes
    # the geometry of the first layer), so make sure you use the same constants that
    # were used during training

    # Number of MFCC features to use
    N_FEATURES = 26

    # Size of the context window used for producing timesteps in the input vector
    N_CONTEXT = 9
    
    # Model Files
    model_file = "/home/ubuntu/deepspeech-0.5.1-models/output_graph.pb"
    alphabet_file = "/home/ubuntu/deepspeech-0.5.1-models/alphabet.txt"
    lm_file = "/home/ubuntu/deepspeech-0.5.1-models/lm.binary"
    trie_file = "/home/ubuntu/deepspeech-0.5.1-models/trie"
    
    ds = Model(model_file, N_FEATURES, N_CONTEXT, alphabet_file, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)


    lm_load_start = timer()
    ds.enableDecoderWithLM(alphabet_file,lm_file,trie_file, LM_ALPHA, LM_BETA)
    lm_load_end = timer() - lm_load_start

    fin = wave.open(filename, 'rb')
    fs = fin.getframerate()
    if fs != 16000:
        print('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs), file=sys.stderr)
        fs, audio = convert_samplerate(filename)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/16000)
    fin.close()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()
    output_text = ds.stt(audio, fs)
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
    
    output = {}
    output["text"] = output_text

    with open(outputfile,"w") as outfile:
        json.dump(output,outfile)
    
    return output_text

## Create a task using PythonOperator to covert audio to text
t3 = PythonOperator(
    task_id='get_audio_text',
    python_callable=audio_to_text,
    op_kwargs={
        "filename" : local_filename,
        "output_file" : local_text_file
    },
    dag=dag)


## Creating a task using BashOperator to copy audio file to local directory
t4 = BashOperator(
    task_id='copy_local_meta_to_s3',
    bash_command='aws s3 cp  ' + local_metadata + ' ' + s3_folder,
    dag=dag)

t5 = BashOperator(
    task_id='copy_local_text_file_to_s3',
    bash_command='aws s3 cp  ' + local_text_file + ' ' + s3_folder,
    dag=dag)

## Create dependency 
t2.set_upstream(t1)
t3.set_upstream(t1)

t4.set_upstream(t2)
t5.set_upstream(t3)
