# Import DictWriter class from CSV module
from csv import DictWriter
from datetime import date

TODAY = date.today().strftime("%d-%m-%Y")

def pushToCSV(new_log):
    # list of column names
    field_names = ['Date','Time','ID','Name','Status']

    # Dictionary
    dict = new_log

    # Open your CSV file in append mode
    # Create a file object for this file
    with open(TODAY + '.csv', 'a') as f_object:
            
            # Pass the file object and a list
            # of column names to DictWriter()
            # You will get a object of DictWriter
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)

            #Pass the dictionary as an argument to the Writerow()
            dictwriter_object.writerow(dict)

            #Close the file object
            f_object.close()
