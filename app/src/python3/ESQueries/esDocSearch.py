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
		"3: Search query using only logical AND",
		"4: Search query using only logical OR",
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
		elif i == "3":
			response = searchQueryUsingLogicalAND()
		elif i == "4":
			response = "Not yet implemented"
		else:
			break
		print(response)
	return ("#" * 15) + " Search is Over!!! " + ("#" * 15) + "\n\n"


def searchESAPIWithJSONBody(jsonBody):
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_search", json=jsonBody).json()


def searchADocumentUsingDocumentId():
	documentId = input("Enter the document id or press enter for random existing : ")
	if documentId == "":
		documentId = getRandomDocumentId()
		print("documentId : " + documentId)
	return requests.get(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_doc/" + documentId).json()


def searchADocumentUsingKeyWord():
	keyWord = input("Enter a key word or press enter for random existing : ")
	if keyWord == "":
		keyWord = random.choice(random.choice(recordsUtils.getKeyWordList()))
		print("keyWord : " + keyWord)
	searchQueryBody = {"size": MAX_NUMBER_OF_RECORDS, "query": getFilterOptionQuery(keyWord)}
	return searchESAPIWithJSONBody(searchQueryBody)


def searchQueryUsingLogicalAND():
	filterQuery = getFilterQuery()
	searchQueryBody = {"query": {"bool": {"filter": filterQuery}}}
	return searchESAPIWithJSONBody(searchQueryBody)


def getRandomDocumentId():
	return random.choice(recordsUtils.getRecords())["id"]


def getFilterQuery():
	filterQuery = []
	print("Search based on logical AND")
	print("Enter keyWords to search and then press enter to search")
	print("Press enter for random existing (3 keyWords chosen randomly)")
	while True:
		keyword = input("Enter keyWord " + str(len(filterQuery) + 1) + " : ")
		if keyword == "":
			break
		filterQuery += [getFilterOptionQuery(keyword)]
	if len(filterQuery) == 0:
		keyWordList = recordsUtils.getKeyWordList()
		filterQuery += [getFilterOptionQuery(random.choice(keyWordList[0]))]
		filterQuery += [getFilterOptionQuery(random.choice(random.choice(keyWordList[1:4])))]
		filterQuery += [getFilterOptionQuery(random.choice(keyWordList[4]))]
	return filterQuery


def getFilterOptionQuery(keyword):
	return {"simple_query_string": {"query": keyword}}
