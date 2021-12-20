import ApiRequests
import csv
from datetime import datetime, timedelta
from pathlib import Path

class Pulling:
    rewcount = 0
    file = Path(input("Input csv file path. Either absolute or relative to script execution: ")).resolve()

    def AddDays(self, date, days=1):
        mintime=datetime.strptime(date[0:10], "%Y-%m-%d")
        return (mintime + timedelta(days)).isoformat()[0:10]


    def addresses(self, addressfield = 'Address', retfields = False):
        with open(self.file, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            return [x for x in reader.fieldnames] if retfields is True else f"File does not contain a field called {addressfield}. Pass fieldname as addressfield param or input correct csv file." if addressfield not in reader.fieldnames else [x[addressfield] for x in reader]
        
        
    def atb(self, request):
        # Gets Date Added to Blockchain
        print(request.GetHotspotInfo(), "\n")
        if not (atbdata := request.GetHotspotInfo()['timestamp_added']):
            return 0
        self.atbdata = atbdata[0:10]
        return self.atbdata
        

    def firstreward(self, request):
        # Gets Date of First Reward
        params = {'min_time': self.atbdata, 'max_time': self.AddDays(self.atbdata, days=(self.rewcount + 1)), 'filter_types': ',rewards_v1,rewards_v2', 'limit': 100 }
        if self.rewcount >= 20:
            self.rewcount = 0
            print('No Reward activity within 20 days of being adding to blockchain. \n')
            return 0
        if not (rew := request.GetHotspotActivity(params=params)):
            return 0
        if type(rew) is not tuple:
            if not rew['data']:
                self.rewcount += 1
                return self.firstreward()
            return rew['data'][len(rew['data']) - 1]['time']
        if rew[1]['data']:
            rew = rew[1]
            return rew['data'][len(rew['data']) - 1]['time']
        rew = rew[0]
        return rew['data'][len(rew['data']) - 1]['time']
    

    def firstdatatransfer(self, request):
        request.GetHotspotActivity()

    def firstpoc(self, request):
        request.GetHotspotActivity()


    def allassert(self, request):
        request.GetHotspotActivity()


def main():
    pullobject = Pulling()
    fieldnamelist = pullobject.addresses(retfields=True)
    
    with open('Hotspot.csv', 'a', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnamelist)
        writer.writeheader()

        for i in pullobject.addresses('Hotspot Name'):
            if not i:
                continue
            request = ApiRequests.APIRequests(i)
            # need to slow this down possibly restricted to 1 request a second maybe 100 a minute then 1 per however long
            # csvwritedict = dict(zip(fieldnamelist,[i, atb(request), firstreward(request), firstdatatransfer(request), firstpoc(request), allassert(request)]))
            # csvwritedict = dict(zip(fieldnamelist,[i, atb(request)]))
            print(pullobject.atb(request), pullobject.firstreward(request))
            # writer.writerow(csvwritedict)

if __name__ == '__main__':
    main()
    # print(Pulling.addresses(retfields=True))