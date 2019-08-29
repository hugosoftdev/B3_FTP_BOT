import ftplib
import os
from io import BytesIO
from helper import randomString

class FTPManager:
  def __init__(self, host,username=None,password=None):
    self.host = host
    self.username = username
    self.password =  password
    self.connection = ftplib.FTP(host)
    self.folderPath = None
    self.isLogged = False

  def Login(self):
    if(self.username != None and self.password != None):
      self.connection.login(self.username, self.password)
    else:
      self.connection.login()
    self.isLogged = True

  def IsLoggedIn(self):
    return self.isLogged

  def VerifyLogin(self):
    if(not self.IsLoggedIn()):
        raise Exception("You must be logged in first")

  def SetFolderPath(self,path):
    self.VerifyLogin()
    self.folderPath = path
    self.connection.cwd(path)


  def ListFolderFiles(self):
    if(self.folderPath != None):
      fileNames = []
      self.connection.dir(fileNames.append)
      fileNames = [x.split(" ")[-1] for x in fileNames]
      return fileNames
    else:
       raise Exception("You must set the folder directory first")

  def DownloadFile(self, fileName):
    myfile = BytesIO()
    self.connection.retrbinary('RETR ' + fileName, myfile.write)
    myfile.seek(0)
    return myfile
    
