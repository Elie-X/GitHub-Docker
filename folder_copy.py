# folder_copy.py

from shutil  import copytree

base = "C:\\Users\\Elie\\Documents\\Projet\\GitHub-Docker\\copyTestBaseFolder"
destination = "C:\\Users\\Elie\\Documents\\Projet\\GitHub-Docker\\copyTestDestinationFolder\\copyTestBaseFolder"
print(destination)

try :
    copytree(base, destination) #shutil needs a path that doesn't already exist
except:
    pass
