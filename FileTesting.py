import os
from pathlib import Path

"""
with open('testfile.txt', 'r') as f:  # On ouvre le fichier en mode Read-Only et on lit ce qui s'y trouve.
    data = f.read()
    print(data)

with open('testwrite.txt', 'w') as f:  # Même chose mais pour écrire dans le fichier
    f.write("wow nice text bro")

print(os.listdir("bidonDir"))

with os.scandir("bidonDir") as entries:  # Scandir retourne un itérateur qui pointe à toutes les entrées du Directory
    for entry in entries:  # Le statement with est utilisé pour fermer automatiquement l'itérateur et ressources après
        # la fin de la boucle
        print(entry.name)

entries = pathlib.Path("bidonDir")  # À regarder toutes les fonctions disponibles dans pathlib car il semble être le
# plus efficace
# Il existe aussi shutil que je pourrais utiliser (https://docs.python.org/3/library/shutil.html)
for entry in entries.iterdir():
    print(entry.name)

basepath = "bidonDir/"
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)
"""
# https://docs.python.org/3/library/pathlib.html
basedir = Path("./bidonDir")
print([x for x in basedir.iterdir() if x.is_dir()])
# Si on assume que la variable basedir comprend le nom du dossier auquel on veut synchroniser son arbre descendant.
# Il faudra donc faire une vérification périodique de son arbre descendant et vérifier chaque fichier pour voir s'il
# a été modifié depuis pour garder seulement la version la plus récente. Il ne sera aussi pas nécessaire de faire
# une sauvegarde au Cloud si aucun changement n'a été apporté.
# On fera aussi la vérification pour s'assurer que le ou les Paths mentionnés à synchroniser sont absolus
