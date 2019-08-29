import os
import logging
import boto3
from botocore.exceptions import ClientError


class S3Wrapper:
        def __init__(self):
            #CONFERIR SE O AWS CLI ESTA CONFIGURADO NA MAQUINA
            self.client = boto3.client('s3')

        def UploadBinary(self, binaryData, bucketName, objectName=None):
            try:
              self.client.put_object(Body=binaryData, Bucket=bucketName,
                                Key=objectName)
            except ClientError as e:
              logging.error(e)
              return False
            return True

        def ListBucketFiles(self, bucketName):
          bucketFileNames = []
          try:
            for key in self.client.list_objects(Bucket=bucketName)['Contents']:
              bucketFileNames.append(key['Key'])
          except KeyError:
            bucketFileNames = []
          return bucketFileNames
