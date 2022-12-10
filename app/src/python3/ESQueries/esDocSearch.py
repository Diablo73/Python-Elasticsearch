import os
import json
import random
import requests


recordsFilePaths = ["app/src/resources/students_30k.json", "../resources/students_30k.json",
                    "../../resources/students_30k.json"]


def printOptions():
	options = [
		"",
		"1: Search a document using documentId",
		"2: Search a document using a keyWord",
		"0: Quit",
		""
	]
	for i in options:
		print(i)


def searchES():
	while True:
		printOptions()
		i = input("Select an option: ")
		if i == "1":
			response = searchADocumentUsingDocumentId()
		elif i == "2":
			response = searchADocumentUsingKeyWord()
		else:
			break
		print(response)
	return ("#" * 15) + " Search is Over!!! " + ("#" * 15) + "\n\n"


def searchADocumentUsingDocumentId():
	documentId = input("Enter the document id or press enter for random existing : ")
	if documentId == "":
		documentId = getRandomDocumentId()
		print("documentId : " + documentId)
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()


def searchADocumentUsingKeyWord():
	keyWord = input("Enter a key word or press enter for random existing : ")
	if keyWord == "":
		keyWord = random.choice(getKeyWordList())
		print("keyWord : " + keyWord)
	searchQueryBody = {"query": {"simple_query_string": {"query": keyWord}}}
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_search", json=searchQueryBody).json()


def getKeyWordList():
	records = getRecords()
	keyWords = set()
	for i in records:
		keyWords.add(i["gender"])
		keyWords.add(i["company"])
		keyWords.add(i["state"])
		keyWords.add(i["country"])
		keyWords.add(i["credit_card_type"])
	return list(keyWords)


def getRandomDocumentId():
	return random.choice(getRecords())["id"]


def getRecords():
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
	return records
