import ApiRequests
import csv
from datetime import datetime, timedelta
from pathlib import Path


def AddDays(date):
    mintime=datetime.strptime(date[0:10], "%Y-%m-%d")
    return mintime + timedelta(1)


def addresses(addressfield = 'Address'):
    with open(file := Path(input("Input csv file path. Either absolute or relative to script execution.")).resolve(), 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        if addressfield not in reader.fieldnames:
            return f"File does not contain a field called {addressfield}. Pass fieldname as addressfield param or input correct csv file."
        return [x[addressfield] for x in reader]
        
        
def atb(address):
        writedict = {}
        request = ApiRequests.APIRequests(address)
        if not(atb:= request.GetHotspotInfo()['timestamp_added']):
            return("Request for hotspot info failed.")
        return atb[0:10] if atb else 0
        

def firstreward():
    pass


def firstdatatransfer():
    pass


def firstpoc():
    pass


def allassert():
    pass


def main():
    fieldnamelist = ['Address', 'Added to Blockchain', 'First Reward Date', 'First Data Transfer Date', 'First PoC Date', 'All Location Asserts']
    
    with open('Hotspot.csv', 'a', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnamelist)
        writer.writeheader()

        for i in addresses():
            csvwritedict = zip(fieldnamelist,[i, atb(), firstreward(), firstdatatransfer(), firstpoc(), allassert()])

            writer.writerow(csvwritedict)

if __name__ == '__main__':
    main()