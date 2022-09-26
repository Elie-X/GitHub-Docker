# folder_copy.py
from shutil  import copytree
import datetime

#def syncNow
#S'assurer qu'on reçoit une Liste de strings suivi d'un destination path


#https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
ct = datetime.datetime.now()
formatted_ct = ct.strftime("%Y-%m-%d %H-%M-%S.%f")
base = "C:\\Users\\Elie\\Documents\\Projet\\GitHub-Docker\\copyTestBaseFolder"
destination = f"C:\\Users\\Elie\\Documents\\Projet\\GitHub-Docker\\copyTestDestinationFolder\\copyTestBaseFolder-{formatted_ct}"
print(destination)

try :
    copytree(base, destination) #shutil needs a path that doesn't already exist
except Exception as e:
    print(e)
    pass
