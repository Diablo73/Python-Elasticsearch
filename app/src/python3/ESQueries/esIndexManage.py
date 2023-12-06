import os
import json
import requests
import prettytable


def printOptions():
	table = prettytable.PrettyTable(["Option", "Event"])
	options = [
		[1, "Add Index"],
		[2, "Get Index Size"],
		[3, "Delete Index"],
		[0, "Quit"]
	]
	table.add_rows(options)
	print(table)

def manageIndex():
	while True:
		printOptions()
		i = input("Select an option: ")
		if i == "1":
			response = putNewIndexInES()
		elif i == "2":
			response = getIndexSizeInES()
		elif i == "3":
			response = deleteIndexInES()
		else:
			break
		print(response)

def putNewIndexInES():
	return requests.put(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX")).json()

def getIndexSizeInES():
	# can also get in csv format or in mb or gb and use wildcard in index name
	# if index names were student_2023-12-06, student_2023-12-07, etc
	# /_cat/indices?h=index,store.size&bytes=mb&format=csv&s=index&index=student_2023-*
	return [{"unit" : "kb"}] + requests.get(os.getenv("ES_URL")
	                                        + "/_cat/indices?h=index,store.size&bytes=kb&format=json&s=index&index="
	                                        + os.getenv("ES_INDEX")).json()


def createNewIndexPatternInES():
	return requests.post(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/index_patterns/index_pattern",
	                     json={ "index_pattern": { "title": os.getenv("ES_INDEX") } }).json()


def deleteIndexInES():
	return requests.delete(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX")).json()
