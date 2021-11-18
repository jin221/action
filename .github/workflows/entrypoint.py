import subprocess
import os
import shutil
import sys

CMAKELISTS_FILE_PATH = 'CMakeLists.txt' #Will change depending on structure
OUTPUT_DIR_PATH = 'outputs' #Will change depending on structure

class Submission:
    def __init__(self, _codeDir, _name):
        self.codeDir = _codeDir
        self.binaryPath = None
        self.name= _name #Should be unique to student
    
    def make_binary(self):
        #run make in the student dir
        owd = os.getcwd()
        os.chdir(self.codeDir)
        os.system('make')
        os.chdir(owd)
        self.binaryPath = os.path.join(self.codeDir, "binary")
    
    def cmake(self, cMakePath):
        #copy in cmake and and run cmake in student dir
        owd = os.getcwd()
        shutil.copyfile(cMakePath,os.path.join(self.codeDir, "CMakeLists.txt"))
        os.chdir(self.codeDir)
        os.system('cmake CMakeLists.txt')
        os.chdir(owd)

    def fuzz(self, input_dir, out_dir, timeout, mode='S'):
        #run fuzz for binary in student dir and name it using student name
        cmd = [
            'timeout', str(timeout),
            'afl-fuzz',
            '-i', input_dir,
            '-o', out_dir,
            f'-{mode}', self.name,
            self.binaryPath,
            '@@',
            '>', os.path.join(out_dir,self.name,'log.txt'),
            '&'
        ]
        os.system(' '.join(cmd))

    def collect_outputs(self, input_dir, output_dir):
        for file in os.listdir(input_dir):
            if (file != "README.txt") and (file.startswith(".") != True):
                if (file.find("orig") == -1):
                    shutil.copyfile(input_dir+"/"+file,output_dir+"/"+file+","+self.name)
                else:
                    shutil.copyfile(input_dir+"/"+file,output_dir+"/"+file)

def mountRemoteDrive(sshIdentity, serverAdress, keyLocation, dirToMount, mountPoint):
    #Code should use location of key and mount the drive
    #Should remove key once done
    return

def setupSubmissionDir(originalLoc, stagingLoc):
    #Should copy necessary student files from repo to another folder so as not to mess with student files
    return

def copyPushErrors(errorLoc, studnetRepo):
    #Should copy errors from output and put them in a folder in the students repo and the push
    return

def decryptKey(passPhrase, encryptLocation, decryptLocation):
    #Decrypts file with passPhrase
    #   encryptLocation:  encrypted file
    #   decryptLocation:  decrypted file save path
    cmd = "echo " + passPhrase + "| gpg --batch -d --yes --passphrase-fd 0 " + encryptLocation +" > "+ decryptLocation
    decrypt = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        output = decrypt.communicate()[0]
    except:
        print("Unable to Decrypt File")
    if "decryption failed" in (output.decode("utf-8")):
        print("Unable to Decrypt File, Error Out:\n"+output.decode("utf-8"))

if __name__ == "__main__":
    print(os.system("ls -a"))
    print(str(sys.argv[1]))
    #Values that need to be passed in by YAML:
    #   Encryption Key
    #   Timeout
    #   Student Name/github username

    #Example steps:
    
    #setupSubmissionDir(student/repo,staging/dir)
    #submission = new Submission(staging/dir, student name)
    #submission.cmake(/location/of/cmake)
    #submission.make_binary
    #decryptKey(pass phrase from yaml, key location, un-encrypted key location)
    #mountRemoteDrive(Identity (should come from yaml too), precipice.ecn.purdue.edu, un-encrypted key location, folder/to/mount, mount/point)
    #submission.fuzz(mount/point/inputs, mount/point, time)
    #time.sleep(time)
    #submission.collect_outputs(mount/point/outputs/, mount/point)
    #copypusherrors(staging/dir/output/errors,student/repo)
    
