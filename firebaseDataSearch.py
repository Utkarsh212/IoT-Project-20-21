# import firebase_admin
# from firebase_admin import  credentials
from firebase_admin import db
from datetime import date
import time

def firebaseData_Search(id):
    t = time.localtime()
    CURRENT_TIME = time.strftime("%H:%M:%S", t)
    TODAY = date.today().strftime("%d/%m/%Y")

    # cred = credentials.Certificate("scanner-database-firebase-adminsdk-npg5h-956503dab3.json")
    # firebase_admin.initialize_app(cred, {
    #     'databaseURL':'https://scanner-database-default-rtdb.firebaseio.com/'
    # })

    ID = id.upper()
    ref = db.reference("/")
    students = ref.get()
    for key, value in students.items():
        if(key == ID):
            NAME = value["Name"]
            STATUS = "Out" if value["Status"] == "In" else "In"
            ref.child(key).update({"Status": STATUS})
            break
                

    # Dictonary of log containing values to be pushed into record.
    try:
        curr_log = {'Date': TODAY, 'Time': CURRENT_TIME, 'ID': ID, 'Name': NAME, 'Status': STATUS}
    except:
        return -1
    return curr_log