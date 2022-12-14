import os
import time
import json
import random
import requests
import threading
if "linux" in os.sys.platform:
	from Utils import recordsUtils
else:
	from app.src.python3.Utils import recordsUtils


TEST_SIZE = 1000
NUMBER_OF_THREADS = 10


def threadingTesting():
	documentIdsList = random.sample(recordsUtils.getDocumentIds(), TEST_SIZE)
	return singleThreading(documentIdsList) + "\n" + multiThreading(documentIdsList)


def singleThreading(documentIdsList):
	startTime = time.time()
	foundCount = threadRunProcess(documentIdsList, 0)
	duration = time.time() - startTime
	return str({"testName": "Single Threading", "success count": foundCount, "time taken": duration})


def multiThreading(documentIdsList):
	threadList = []
	foundCount = 0
	partition = (TEST_SIZE // NUMBER_OF_THREADS) + 1
	for i in range(NUMBER_OF_THREADS):
		start = i * partition
		end = start + partition
		if end >= TEST_SIZE:
			end = len(documentIdsList)
		threadList += [threading.Thread(target=threadRunProcess, args=(documentIdsList[start:end], foundCount))]

	startTime = time.time()
	for thread in threadList:
		thread.start()

	for thread in threadList:
		thread.join()
	duration = time.time() - startTime
	return str({"testName": "Multi Threading", "success count": foundCount, "time taken": duration})


def threadRunProcess(documentIdsList, foundCount):
	for documentId in documentIdsList:
		response = getESDocument(documentId)
		if response["found"]:
			foundCount += 1
		if foundCount % (TEST_SIZE // 100) == 0:
			print(foundCount)
	return foundCount


def getESDocument(documentId):
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()
