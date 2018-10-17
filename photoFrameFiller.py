# File copy tool designed to fill a photo frame's SD card or any other similar 
# application where you need to copy random files up to a certain size
# from a source directory to a destination directory
# Tested with Python 3 on Linux and OSX
# GITHub Page with further info at https://github.com/therealrobster/randomFileCopyTool


import os
import csv
import random
from shutil import copyfile

def loadFileNames(fileTypeToSearchFor, pathToSearch):
	
	global fileCount
	global fileList
	global fileSizeTotalOriginal


	if os.path.exists(pathToSearch):

		#reset file count
		fileCount = 0

		fileExtensionUpper = fileTypeToSearchFor.upper()
		fileExtensionLower = fileTypeToSearchFor.lower()

		print("searching path for matching files... please be patient")

		#add filenames to the list
		for root, dirs, files in os.walk(pathToSearch):
			for file in files:
				if file.endswith(fileTypeToSearchFor) or file.endswith(fileExtensionUpper) or file.endswith(fileExtensionLower):

					#add to list (depreciated soon)
					fileList.append(file)

					#count our files, why not
					fileCount += 1

					#get filesize
					fileNameToGetInfo = root+"/"+file
					statinfo = os.stat(fileNameToGetInfo)
					fileSize = statinfo.st_size

					#increment the count for a bit of info to show user
					fileSizeTotalOriginal += fileSize 

					#write CSV file
					out = csv.writer(open("fileList.csv","a"), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					data = [fileNameToGetInfo, str(fileSize)]
					out.writerow(data)
	else:
		print("========================")
		print("That path does not exist")
		print("========================")
		print("exiting... please run again with the correct path")
		exit()


def showFiles(fileList):
	for found in fileList:
		print("Found : ",str(found))



def deleteCSVFile():
	#remove the CSV file each run, that we we don't append and have duplicates in our CSV
	try:
	    os.remove('fileList.csv')
	except OSError:
	    pass


def pickRandomRow():
	with open('fileList.csv') as f:
		reader = csv.reader(f)
		chosen_row = random.choice(list(reader))
		return(chosen_row)

def chooseSomeFiles(bytesToFill):
	# this is the idea:
	# access a global storage list to store filenames that we'll be keeping
	# pick a random file from the CSV file
	# check if adding it will take up more room than we have free
	# if we have room free, add it to the storage list
	# on next check, see if the filename exists.  If so ignore. 
	# If not... repeat until no room left

	# access a global storage list to store filenames that we'll be keeping
	global storageList
	global storageListSize


	# pick a random file from the CSV file
	randomRow = pickRandomRow()
	storageList.append(randomRow)

	print("Picking files randomly.  This takes time. Please be patient")

	# check if adding it will take up more room than we have free
	while storageListSize <= bytesToFill:

		addToList = False #should we add the random file to the list?

		#check if the file exists in our list and don't add it if so
		for fileDetails in storageList:
			#if we find the file is already in the list
			if fileDetails[0] == randomRow[0]: 
				addToList = False
			else:
				addToList = True
			 	
		if addToList:
			storageList.append(randomRow)
			storageListSize += int(randomRow[1])


		#pick another random row for testing on next loop
		randomRow = pickRandomRow()

	print("Done selecting random files!")



def finalCopy(destinationPath):

	global storageList

	if not os.path.exists(destinationPath):
	    os.makedirs(destinationPath)
	    print("created folder 'copiedFiles' under current folder")

	for item in storageList:
		filename = os.path.basename(item[0])
		copyfile(item[0], os.path.join(destinationPath, filename))
		print("copying ", item[0])

	print("All done.  Files can now be found at ", destinationPath)		



############################################
# Fill up a USB stick / or any other folder
# with files up to a certain amount of space
# Files are randomly chosen.  The idea is, a 
# photo frame that needs refilling from time
# to time, but no effort required in picking 
# photos
############################################

#setup the variables as empty for first run
fileList 				= [] 	# probably depreciated soon, ignore
fileCount 				= 0		# just how many files we have in total when doing initial search
fileSizeTotalOriginal 	= 0		# How much size our original file search was
storageList 			= []	# A list of filenames that we will add to as our final list of files to copy
storageListSize			= 0		# How many bytes in total we're going to be copying, this grows as we add more files to the list for comparison later

#delete any temp files before run for a clean start
deleteCSVFile()

#compile a list of files of a certail filetype only
fileTypeToSearchFor = input("What file type are we looking for?  (example 'jpg'): ")
pathToSearch = input("Enter path to search.  (Example : /Users/miguel/Pictures) ")
loadFileNames(fileTypeToSearchFor, pathToSearch)

print ("Looking in ", pathToSearch)
print ("Total files found: ", str(fileCount))
print ("Total file size of: ", round(fileSizeTotalOriginal / 1073741824,2), "GB / ", fileSizeTotalOriginal, "bytes")

#ask how many GB of files the user wants to copy
GBToFill = input("How many GB of files do you want to copy? ")
bytesToFill = int(GBToFill) * 1073741824
print(str(GBToFill), "GB is ", str(bytesToFill), "bytes")

if int(bytesToFill) > int(fileSizeTotalOriginal):
	print("WARNING!  You must choose to copy LESS than or EQUAL to the total available (", fileSizeTotalOriginal,"bytes)")
	print("exiting... please run again")
	exit()
else:
	#search through CSV and randomly pick bytesToFill's worth of files
	chooseSomeFiles(bytesToFill)

	#copy the files to a destination folder within the current folder
	destinationPath = input("Enter destination path. (Example: /Users/miguel/Desktop/randomFiles)")
	finalCopy(destinationPath)