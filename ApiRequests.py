import requests
import json
class APIRequests:
    def __init__(self, Address):
        self.UrlDict = {'base':'https://api.helium.io/v1/', 'hotspot':'https://api.helium.io/v1/hotspots/'}
        self.Address = Address
        # self.Stats = requests.get("https://api.helium.io/v1/stats")
        self.status = None
    
    def GetHotspotInfo(self, event = None):
        h1 = requests.get(f"{self.UrlDict['hotspot']}{self.Address}")
        self.rJson1 = json.loads(h1.content)['data']
        
    def GetHotspotActivity(self, event = None):
        h2 = requests.get(f"{self.UrlDict['hotspot']}{self.Address}/activity")
        h2 = requests.get(f"{self.UrlDict['hotspot']}{self.Address}/activity?cursor={json.loads(h2.content)['cursor']}")
        self.rJson2 = json.loads(h2.content)
    def GetHotspotLocation(self, distance = "15000", event = None):
        h3 = requests.get(f"{self.UrlDict['hotspot']}location/distance?lat={self.rJson1['lat']}&lon={self.rJson1['lon']}&distance={distance}")
if __name__ == "__main__":
    DGB = APIRequests()
    DGB.GetHotspotActivity()
    print(DGB.activityList)
