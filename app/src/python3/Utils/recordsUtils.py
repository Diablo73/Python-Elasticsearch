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
	genderWords = set()
	companyWords = set()
	stateWords = set()
	countryWords = set()
	credit_card_typeWords = set()
	for i in records:
		genderWords.add(i["gender"])
		companyWords.add(i["company"])
		stateWords.add(i["state"])
		countryWords.add(i["country"])
		credit_card_typeWords.add(i["credit_card_type"])
	return [list(genderWords), list(companyWords), list(stateWords), list(countryWords), list(credit_card_typeWords)]
