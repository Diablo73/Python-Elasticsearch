import os
import json
import requests

filePaths = ["app/src/resources/students_30k_bulkES.txt", "../../resources/students_30k_bulkES.txt"]

def bulkUpload():
	records = ""
	for path in filePaths:
		try:
			studentDataTxtFile = open(path, "r")
			records = studentDataTxtFile.read()
			print("Data found in file : " + path)
			studentDataTxtFile.close()
			break
		except Exception as e:
			print(str(e))

	try:
		records += "\n"
		response = requests.post(os.getenv("ES_URL") + "/_bulk", data=records,
		                         headers={"content-type": "application/json", "charset": "UTF-8"}).json()
		return "Upload query execution : Success!!! ✅\n" + str(response)
	except Exception as e:
		return "Upload query execution : Fail!!! ❌\n" + str(e)
