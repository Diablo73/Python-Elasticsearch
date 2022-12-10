import os
import json
import random
import requests


recordsFilePaths = ["app/src/resources/students_30k.json", "../resources/students_30k.json",
                    "../../resources/students_30k.json"]


def searchADocumentUsingDocumentId():
	documentId = input("Enter the document id or press enter for random existing : ")
	if documentId == "":
		documentId = getRandomDocumentId()
		print(documentId)
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()


def getRandomDocumentId():
	records = []
	for path in recordsFilePaths:
		try:
			recordsJsonFile = open(path, "r")
			records = json.loads(recordsJsonFile.read())
			print("Data found in file : " + path)
			recordsJsonFile.close()
			break
		except Exception as e:
			print(str(e))
	return random.choice(records)["id"]
