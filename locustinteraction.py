from locust import HttpUser, task, between
import json
import uuid
from Sites import json_sites
from Collections import json_collections
from Objects import json_objects_collection
from Visitors import json_visitors
import random
from datetime import datetime, timedelta
import logging

class interaction(HttpUser):
    logging.basicConfig(filename='loadtest.log', level=logging.INFO)
    logging.info('Locust Started')
    wait_time = between(0.2, 0.3)
 
    @task
    def interactionARVR(self):
        objects_list = []
        for object in json_objects_collection:
            objects_list.append(object["ID"])
        visitor_list = []
        for visitor in json_visitors:
            visitor_list.append(visitor["ID"])
        for i in range(0,100):
            visitor_i = random.choice(visitor_list)
            object_i = random.choice(objects_list)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            self.client.post("/interactiongraph/visitors/", json={"ID":visitor_i}, name="/visitors")
            self.client.post(f"/interactiongraph/visitors/{visitor_i}/interactedVRAR", json={"culturalobjectid":object_i,"visitDatetime":dt_string, "value":"123456"}, name="/interactedVRAR")     
    @task
    def interactionProximity(self):
        objects_list = []
        for object in json_objects_collection:
            objects_list.append(object["ID"])
        visitor_list = []
        for visitor in json_visitors:
            visitor_list.append(visitor["ID"])
        for i in range(0,100):
            visitor_i = random.choice(visitor_list)
            object_i = random.choice(objects_list)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            self.client.post("/interactiongraph/visitors/", json={"ID":visitor_i}, name="/visitors")
            self.client.post(f"/interactiongraph/visitors/{visitor_i}/visitedinproximity", json={"culturalobjectid":object_i,"visitDatetime":dt_string, "precision":0.1}, name="/visitedinproximity")     
    @task
    def interactionOnline(self):
        objects_list = []
        for object in json_objects_collection:
            objects_list.append(object["ID"])
        visitor_list = []
        for visitor in json_visitors:
            visitor_list.append(visitor["ID"])
        for i in range(0,100):
            visitor_i = random.choice(visitor_list)
            object_i = random.choice(objects_list)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            self.client.post("/interactiongraph/visitors/", json={"ID":visitor_i}, name="/visitors")
            self.client.post(f"/interactiongraph/visitors/{visitor_i}/visitedonline", json={"culturalobjectid":object_i,"visitDatetime":dt_string, "strength":"2"}, name="/visitedonline")     


    @task
    def metrics(self):
        logging.basicConfig(filename='loadtest.log', level=logging.INFO)
        logging.info('Locust Started')
        now = datetime.now()
        dtUp = datetime.now()
        minutes = 25
        minutes_added = timedelta(minutes = minutes)
        dtBottom = now - minutes_added
        dtUp_string = dtUp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        dtBottom_string = dtBottom.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        objects_list = []
        for object in json_objects_collection:
            objects_list.append(object["ID"])
        for j in range(0,10):
            object_j = random.choice(objects_list)
            resp = self.client.get(f"/interactiongraph/visits/metrics/visitorsnumber?datefrom={dtUp_string}&dateto={dtBottom_string}&culturalobjectid={object_j}", name="/visitorsnumber")
            #logging.info(str(resp.content))
            self.client.get(f"/interactiongraph/visits/metrics/cumulativevisitorsnumberday?datefrom={dtUp_string}&dateto={dtBottom_string}&culturalobjectid={object_j}", name="/cumulativevisitorsnumberday")
            #logging.info(str(resp.content))
            self.client.get(f"/interactiongraph/visits/metrics/cumulativevisitorsnumberyear?datefrom={dtUp_string}&dateto={dtBottom_string}&culturalobjectid={object_j}", name="/cumulativevisitorsnumberyear")
            #logging.info(str(resp.content))
            