import ftplib
import os
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
    #salvo direto no hd em um folder temporario, é menos eficiente que jogar na RAM mas permite
    #que eu faça o download de arquivos pesados e paralelize essa operação (to do). 
    absolutePath = os.path.abspath(".")
    localFileName = '{0}/temp/{1}'.format(absolutePath, fileName)
    with open(localFileName, 'wb') as f:
        self.connection.retrbinary('RETR ' + fileName, f.write)
    return localFileName
    
