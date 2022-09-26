from locust import HttpUser, task, between
import json
import uuid
from Sites import json_sites
from Collections import json_collections
from Objects import json_objects_collection
from Visitors import json_visitors
import random

class FeedGraph(HttpUser):
    wait_time = between(0.2, 0.3)
    def on_start(self):
        for site in json_sites:
            self.client.post("/interactiongraph/culturalsites/", json={"ID":site["ID"], "Name":site["Name"]}, name="/culturalsites")
        for collection in json_collections:
            siteID = collection["SiteID"]
            collectionID = collection["ID"]
            if (collection["Type"] == "physic"):
                self.client.post("/interactiongraph/culturalcollections/", json={"ID":collection["ID"], "Name":collection["Name"], "Type":collection["Type"], "Location":collection["Location"]}, name="/culturalcollections")
            else:
                self.client.post("/interactiongraph/culturalcollections/", json={"ID":collection["ID"], "Name":collection["Name"], "Type":collection["Type"], "Category":collection["Category"]}, name="/culturalcollections")
            self.client.post(f"/interactiongraph/culturalsites/{siteID}/addcollection", json={"culturalcollectionid":collection["ID"], "dateFrom":"2020-12-01T00:00:00.000Z", "dateTo":"2021-01-31T23:59:59.999Z"}, name="/addcollection")
 
        objects_list = []
        for object in json_objects_collection:
            objectID = object["ID"]
            collectionID = object["collectionID"]
            objects_list.append(objectID)
            self.client.post("/interactiongraph/culturalobjects/", json={"ID":objectID, "Name":object["Name"], "Room":object["Room"]},name="/culturalojects")
            self.client.post(f"/interactiongraph/culturalcollections/{collectionID}/addculturalobject", json={"culturalobjectid":objectID, "dateFrom":"2020-12-01T00:00:00.000Z", "dateTo":"2021-01-31T23:59:59.999Z"}, name="/addculturalobject")     
        