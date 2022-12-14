import socket, tqdm, os, zipfile, datetime, traceback, sys, os.path, PySimpleGUI as sg, schedule
from multiprocessing import Process, Queue

def syncServer(q):
    sync_state = True
    print("sync activated")
    sync(q)
    schedule.every(10).seconds.do(sync, q=q) #Needs callable function name, no ()
    while sync_state:
        schedule.run_pending()

def sync(q):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 #Send 4096 bytes each time

    try:

        folder_list = []

        while not q.empty():
            folder_list.append(q.get())

        updateQueue(q, folder_list)

        print(folder_list)

        if folder_list:

            host = socket.gethostname()

            port = 1234

            s = socket.socket()

            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")


            ct = datetime.datetime.now()
            formatted_ct = ct.strftime("%Y-%m-%d %H-%M-%S.%f")
            archive_filename = f"archive {formatted_ct}.zip"

            with zipfile.ZipFile(archive_filename, 'w') as f:
                for folder in folder_list:
                    for folderName, subfolders, filenames in os.walk(folder):
                        for filename in filenames:
                            filePath = os.path.join(folderName, filename)
                            f.write(filePath)
            filesize = os.path.getsize(archive_filename)
            s.send(f"{archive_filename}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(range(filesize), f"Sending {archive_filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(archive_filename, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in
                    # busy networks
                    s.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
            # close the socket
            s.close()

            os.remove(archive_filename)
    except:
        traceback.print_exc()
        sys.exit(1)

def updateQueue(q, folder_list):
    while not q.empty():
        q.get()
    for folder in folder_list:
        q.put(folder)

#On doit avoir une fonction main ?? cause du Threading qui fait qu'on peut pas call soi-m??me
def main(q):
    folder_list = []
    selected_folder = ""
    sync_thread = None


    file_list_column = [
        [
            sg.Text("Dossier ?? synchroniser"),
            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), #Input avec les events enabled et la key pour s'y r??f??rer par la suite
            sg.FolderBrowse(button_text="Naviguer"), #Bouton de browsing
            sg.Button("Ajouter", key="-ADD FOLDER-")
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(63,20), key="-FOLDER LIST-"  #Pas encore de valeurs pr??sentes
            )
        ],
    ]

    button_column = [
        [sg.Push(), sg.Button("Arr??ter la synchronisation", key="-STOP SYNC-"), sg.Push()],
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
            sg.VSeparator(), #S??parer les deux colonnes
            sg.Column(button_column),
            sg.VSeparator(), #S??parer les deux colonnes
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
            #Si on a un nouveau folder, on veut l'ajouter ?? la liste de folders pr??sente
            #et display ?? nouveau celle-ci updated.
            folder = os.path.abspath(values["-FOLDER-"])
            #On s'assure que le folder n'est pas d??j?? dans notre liste et qu'il est bien
            #un dossier.
            if folder not in folder_list and os.path.isdir(folder):
                folder_list.append(folder)
            window["-FOLDER LIST-"].update(folder_list)
            updateQueue(q, folder_list)
        elif event == "-FOLDER LIST-":
            try:
                selected_folder = values["-FOLDER LIST-"][0]
            except:
                pass
        elif event == "-STOP SYNC-":
            print("Arr??t de la synchronisation p??riodique.")
            if (isinstance(sync_thread, Process)):
                sync_thread.terminate()
            #sg.popup("Hello!")
            #sg.popup_ok("OK?")
            #sg.popup_menu("MENU")
        elif event == "-SYNC NOW-":
            print("D??but de la synchronisation p??riodique.")
            updateQueue(q, folder_list)
            if (isinstance(sync_thread, Process)):
                sync_thread.terminate()
            sync_thread = Process(target=syncServer, args=(q,)) #If you use start fct on the same statement, sync_thread won't be instance of Process. Why?
            sync_thread.start()
        elif event == "-REMOVE FOLDER-":
            try:
                folder_list.remove(selected_folder)
                window["-FOLDER LIST-"].update(folder_list)
                updateQueue(q, folder_list)
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
