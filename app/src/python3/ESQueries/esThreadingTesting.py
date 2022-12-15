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
	successList = threadRunProcess(documentIdsList, [])
	duration = time.time() - startTime
	return str({"testName": "Single Threading", "success count": len(successList), "time taken": duration})


def multiThreading(documentIdsList, numberOfThreads):
	threadList = []
	successList = []
	partition = (len(documentIdsList) // numberOfThreads) + 1
	for i in range(numberOfThreads):
		start = i * partition
		end = start + partition
		if end >= len(documentIdsList):
			end = len(documentIdsList)
		threadList += [threading.Thread(target=threadRunProcess, args=(documentIdsList[start:end], successList))]

	startTime = time.time()
	for thread in threadList:
		thread.start()

	for thread in threadList:
		thread.join()
	duration = time.time() - startTime
	return str({"testName": "Multi Threading", "success count": len(successList), "time taken": duration})


def threadRunProcess(documentIdsList, successList):
	for i in range(len(documentIdsList)):
		response = getESDocument(documentIdsList[i])
		if response["found"]:
			successList += [documentIdsList[i]]
		if (i + 1) % (len(documentIdsList) // 100) == 0:
			print(str(i + 1) + " / " + str(len(documentIdsList)) + " - "
			      + str(((i + 1) * 100) / len(documentIdsList)) + "%")
	return successList


def getESDocument(documentId):
	try:
		return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()
	except Exception as e:
		print("Exception for docId : " + documentId + " : " + str(e))
		return {"found": False}
