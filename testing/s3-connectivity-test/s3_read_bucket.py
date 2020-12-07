from s3_utils import get_matching_s3_keys

bucket = "rmlcontent"
prefix = ""
suffix = ""
file_list = []
for key in get_matching_s3_keys(bucket=bucket,prefix=prefix,suffix=suffix):
    file_list.append("s3://"+bucket+"/"+key)
print(file_list)

