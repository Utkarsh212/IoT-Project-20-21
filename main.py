import firebase_admin
from firebase_admin import  credentials
import PySimpleGUI as sg
import cv2
from pyzbar.pyzbar import decode
import keyboard as kb
from firebaseDataSearch import firebaseData_Search
from push_to_csv import pushToCSV
from table_example import populateTable

cred = credentials.Certificate("scanner-database-firebase-adminsdk-npg5h-956503dab3.json")
firebase_admin.initialize_app(cred, {
        'databaseURL':'https://scanner-database-default-rtdb.firebaseio.com/'
})

def main():
    sg.theme('DefaultNoMoreNagging')
    video_frame_column = [
        [sg.Text("Scanner", justification="center")],
        [sg.Image(filename="", key="-IMAGE-", expand_x=True, expand_y=True)]
    ]
    functional_column = [
        [sg.Text("Log Settings", justification="center")],
        [   
            sg.Text("Scanned ID:", justification="center"), 
            sg.Text(size=(30, 1), key="-TOUT-", justification="center", background_color="white")
        ],
        [sg.Button("Enter")],
        [sg.Button("Exit")],
        [sg.Button("Display Log")]
    ]
    layout=[
            [
                sg.Column(video_frame_column),
                sg.VSeperator(),
                sg.Column(functional_column, element_justification='c')
            ]
        ]
    window = sg.Window("Entry/Exit Log Management System", layout, location=(300, 150), resizable=True, finalize=True)
    cap = cv2.VideoCapture(0)
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        success, img = cap.read()
        imgbytes = cv2.imencode(".png", img)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)
        if event == "Enter" or kb.is_pressed("enter"):
            if decode(img) == []:
                window["-TOUT-"].update("Improper Scan!")
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                window["-TOUT-"].update(myData)
                updated_log = firebaseData_Search(myData)
                if updated_log == -1:
                    window["-TOUT-"].update("Unauthorised ID")
                else:
                    pushToCSV(updated_log)
            cv2.waitKey(1000)
        cv2.waitKey(100)
        if event == "Display Log":
            headings_list = ['Date','Time','ID','Name','Counter']
            populateTable(headings_list)
    window.close()
main()