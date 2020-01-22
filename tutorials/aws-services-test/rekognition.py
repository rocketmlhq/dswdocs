# 
# Author 2019 RocketML
#
import boto3

BUCKET = "rmlcontent"
KEY = "credit_card_03.png"

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-west-2"):
	rekognition = boto3.client(service_name='rekognition', region_name='us-west-2')
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']

detect_labels(BUCKET, KEY)
