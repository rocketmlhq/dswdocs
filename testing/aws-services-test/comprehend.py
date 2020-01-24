# 
# Author 2019 RocketML
#


import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
text = 'Accelerate your data science work with RocketML'

print('Calling DetectEntities')
print(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'),
                 sort_keys=True, indent=4))
print('End of DetectEntities\n')
