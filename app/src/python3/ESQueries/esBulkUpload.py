import os
import json
import requests
import pytz
from datetime import datetime


recordsFilePaths = ["app/src/resources/students_30k_bulkES.txt", "../resources/students_30k_bulkES.txt",
                    "../../resources/students_30k_bulkES.txt"]
logsFilePaths = ["app/src/logs/esBulkUploadLogs.txt", "../logs/esBulkUploadLogs.txt",
                 "../../logs/esBulkUploadLogs.txt"]


def bulkUpload():
	records = ""
	for path in recordsFilePaths:
		try:
			recordsTxtFile = open(path, "r")
			records = recordsTxtFile.read()
			print("Data found in file : " + path)
			recordsTxtFile.close()
			break
		except Exception as e:
			print(str(e))

	try:
		records += "\n"
		response = requests.post(os.getenv("ES_URL") + "/_bulk", data=records,
		                         headers={"content-type": "application/json", "charset": "UTF-8"}).json()
		return "Upload query execution : Success!!! ✅\n" + str(writeLogs(response))
	except Exception as e:
		return "Upload query execution : Fail!!! ❌\n" + str(e)


def writeLogs(response):
	header = ("#" * 15) + "  " + str(datetime.now(pytz.timezone("Asia/Kolkata"))) + "  " + ("#" * 15) + "\n\n"
	summary = ""
	logs = ""
	createdCount = 0
	errorCount = 0
	logsTxtFile = None
	for path in logsFilePaths:
		try:
			logsTxtFile = open(path, "w")
			break
		except Exception as e:
			print(str(e))

	if not response["errors"]:
		createdCount = len(response["items"])
		summary = json.dumps({"createdCount": createdCount, "errorCount": errorCount})
	else:
		for doc in response["items"]:
			if doc["create"]["status"] == 201:
				createdCount += 1
			else:
				errorCount += 1
				logs += json.dumps(doc["create"]) + "\n"
		summary = json.dumps({"createdCount": createdCount, "errorCount": errorCount}) + "\n\n"
	logs = header + summary + logs
	logsTxtFile.write(logs)
	logsTxtFile.close()
	return summary
