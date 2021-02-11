import json
from Item import Item
from Region import Region
from Location import Location
from Entrance import Entrance
from ItemDictionary import itemDictionary
from TabDictionary import tabDictionary
from EntranceDictionary import entrancesDictionary

class SpoilerData:
    def __init__(self,filename):
        # Load the JSON file
        self.filename = filename
        with open(self.filename) as f:
            self.rawData = json.load(f)

        # Extract data from settings
        self.locationData = self.rawData['locations']
        self.wothData = self.rawData[':woth_locations']
        self.settings = self.rawData['settings']
        self.entranceData = self.rawData['entrances']
        self.dungeonMQData = self.rawData['dungeons']
        self.version = self.rawData[':version']
        self.hash = self.rawData['file_hash']
        self.settingsString = self.rawData[':settings_string']

        # Check for sanities
        self.isTriforceHunt = self.settings['triforce_hunt']
        self.isSkullsanity = not self.settings['tokensanity'] == 'off'
        self.isEntranceRandomzier = bool(self.entranceData)
        self.isShopsanity = not self.settings['shopsanity'] == 'off'
        self.isMQDungeons = 'mq' in self.dungeonMQData.values()


        self.regions = dict()
        self.locations = dict()
        self.items = dict()
        self.entrances = dict()
        self.tabs = dict()
        self.shops = dict()
        self.mqDungeons = dict()
        self.dungeonItems = {
            'Deku Tree': [],
            'Dodongos Cavern': [],
            'Jabu Jabus Belly': [],
            'Forest Temple': [],
            'Fire Temple': [],
            'Water Temple': [],
            'Shadow Temple': [],
            'Spirit Temple': [],
            'Ice Cavern': [],
            'Bottom of the Well': [],
            'Gerudo Fortress': [],
            'Gerudo Training Grounds': [],
            'Ganons Castle': []
        }

        self.initializeItems()
        self.initializeRegions()
        self.initializeLocations()
        self.initializeTabs()
        if self.isEntranceRandomzier:
            self.initializeEntrances()
            self.organizeEntrancesIntoRegions()
        if self.isShopsanity:
            self.findShops()

        self.organizeLocationsIntoTabs()
        self.findDungeonItems()
        if self.isMQDungeons:
            pass

    def initializeItems(self):
        for item in itemDictionary:
            self.items[item] = Item(item,itemDictionary[item])

    def initializeLocations(self):
        locations = self.locationData
        for location in locations:
            item = locations[location]
            locationObj = Location(location)
            self.locations[location] = locationObj
            if isinstance(item,dict):
                itemName = item['item']
            else:
                itemName = item

            # if itemName in self.items:
            itemObj = self.items[itemName]
            locationObj.addItem(item,itemObj)
            # else:
            #     locationObj.addItem(item)
            #     itemObj = locationObj.item
            #     self.items[itemName] = itemObj
            #     if itemName in itemDictionary:
            #         itemObj.image = itemDictionary[itemName]
            if location in self.wothData:
                locationObj.isWOTH = True
            for region in self.regions.values():
                for search in region.search:
                    if search in location:
                        region.locations.append(locationObj)
                        locationObj.region = region
                        locationObj.isDungeon = region.isDungeon
                        break


    def initializeRegions(self):
        for region in entrancesDictionary:
            regionObj = Region(region,entrancesDictionary[region])
            self.regions[region] = regionObj
            if regionObj.isDungeon:
                for dungeon in self.dungeonMQData:
                    for search in regionObj.search:
                        if search in dungeon:
                            if self.dungeonMQData[dungeon] == 'mq':
                                regionObj.isMQ = True
                            break

    def initializeEntrances(self):
        for entrance in self.entranceData:
            location = self.entranceData[entrance]
            self.entrances[entrance] = Entrance(entrance,location)

    def initializeTabs(self):
        for tab in tabDictionary:
            self.tabs[tab] = dict()
            for item in itemDictionary:
                if item in tabDictionary[tab]['items']:
                    self.tabs[tab][item] = []

    def organizeLocationsIntoTabs(self):
        for location in self.locations.values():
            item = location.item
            for tab in self.tabs:
                if item.name in self.tabs[tab]:
                    self.tabs[tab][item.name].append(location)
                    item.tab = tab

    def organizeEntrancesIntoRegions(self):
        for entrance in self.entrances.values():
            entranceFrom = entrance.entranceFrom.split()
            if len(entranceFrom) > 1:
                entranceFrom = ' '.join(entranceFrom[:2])
            else:
                entranceFrom = entranceFrom[0]

            leadsToRegion = entrance.leadsToRegion.split()
            if len(leadsToRegion) > 1:
                leadsToRegion = ' '.join(leadsToRegion[:2])
            else:
                leadsToRegion = leadsToRegion[0]
            for region in self.regions:
                regionObj = self.regions[region]
                for search in regionObj.search:
                    found = False
                    if search == 'Market':
                        if search in entranceFrom and entranceFrom != 'Market Entrance' and entranceFrom != 'Market Guard House':
                            regionObj.exits.append(entrance)
                            found = True
                        if search in leadsToRegion and leadsToRegion != 'Market Entrance' and leadsToRegion != 'Market Guard House':
                            regionObj.entrances.append(entrance)
                            found = True
                    elif search == 'Ganons Castle':
                        continue
                    elif search == 'OGC':
                        if search in entrance.entranceTo:
                            regionObj.exits.append(entrance)
                            found = True
                    else:
                        if search in entranceFrom:
                            regionObj.exits.append(entrance)
                            found = True
                        if search in leadsToRegion:
                            regionObj.entrances.append(entrance)
                            entrance.isDungeon = regionObj.isDungeon
                            found = True
                    if found:
                        break

    def findDungeonItems(self):
        dungeonItemList = self.tabs['Dungeon Items']
        for locationList in dungeonItemList.values():
            for location in locationList:
                for dungeon in self.dungeonItems:
                    if dungeon in location.item.name:
                        self.dungeonItems[dungeon].append(location)

    def findShops(self):
        shopAssoc = {'KF Shop': 'Kokiri Shop',
                     'Market Bazaar': 'Child Bazaar',
                     'Market Potion Shop': 'Child Potion Shop',
                     'Market Bombchu Shop': 'Bombchu Shop',
                     'Kak Bazaar': 'Adult Bazaar',
                     'Kak Potion Shop': 'Adult Potion Shop',
                     'GC Shop': 'Goron City',
                     'ZD Shop': 'Zora Domain'}
        for shop in shopAssoc:
            self.shops[shopAssoc[shop]] = []

        for location in self.locations.values():
            if "Shop" in location.name or "Bazaar" in location.name:
                for shop in shopAssoc:
                    if shop in location.name:
                        self.shops[shopAssoc[shop]].append(location)






if __name__ == '__main__':
    # test = SpoilerData('StandardSeed.json')
    test = SpoilerData('/spoilerLogs/FullEntranceChusInLogic.json')