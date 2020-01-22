#
# @author  RocketML
#
import boto3

# Document
s3BucketName = "rmlcontent"
#documentURI = "https://rmlcontent.s3-us-west-2.amazonaws.com/credit_card_03.png"
documentName = "images.jpg"

# Amazon Textract client
textract = boto3.client('textract',region_name='us-west-2')

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

# Print detected text
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[94m' +  item["Text"] + '\033[0m')
