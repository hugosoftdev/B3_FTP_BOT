from S3Wrapper import S3Wrapper
from FTPManager import FTPManager
import os
import shutil


class B3Bot:
        def __init__(self):
                self.AlreadyDownloaded = []
                self.s3 = S3Wrapper()
                self.ftp = FTPManager('ftp.bmf.com.br')
                self.CleanTempFolder()

        def GetExistingFiles(self):
                fileNames = self.s3.ListBucketFiles('pfedell')
                self.AlreadyDownloaded =  fileNames

        def CleanTempFolder(self):
                absolutePath = os.path.abspath(".")
                path = absolutePath + "/temp"
                for root, dirs, files in os.walk(path):
                        for f in files:
                                os.unlink(os.path.join(root, f))
                        for d in dirs:
                                shutil.rmtree(os.path.join(root, d))

        def Run(self):
                self.GetExistingFiles()
                self.ftp.Login()
                self.ftp.SetFolderPath('marketdata/Bovespa-Vista')

                #paralelizar esse pedaço aqui
                for item in self.ftp.ListFolderFiles():
                        if item not in self.AlreadyDownloaded:
                                print("Downloading {0}...".format(item))
                                downloadedFileName = self.ftp.DownloadFile(item)
                                print("Uploading {0}...".format(item))
                                self.s3.UploadFile(downloadedFileName, 'pfedell', item)
                                self.AlreadyDownloaded.append(item)
                self.CleanTempFolder()


bot = B3Bot()
bot.Run()
