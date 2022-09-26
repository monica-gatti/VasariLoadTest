from locust import HttpUser, task, between
import json
import uuid
from Sites import json_sites
from Collections import json_collections
from Objects import json_objects_collection
from Visitors import json_visitors
import random

class QuickstartUser(HttpUser):
    wait_time = between(0.2, 0.3)
    def on_start(self):
        for site in json_sites:
            self.client.post("/interactiongraph/culturalsites/", json={"ID":site["ID"], "Name":site["Name"]})
        for collection in json_collections:
            siteID = collection["SiteID"]
            collectionID = collection["ID"]
            if (collection["Type"] == "physic"):
                self.client.post("/interactiongraph/culturalcollections/", json={"ID":collection["ID"], "Name":collection["Name"], "Type":collection["Type"], "Location":collection["Location"]})
            else:
                self.client.post("/interactiongraph/culturalcollections/", json={"ID":collection["ID"], "Name":collection["Name"], "Type":collection["Type"], "Category":collection["Category"]})
            self.client.post(f"/interactiongraph/culturalsites/{siteID}/addcollection", json={"culturalcollectionid":collection["ID"], "dateFrom":"2020-12-01T00:00:00.000Z", "dateTo":"2021-01-31T23:59:59.999Z"})
 
        objects_list = []
        for object in json_objects_collection:
            objectID = object["ID"]
            collectionID = object["collectionID"]
            objects_list.append(objectID)
            self.client.post("/interactiongraph/culturalobjects/", json={"ID":objectID, "Name":object["Name"], "Room":object["Room"]})
            self.client.post(f"/interactiongraph/culturalcollections/{collectionID}/addculturalobject", json={"culturalobjectid":objectID, "dateFrom":"2020-12-01T00:00:00.000Z", "dateTo":"2021-01-31T23:59:59.999Z"})     
        visitor_list = []
        for visitor in json_visitors:
            visitorID = visitor["ID"]
            visitor_list.append(visitorID)
            self.client.post("/interactiongraph/visitors/", json={"ID":visitorID})
        for i in range(0,500):
            visitor_i = random.choice(visitor_list)
            object_i = random.choice(objects_list)
            self.client.post(f"/interactiongraph/visitors/{visitor_i}/interactedVRAR", json={"culturalobjectid":object_i,"visitDatetime":"2020-12-10T00:00:00.000Z", "value":"123456"})     
        
    @task
    def index_page(self):
        objects_list = []
        for object in json_objects_collection:
            objects_list.append(object["ID"])
        #self.client.get("/interactiongraph/culturalsites/")
        #self.client.get("/interactiongraph/culturalcollections/")
        #self.client.get("/interactiongraph/culturalobjects")
        #self.client.get("/visits/metrics/visitorsnumbers", datefrom="2020-11-01T00:00:00.000Z", dateto="2020-12-31T00:00:00.000Z", culturalobjectid="SR71A-0000001")
        #for j in range(0,10):
        for object_j in objects_list:
            #object_j = random.choice(objects_list)
            self.client.get(f"/interactiongraph/visits/metrics/visitorsnumber?datefrom=2020-11-01T00%3A00%3A00.000Z&dateto=2020-12-31T00%3A00%3A00.000Z&culturalobjectid={object_j}")
            self.client.get(f"/interactiongraph/visits/metrics/cumulativevisitorsnumberday?datefrom=2020-12-10T00%3A00%3A00.000Z&dateto=2020-12-10T02%3A00%3A00.000Z&culturalobjectid={object_j}")
            self.client.get(f"/interactiongraph/visits/metrics/cumulativevisitorsnumberyear?datefrom=2020-12-01T00%3A00%3A00.000Z&dateto=2020-12-02T00%3A00%3A00.000Z&culturalobjectid={object_j}")
    #@task(3)
    #def view_item(self):
    #    for item_id in range(10):
    #        self.client.get(f"/interactiongraph/culturalsites/{item_id}", name="/culturalsites")