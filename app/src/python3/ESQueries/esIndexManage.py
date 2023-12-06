import os
import json
import requests
import prettytable


def printOptions():
	table = prettytable.PrettyTable(["Option", "Event"])
	options = [
		[1, "Add Index"],
		[2, "Delete Index"],
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
			response = deleteIndexInES()
		else:
			break
		print(response)

def putNewIndexInES():
	return requests.put(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX")).json()

def createNewIndexPatternInES():
	return requests.post(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/index_patterns/index_pattern",
	                     json={ "index_pattern": { "title": os.getenv("ES_INDEX") } }).json()


def deleteIndexInES():
	return requests.delete(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX")).json()


deleteQueryBody = '{"query":{"match_all":{}}}'
response = requests.post(os.getenv("ES_URL") + "/" + os.getenv("ES_INDEX") + "/_delete_by_query",
                         json=json.loads(deleteQueryBody)).json()
