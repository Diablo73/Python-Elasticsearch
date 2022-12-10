import json


recordsFilePaths = ["app/src/resources/students_30k.json", "../resources/students_30k.json",
                    "../../resources/students_30k.json"]


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
