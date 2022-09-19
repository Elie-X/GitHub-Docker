# test_interface.py

import PySimpleGUI as sg
import os.path

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), #Input avec les events enabled et la key pour s'y référer par la suite
        sg.FolderBrowse(), #Bouton de browsing
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20), key="-FILE LIST-"  #Pas encore de valeurs présentes
        )
    ],
]

image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]


layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(), #Séparer les deux colonnes
        sg.Column(image_viewer_column),
    ]
]

#Pour ajouter un thème pour changer les couleurs de base
#sg.theme("Theme name")

#Pour voir le preview de tous les thèmes
#sg.theme_previewer()

#SimpleGUI window, first arg = title name, second arg = layout created
window = sg.Window("Image Viewer", layout)


while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-": #if key of the event = -FOLDER-
        folder = values["-FOLDER-"] #Retourne le path de l'input avec la key -FOLDER-
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename) #Display l'image avec le filename mentionné
        except:
            pass

window.close()