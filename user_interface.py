import multiprocessing
from time import sleep

import PySimpleGUI as sg
import os.path

import schedule
from multiprocessing import Process, Queue
from folder_copy import syncNow

def syncServer(q):
    q = q
    sync_state = True
    print("sync activated")
    schedule.every(5).seconds.do(printTime, q=q) #Needs callable arg
    while sync_state:
        schedule.run_pending()

def printTime(q):
    print(q)

#On doit avoir une fonction main à cause du Threading qui fait qu'on peut pas call soi-même
def main(q):
    folder_list = []
    selected_folder = ""
    sync_thread = None


    file_list_column = [
        [
            sg.Text("Dossier à synchroniser"),
            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), #Input avec les events enabled et la key pour s'y référer par la suite
            sg.FolderBrowse(button_text="Naviguer"), #Bouton de browsing
            sg.Button("Ajouter", key="-ADD FOLDER-")
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(63,20), key="-FOLDER LIST-"  #Pas encore de valeurs présentes
            )
        ],
    ]

    button_column = [
        [sg.Push(), sg.Button("Arrêter la synchronisation", key="-STOP SYNC-"), sg.Push()],
        [sg.Push(), sg.Button("Synchroniser maintenant", key="-SYNC NOW-"), sg.Push()],
        [sg.Push(), sg.Button("Enlever ce dossier", key="-REMOVE FOLDER-"), sg.Push()],
    ]

    log_column = [
        [sg.Text("Statut")],
        [sg.Output(size=(63,20))],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeparator(), #Séparer les deux colonnes
            sg.Column(button_column),
            sg.VSeparator(), #Séparer les deux colonnes
            sg.Column(log_column),
        ]
    ]

    window = sg.Window("ElieDrive", layout, icon="eliedrive_icon.ico")

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            if (isinstance(sync_thread, Process)):
                sync_thread.terminate()
            break
        if event == "-ADD FOLDER-":
            #Si on a un nouveau folder, on veut l'ajouter à la liste de folders présente
            #et display à nouveau celle-ci updated.
            folder = os.path.abspath(values["-FOLDER-"])
            #On s'assure que le folder n'est pas déjà dans notre liste et qu'il est bien
            #un dossier.
            if folder not in folder_list and os.path.isdir(folder):
                folder_list.append(folder)
            window["-FOLDER LIST-"].update(folder_list)
        elif event == "-FOLDER LIST-":
            try:
                selected_folder = values["-FOLDER LIST-"][0]
            except:
                pass
        elif event == "-STOP SYNC-":
            print("Stop Sync!")
            sync_state = False
            #sg.popup("Hello!")
            #sg.popup_ok("OK?")
            #sg.popup_menu("MENU")
        elif event == "-SYNC NOW-":
            print("Sync now!")
            q = folder_list
            sync_thread = Process(target=syncServer, args=(q,)) #If you use start fct on the same statement, sync_thread won't be instance of Process. Why?
            sync_thread.start()
        elif event == "-REMOVE FOLDER-":
            print("Remove folder " + selected_folder)
            try:
                folder_list.remove(selected_folder)
                window["-FOLDER LIST-"].update(folder_list)
            except:
                pass
        else:
            pass
    window.close()

if __name__ == '__main__':
    q = Queue()
    q.put(None)
    main_thread = Process(target=main, args=(q,))
    main_thread.start()
    print(isinstance(main_thread, Process))
