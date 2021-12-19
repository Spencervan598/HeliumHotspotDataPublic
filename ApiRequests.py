import requests
import json
from time import sleep

class APIRequests:
    def __init__(self, Address):
        self.UrlDict = {'base':'https://api.helium.io/v1/', 'hotspot':'https://api.helium.io/v1/hotspots/', 'activity':'https://api.helium.io/v1/hotspots/~/activity?'}
        self.Address = Address
        # self.Stats = requests.get("https://api.helium.io/v1/stats")
        self.status = None
    
    def GetHotspotInfo(self, dictUrl = 'base', params = None , event = None):        
        h1 = requests.get(f"{self.UrlDict[dictUrl]}{self.Address}", params = params)
        if h1.status_code == 429:
            sleep(int(h1.headers['retry-after'])+1)
            self.GetHotspotInfo()
        self.rJson1 = json.loads(h1.content)['data'] if json.loads(h1.content)['data'] else {'data':{'timestamp_added': 0}}
        return self.rJson1
        
    def GetHotspotActivity(self, cursor = None, filters = None, event = None):
        if not cursor:
            h2 = requests.get(f"{self.UrlDict['hotspot']}{self.Address}/activity?", filters)
            cursor = json.loads(h2.content)['cursor']
        h2 = requests.get(f"{self.UrlDict['hotspot']}{self.Address}/activity?{cursor}")
        self.rJson2 = json.loads(h2.content)
        return self.rJson2
    def GetHotspotLocation(self, distance = "15000", event = None):
        h3 = requests.get(f"{self.UrlDict['hotspot']}location/distance?lat={self.rJson1['lat']}&lon={self.rJson1['lon']}&distance={distance}")


if __name__ == "__main__":
    apiObject = APIRequests(input("Hotspot Address"))
