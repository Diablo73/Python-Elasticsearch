import os
import json
import random
import requests
import prettytable
if "linux" in os.sys.platform:
	from Utils import recordsUtils
else:
	from app.src.python3.Utils import recordsUtils


MAX_NUMBER_OF_RECORDS = len(recordsUtils.getRecords())


def printOptions():
	table = prettytable.PrettyTable(["Option", "Event"])
	options = [
		[1, "Search a document using documentId"],
		[2, "Search a document using a keyWord"],
		[3, "Search query using only logical AND"],
		[4, "Search query using only logical OR"],
		[0, "Quit"]
	]
	table.add_rows(options)
	print(table)


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
			response = searchQueryUsingLogicalOR()
		else:
			break
		print(response)
	return ("#" * 15) + " Search is Over!!! " + ("#" * 15) + "\n\n"


def searchESAPIWithJSONBody(jsonBody):
	print("JSON Body = " + str(jsonBody))
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
	searchQueryBody = {"size": MAX_NUMBER_OF_RECORDS, "query": getKeyWordQuery(keyWord)}
	return searchESAPIWithJSONBody(searchQueryBody)


def searchQueryUsingLogicalAND():
	filterQuery = getFilterQuery("AND")
	searchQueryBody = {"size": MAX_NUMBER_OF_RECORDS, "query": {"bool": {"filter": filterQuery}}}
	return searchESAPIWithJSONBody(searchQueryBody)


def searchQueryUsingLogicalOR():
	filterQuery = getFilterQuery("OR")
	searchQueryBody = {"size": MAX_NUMBER_OF_RECORDS, "query": {"bool": {"filter": filterQuery}}}
	return searchESAPIWithJSONBody(searchQueryBody)


def getRandomDocumentId():
	return random.choice(recordsUtils.getRecords())["id"]


def getFilterQuery(logic):
	filterKeyWords = []
	print("Search based on logical AND")
	print("Enter keyWords to search and then press enter to search")
	print("Press enter for random existing (3 keyWords chosen randomly)")
	while True:
		keyword = input("Enter keyWord " + str(len(filterKeyWords) + 1) + " : ")
		if keyword == "":
			break
		filterKeyWords += [keyword]
	if len(filterKeyWords) == 0:
		filterKeyWords = getFilterKeyWords(logic)
	return getFilterOptionQuery(logic, filterKeyWords)


def getKeyWordQuery(keyword):
	return {"simple_query_string": {"query": keyword}}


def getFilterOptionQuery(logic, filterKeyWords):
	filterQuery = []
	if logic == "OR":
		filterKeyWords = [" ".join(filterKeyWords)]
	for keyWord in filterKeyWords:
		filterQuery += [getKeyWordQuery(keyWord)]
	return filterQuery


def getFilterKeyWords(logic):
	filterKeyWords = []
	keyWordList = recordsUtils.getKeyWordList()
	if logic == "AND":
		filterKeyWords += [random.choice(keyWordList[0])]
		filterKeyWords += [random.choice(keyWordList[5])]
		filterKeyWords += [random.choice(random.choice(keyWordList[1:5]))]
	elif logic == "OR":
		filterKeyWords += [str(random.randint(1, MAX_NUMBER_OF_RECORDS))]
		filterKeyWords += [random.choice(random.choice(keyWordList[1:3]))]
		filterKeyWords += [random.choice(random.choice(keyWordList[3:5]))]
	return filterKeyWords
