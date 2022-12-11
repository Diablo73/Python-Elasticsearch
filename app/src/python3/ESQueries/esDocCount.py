import os
import json
import requests


def getTotalCountOfDocsInES():
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_count").json()
