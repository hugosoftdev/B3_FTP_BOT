from S3Wrapper import S3Wrapper
from FTPManager import FTPManager
import os
import json


class B3Bot:
        def __init__(self):
                self.AlreadyDownloaded = []
                self.s3 = S3Wrapper()
                self.ftp = FTPManager('ftp.bmf.com.br')

        def GetExistingFiles(self):
                fileNames = self.s3.ListBucketFiles('b3ftpraw2')
                self.AlreadyDownloaded =  fileNames

        def Run(self):
                self.GetExistingFiles()
                self.ftp.Login()
                self.ftp.SetFolderPath('marketdata/Bovespa-Vista')

                #paralelizar esse pedaço aqui
                for item in self.ftp.ListFolderFiles():
                        if item not in self.AlreadyDownloaded:
                                print("Downloading {0}...".format(item))
                                binaryData = self.ftp.DownloadFile(item)
                                print("Uploading {0}...".format(item))
                                self.s3.UploadBinary(
                                    binaryData, 'pfedell', item)
                                self.AlreadyDownloaded.append(item)


def lambda_handler(event, context):
    bot = B3Bot()
    bot.Run()
    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }


