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


def threadingTesting():
	try:
		testSize = int(input("Input Test Size : "))
		numberOfThreads = int(input("Input number of Threads : "))
		documentIdsList = random.sample(recordsUtils.getDocumentIds(), testSize)
		return singleThreading(documentIdsList) + "\n" + multiThreading(documentIdsList, numberOfThreads)
	except Exception as e:
		return str(e)


def singleThreading(documentIdsList):
	startTime = time.time()
	foundCount = threadRunProcess(documentIdsList, 0)
	duration = time.time() - startTime
	return str({"testName": "Single Threading", "success count": foundCount, "time taken": duration})


def multiThreading(documentIdsList, numberOfThreads):
	threadList = []
	foundCount = 0
	partition = (len(documentIdsList) // numberOfThreads) + 1
	for i in range(numberOfThreads):
		start = i * partition
		end = start + partition
		if end >= len(documentIdsList):
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
		if foundCount % (len(documentIdsList) // 10) == 0:
			print(foundCount)
	return foundCount


def getESDocument(documentId):
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()
