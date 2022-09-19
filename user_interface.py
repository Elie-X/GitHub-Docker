import PySimpleGUI as sg
import os.path

file_list_column = [
    [
        sg.Text("Dossier à synchroniser"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), #Input avec les events enabled et la key pour s'y référer par la suite
        sg.FolderBrowse(), #Bouton de browsing
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20), key="-FILE LIST-"  #Pas encore de valeurs présentes
        )
    ],
]

button_column = [
    sg.Button("Arrêter la synchronisation"),
    sg.Button("Synchroniser maintenant"),
    sg.Button("Enlever ce dossier")
]

