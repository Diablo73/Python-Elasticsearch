import os
import time
import json
import random
import requests
if "linux" in os.sys.platform:
	from Utils import recordsUtils
else:
	from app.src.python3.Utils import recordsUtils


TEST_SIZE = 1000


def threadingTesting():
	return singleThreading() + "\n"


def singleThreading():
	documentIdsList = random.sample(recordsUtils.getDocumentIds(), TEST_SIZE)
	startTime = time.time()
	foundCount = 0
	for documentId in documentIdsList:
		response = getESDocument(documentId)
		if response["found"]:
			foundCount += 1
		if foundCount % (TEST_SIZE // 100) == 0:
			print(foundCount)
	duration = time.time() - startTime
	return str({"testName": "Single Threading", "success count": foundCount, "time taken": duration})


def getESDocument(documentId):
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()
