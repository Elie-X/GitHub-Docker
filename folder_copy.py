# folder_copy.py

from shutil  import copytree
import datetime

#def syncNow
#S'assurer qu'on reçoit une Liste de strings suivi d'un destination path
ct = datetime.datetime.now()
print(ct)

base = "C:\\Users\\Elie\\Documents\\Projet\\GitHub-Docker\\copyTestBaseFolder"
destination = "C:\\Users\\Elie\\Documents\\Projet\\GitHub-Docker\\copyTestDestinationFolder\\copyTestBaseFolder" + "backup" + str(ct)
print(destination)

try :
    copytree(base, destination) #shutil needs a path that doesn't already exist
except:
    #print(exception)
    pass
