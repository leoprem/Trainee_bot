# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet,  AllSlotsReset

import pandas as pd
import openpyxl
class ActionHelloWorld(FormAction):

    def name(self) -> Text:
        return "status_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("Fetching slots")
    
        return ["emp_id", "course_name", "status"]

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        filePath = "./api.csv"
        print("Got all the slots inserting into db")
        emp_id = tracker.get_slot("emp_id")
        course_name= tracker.get_slot("course_name")
        status= tracker.get_slot("status")

        df1 = pd.read_csv(filePath)

        df2 = pd.DataFrame({"emp_id":[int(emp_id)],"course":[course_name],"status":[status]})
        if df1.empty:
            df1 = df2
        else:
            flag = False
            for _, row in df1.iterrows():
                if row["emp_id"] == int(emp_id) and row["course"].lower() == course_name.lower():
                    df1.loc[(df1["emp_id"]==int(emp_id)) & (df1["course"]==course_name),"status"] = status
                    flag = True
            if flag == False:
                df1 = df1.append(df2,ignore_index=True)

        #print(df2)

        df1.to_csv(filePath)

        dispatcher.utter_message(template="utter_slot_values")

        return [AllSlotsReset()]

class ActionReturnStatus(FormAction):

    def name(self) -> Text:
        return "get_status"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
    
        return ["emp_id"]

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        print("Checking status")
        filePath = "./api.csv"

        emp_id = tracker.get_slot("emp_id")

        df1 = pd.read_csv(filePath)
        msg = ""
        flag = False
        for _, row in df1.iterrows():
            #print(row)
            if str(row["emp_id"]) == str(emp_id):
                if flag == False:
                    msg+= "<em>These are the courses done by "+emp_id+":</em><br>"
                msg += "<strong>Course</strong>: {}  <strong>Status</strong>: {}<br>".format(row['course'],row['status'])
                flag = True

        if flag == False:
            msg = str(emp_id)+" has not logged any course status"
        dispatcher.utter_message(text=msg)

        return [AllSlotsReset()]
