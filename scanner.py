import firebase_admin
from firebase_admin import  credentials
import cv2
from pyzbar.pyzbar import decode
import keyboard as kb
from firebaseDataSearch import firebaseData_Search
from push_to_csv import pushToCSV

cred = credentials.Certificate("scanner-database-firebase-adminsdk-npg5h-956503dab3.json")
firebase_admin.initialize_app(cred, {
        'databaseURL':'https://scanner-database-default-rtdb.firebaseio.com/'
})

cap = cv2.VideoCapture(0)
cap.set(4,480)
while True:
    success,img = cap.read()
    cv2.imshow('Result',img)    
    if kb.is_pressed("enter"):
        if(decode(img) == []):
            print("Improper Scan")
        for barcode in decode(img):        
            myData = barcode.data.decode('utf-8')
            print("Scanned ID : ", myData)
            updated_log = firebaseData_Search(myData)
            if(updated_log == -1):
                print("Unauthorized ID")
            else:
                pushToCSV(updated_log)
        cv2.waitKey(1000)
    cv2.waitKey(100)