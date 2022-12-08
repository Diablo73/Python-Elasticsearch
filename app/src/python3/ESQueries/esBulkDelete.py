import os
import json
import requests


def bulkDelete():
    print("Deleting all documents from index : " + os.getenv("ES_INDEX"))
    try:
        deleteQueryBody = '{"query":{"match_all":{}}}'
        response = requests.post(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_delete_by_query",
                                 json=json.loads(deleteQueryBody)).json()
        return "Delete query execution : Success!!! ✅\n" + str(response)
    except Exception as e:
        return "Delete query execution : Fail!!! ❌\n" + str(e)
