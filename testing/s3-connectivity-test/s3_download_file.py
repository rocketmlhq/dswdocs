import boto3
from s3_utils import get_matching_s3_keys

bucket = "rmlcontent"
prefix = ""
suffix = ""
file_list = []
for key in get_matching_s3_keys(bucket=bucket,prefix=prefix,suffix=suffix):
    file_list.append("s3://"+bucket+"/"+key)


s3 = boto3.client('s3')
s3_filename = file_list[0]
bucket_name = s3_filename.split("s3://")[1].split("/")[0]
object_name = '/'.join(s3_filename.split("s3://")[1].split("/")[1:])
local_filename = s3_filename.split("/")[-1]
print(local_filename)
s3.download_file(bucket_name,object_name,local_filename)
