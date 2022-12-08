from ESQueries import esBulkDelete


def printStart():
	print()
	print(("#" * 15) + " Python-Elasticsearch " + ("#" * 15))
	print(("#" * 15) + (" " * 6) + " START!!! " + (" " * 6) + ("#" * 15))
	print()


def printEnd():
	print()
	print(("#" * 15) + " Python-Elasticsearch " + ("#" * 15))
	print(("#" * 15) + (" " * 6) + " END!!!!! " + (" " * 6) + ("#" * 15))
	print()


def printOptions():
	options = [
		"",
		"1: Bulk-Delete and Bulk-Upload",
		"2: Bulk-Delete only",
		"3: Bulk-Upload only",
		"4: Search",
		"0: Quit",
		""
	]
	for i in options:
		print(i)


def process():
	while True:
		printOptions()
		i = input("Select an option: ")
		if i == "1":
			response = "Not yet implemented"
		elif i == "2":
			response = esBulkDelete.bulkDelete()
		elif i == "3":
			response = "Not yet implemented"
		elif i == "4":
			response = "Not yet implemented"
		else:
			break
		print(response)


if __name__ == '__main__':
	printStart()
	process()
	printEnd()
