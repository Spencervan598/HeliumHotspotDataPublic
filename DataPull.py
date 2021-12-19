import ApiRequests
import csv
from datetime import datetime, timedelta
from pathlib import Path


def AddDays(date):
    mintime=datetime.strptime(date[0:10], "%Y-%m-%d")
    return mintime + timedelta(1)


def addresses(addressfield = 'Address', retfields = False):
    with open(file := Path(input("Input csv file path. Either absolute or relative to script execution.")).resolve(), 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        # if retfields is True:
        #     return reader.fieldnames 
        # if addressfield not in reader.fieldnames:
        #     return f"File does not contain a field called {addressfield}. Pass fieldname as addressfield param or input correct csv file."
        

        # This return statement may work, have not tested need to test this tmrw. 12/17
        return [x for x in reader.fieldnames] if retfields is True else f"File does not contain a field called {addressfield}. Pass fieldname as addressfield param or input correct csv file." if addressfield not in reader.fieldnames else [x[addressfield] for x in reader]
        
        
def atb(request):
        # request = ApiRequests.APIRequests(address)
        print(request.GetHotspotInfo(), "\n")
        if not (atb := request.GetHotspotInfo()['timestamp_added']):
            return("Request for hotspot info failed.")
        return atb[0:10] if not atb else 0
        

def firstreward(request):
    request.GetHotspotActivity()
    if not (rew := request.GetHotspotActivity()):
        pass
    

def firstdatatransfer(request):
    request.GetHotspotActivity()

def firstpoc(request):
    request.GetHotspotActivity()


def allassert(request):
    request.GetHotspotActivity()


def main():
    fieldnamelist = addresses()
    
    with open('Hotspot.csv', 'a', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnamelist)
        writer.writeheader()

        for i in addresses('Hotspot Name'):
            if not i:
                continue
            request = ApiRequests.APIRequests(i)
            # need to slow this down possibly restricted to 1 request a second maybe 100 a minute then 1 per however long
            # csvwritedict = dict(zip(fieldnamelist,[i, atb(request), firstreward(request), firstdatatransfer(request), firstpoc(request), allassert(request)]))
            csvwritedict = dict(zip(fieldnamelist,[i, atb(request)]))
            writer.writerow(csvwritedict)

if __name__ == '__main__':
    # main()
    print(addresses('Hotspot Name', True))