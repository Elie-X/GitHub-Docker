import PySimpleGUI as sg
import os.path

def updateFolderList():
    window["-FOLDER LIST-"].update(folder_list)

folder_list = []
selected_folder = ""

file_list_column = [
    [
        sg.Text("Dossier à synchroniser"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), #Input avec les events enabled et la key pour s'y référer par la suite
        sg.FolderBrowse(), #Bouton de browsing
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(53,20), key="-FOLDER LIST-"  #Pas encore de valeurs présentes
        )
    ],
]

button_column = [
    [sg.Button("Arrêter la synchronisation", key="-STOP SYNC-")],
    [sg.Button("Synchroniser maintenant", key="-SYNC NOW-")],
    [sg.Button("Enlever ce dossier", key="-REMOVE FOLDER-")],
]



layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(), #Séparer les deux colonnes
        sg.Column(button_column),
    ]
]

window = sg.Window("ElieDrive", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        #Si on a un nouveau folder, on veut l'ajouter à la liste de folders présente
        #et display à nouveau celle-ci updated.
        folder = values["-FOLDER-"]
        #On s'assure que le folder n'est pas déjà dans notre liste et qu'il est bien
        #un dossier.
        if folder not in folder_list and os.path.isdir(folder):
            folder_list.append(folder)
        updateFolderList()
    elif event == "-FOLDER LIST-":
        selected_folder = values["-FOLDER LIST-"][0]
    elif event == "-STOP SYNC-":
        print("Stop Sync!")
    elif event == "-SYNC NOW-":
        print("Sync now!")
    elif event == "-REMOVE FOLDER-":
        print("Remove folder " + selected_folder)
        try:
            folder_list.remove(selected_folder)
            updateFolderList()
        except:
            pass
    else:
        pass

window.close()