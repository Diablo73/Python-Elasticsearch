from ESQueries import esBulkDelete, esBulkUpload, esDocCount, esDocSearch, esThreadingTesting
import prettytable


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
	table = prettytable.PrettyTable(["Option", "Event"])
	options = [
		[1, "Bulk-Delete and Bulk-Upload"],
		[2, "Bulk-Delete only"],
		[3, "Bulk-Upload only"],
		[4, "Search a document"],
		[5, "Count of documents"],
		[6, "Threading Testing"],
		[9, "Clear Console"],
		[0, "Quit"],
	]
	table.add_rows(options)
	print(table)


def process():
	while True:
		printOptions()
		i = input("Select an option: ")
		if i == "1":
			response = esBulkDelete.bulkDelete() + "\n" + esBulkUpload.bulkUpload()
		elif i == "2":
			response = esBulkDelete.bulkDelete()
		elif i == "3":
			response = esBulkUpload.bulkUpload()
		elif i == "4":
			response = esDocSearch.searchES()
		elif i == "5":
			response = esDocCount.getTotalCountOfDocsInES()
		elif i == "6":
			response = esThreadingTesting.threadingTesting()
		else:
			break
		print(response)


if __name__ == '__main__':
	printStart()
	process()
	printEnd()
