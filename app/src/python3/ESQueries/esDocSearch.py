import os
import json
import random
import requests
from Utils import recordsUtils


MAX_NUMBER_OF_RECORDS = len(recordsUtils.getRecords())


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
		keyWord = random.choice(recordsUtils.getKeyWordList())
		print("keyWord : " + keyWord)
	searchQueryBody = {"size": MAX_NUMBER_OF_RECORDS, "query": {"simple_query_string": {"query": keyWord}}}
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_search", json=searchQueryBody).json()


def getRandomDocumentId():
	return random.choice(recordsUtils.getRecords())["id"]
