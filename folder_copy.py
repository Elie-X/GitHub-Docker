# folder_copy.py
import os
from shutil  import copytree
import datetime


#S'assurer qu'on reçoit une Liste de strings suivi d'un destination path
def syncNow(str_list, path):
    #If not a list, will get an exception anyways
    for str in str_list:
        if not os.path.exists(str):
            raise ValueError("One of the paths in the sync list does not exist.")
    if not os.path.exists(path):
        raise ValueError("Destination path does not exist.")


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
