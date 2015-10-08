#!/usr/bin/python

import json
import yaml
import sys
import os
import ast, boto, json, re
from itertools import count
import securitychecker

try:
	__import__('imp').find_module('securitychecker')
	modpath = securitychecker.__file__
        TESTDIR = os.path.dirname(modpath) + "/data/UnitTests"
except:
	TESTDIR = "UnitTests"

class CFTest:
	
	def __init__(self, templatedata, tests):
		self.templatedata = templatedata
		self.tests = tests

	def readUnitTests (self, filename):
        	unitTests = {}
        	# open the provided test file and then read in each line
        	with open(filename) as f:
                	for line in f:
                        	line = line.strip(' \t\n\r')
                        	if line.startswith("#"):
                                	pass    # ignore comments
                        	else:
                                	if len(unitTests) == 0:
                                        	unitTests = ast.literal_eval(line)
                                	else:
                                        	unitTests.update(ast.literal_eval(line))
        	f.close()

        	return unitTests

	def cfengine(self, unitTests):
		cloudf = self.templatedata
		original = cloudf
        	testNum = 1

        	while testNum <= len(unitTests):
                	#initialize status = 0 if currently blank
                	if unitTests[str(testNum)]['status'] == '':
                	        unitTests[str(testNum)]['status'] = 0
                	error = False
                	for key in unitTests[str(testNum)]:
                        	unitTests[str(testNum)][key] = self.checkVariable(str(unitTests[str(testNum)][key]), unitTests)
                        	if str(unitTests[str(testNum)][key]).find("ERROR!!!") >=0:
                                	unitTests[str(testNum)]['result'] = str(unitTests[str(testNum)][key]) + str(key)
                                	error = True
                                	break
                	if error:
                        	#print str(unitTests[str(testNum)]['result'])
                        	break

             		count = 0

                        #checks what the test will be testing against.  Either a cloudformation template or previous results
           	        if unitTests[str(testNum)]['data'] != 'cloudformation':
                	        cloudf = unitTests[str(testNum)]['data']
        	        if unitTests[str(testNum)]['action'] == "request" or unitTests[str(testNum)]['action'] == "count":
	                        if unitTests[str(testNum)].has_key("key"):
                        	        unitTests[str(testNum)]['result'] = self.scanDictforKey(str(testNum), cloudf, unitTests)
             	   	elif unitTests[str(testNum)]['action'] == "dictionary":
              		          if unitTests[str(testNum)].has_key("key"):
					emptylist = []
					unitTests[str(testNum)]['result'] = self.findDictionary(str(testNum), cloudf, unitTests, unitTests[str(testNum)]['key'], [])
                	cloudf = original
        	        testNum = testNum + 1
	        return unitTests


	def runTests (self):
		# run tests

		results = []

		for t in self.tests:
			if len(self.tests) == 1:   # if a single unit test
				unittestfile = t  
			else:
				unittestfile = TESTDIR + "/" + t    # if a set of tests

			unitTests = self.readUnitTests(unittestfile)
			result = self.cfengine(unitTests)
			results.append(str(result[str(len(result))]['result']))
		return results


	def checkVariable(self, variable, unitTests):
        	#verifies that only permitted characters exist within the string
        	if re.match("[^ A-Za-z0-9()<>=:!\[\]]", variable):
                	variable = "ERROR!!! Invalid characters within test case. Field: "
        	#checks to see if there value within the field references another field within the test unit dictionary
        	#if it does, then replace that part with the referenced data
        	elif variable.find("[") >= 0:
                	bracketcount = variable.count("[")

                	for i in xrange(0, bracketcount):
                        	#find the first open bracket and close bracket
                        	openbracket = variable.find("[")
                        	closebracket = variable.find("]")

                        	#ensure that there are no other open brackets between those two identified open and close brackets
                        	#if there is another open bracket keep going through the string until there is only 1 open and 1 close
                        	while variable[openbracket+1:closebracket].find("[") >= 0:
                                	openbracket = variable.find("[", openbracket+1)


                        	#tests to see if the format of the reference is: [test number]:[field]
                        	if str(variable[openbracket+1]).isdigit():
                                	if str(variable[openbracket+1:closebracket]).find(":")>=0:
                                        	testNum = str(variable[openbracket+1:variable.index(":")])
                                        	field = str(variable[variable.index(":")+1:closebracket])
                                        	#update the variable string with the referenced information
                                        	variable= variable[0:openbracket]+str(unitTests[testNum][field])+variable[closebracket+1:len(variable)]
                                	else:
                                        	variable = "ERROR: Unknown formating. Field: "

		return variable

	def scanDictforKey(self, testNum, request, unitTests):
        	value = ""

        	#Checks if the value passed into this function has a key with the requested value
        	if request.has_key(unitTests[str(testNum)]['key']):

                	value = request[unitTests[str(testNum)]['key']]


        	#If it doesn't have a key then it will iterate through all keys looking for additional dictionaries that may contain the key
       		else:
                	for key in request:
                        	if value != "":
                                	break
                        	if type(request[key]) is dict:
                                	value = scanDictforKey(testNum, request[key])
                        	elif type(request[key]) is list:
                                	value = scanListforKey(testNum, request[key])

        	return value

	def scanListforKey(self, testNum, request):
        	value = ""

        	#for each item in the list check if it a dictionary and then look inside it for the key
        	for i in request:
                	if value != "":
                        	break
                	if type(i) is dict:
                        	value = scanDictforKey(testNum, i)
                	elif  type(i) is list:
                        	value = scanListforKey(testNum, i)

        	return value

	def scanListforValue(self, testNum, request):
        	global count

        	value = ""


        	#for each item in the list check if it contains the value we are looking for
        	for i in request:
                	#if it is a dictionary, convert it to a list of it's values and send it back for scanning
                	if type(i) is dict:
                        	value = scanListforValue(testNum, list(i.values()))
                	#if it is another list, send the new list through for scanning
                	elif  type(i) is list:
                        	value = scanListforValue(testNum, i)
                	#if the value exists within the item, set value = True
                	elif str(i).find(unitTests[str(testNum)]['value']) >= 0:
                	        value = 'True'
        	                count = count + 1

	        return value

	def findDictionary(self, testNum, request, unitTests, key, value):
		#checks if the data passed into the function is a dictionary type
		if type(request) is dict:
			if (request.has_key(key)):
				if unitTests[testNum].has_key('value'):
					if str(unitTests[testNum]['value']).find('[') >= 0:
						temp = str(unitTests[testNum]['value'])
						if temp.find('>=') >= 0:
							calcvalue = temp[temp.index('>=')+2:len(temp)-1]
							if request[key] >= calcvalue:
									value.append(request)
									unitTests[testNum]['status'] = True
						elif temp.find('<=') >= 0:
							calcvalue = temp[temp.index('<=')+2:len(temp)-1]
							if request[key] <= calcvalue:
								value.append(request)
								unitTests[testNum]['status'] = True
						elif temp.find('!=') >= 0:
							calcvalue = temp[temp.index('!=')+2:len(temp)-1]
							if request[key] != calcvalue:
								value.append(request)
								unitTests[testNum]['status'] = True
						elif temp.find('>') >= 0:
							calcvalue = temp[temp.index('>')+1:len(temp)-1]
							if request[key] > calcvalue:
								value.append(request)
								unitTests[testNum]['status'] = True
						elif temp.find('<') >= 0:
							calcvalue = temp[temp.index('<')+1:len(temp)-1]
							if request[key] < calcvalue:
								value.append(request)
								unitTests[testNum]['status'] = True
						elif temp.find('=') >= 0:
							calcvalue = temp[temp.index('=')+1:len(temp)-1]
							if request[key] == calcvalue:
								value.append(request)
								unitTests[testNum]['status'] = True

					elif request[key] == unitTests[testNum]['value']:
						value.append(request)
						unitTests[testNum]['status'] = True
				else:
					value.append(request)
					unitTests[testNum]['status'] = True
			else:
				for k in request:

					if type(request[k]) is dict or type(request[k]) is list:
						value = self.findDictionary(testNum, request[k], unitTests, key, value)


		elif type(request) is list:

			for i in request:

				if type(i) is dict or type(i) is list:
					value = self.findDictionary(testNum, i, unitTests, key, value)

		elif type(request) is str:
			#if we get a string that looks like a dictionary or a list send it back to this function as dict or list type
			if request[0] == "{" or request[0] == "[":
				value = self.findDictionary(testNum, ast.literal_eval(request), unitTests, key, value)

		return value


	def fieldSearch (self, testNum, request):

		global unitTests

	
		#checks if the data passed into the function is a dictionary type
		if type(request) is dict:

			unitTests[testNum]['result'] = scanDictforKey(testNum , request)

			#if we found a result and there is no specific value to confirm exists within the result status = True
			if unitTests[testNum]['result'] != "" and not unitTests[testNum].has_key('value'):
				unitTests[testNum]['status'] = "True"
			#if we found a results and there is a specific value that should exist within the result, test for that value
			if unitTests[testNum]['result'] != "" and unitTests[testNum].has_key('value'):
				if unitTests[testNum]['result'].find(unitTests[testNum]['value']) >= 0:
					unitTests[testNum]['status'] = True
		elif type(request) is list:
			unitTests[testNum]['result'] = scanListforKey(testNum , request)
			#if we found a result of the query set status = True
			if unitTests[testNum]['result'] != "":
				unitTests[testNum]['status'] = "True"
		elif type(request) is str:
			#if we get a string that looks like a dictionary or a list send it back to this function as dict or list type
			if request[0] == "{" or request[0] == "[":
				fieldSearch(testNum, ast.literal_eval(request))

		return


	def valueSearch (self, testNum, request):

		global unitTests
		global count

		if type(request) is dict:
			#for every key within the dictionary, test to see if the value contains the value we are looking for
			for key in request:
				if type(request[key]) is str:
					temp = request[key]
					if temp.find(unitTests[testNum]['value']) >= 0:
						count = count + 1
						unitTests[testNum]['status'] = count
					else:
						if temp[0] == "{" or temp[0] == "[":
							valueSearch(testNum, ast.literal_eval(temp))
				elif type(request[key]) is dict:
					test = scanListforValue(str(testNum), list(request[key].value()))
					if test == 'True':
						unitTests[str(testNum)]['status'] = count
				elif type(request[key]) is list:
					test = scanListforValue(str(testNum) , request[key])
					if test == 'True' :
						unitTests[str(testNum)]['status'] = count
		elif type(request) is list:
			test = scanListforValue(str(testNum) , request)
			if test == 'True' :
				unitTests[str(testNum)]['status'] = count

		elif type(request) is str:
			if request[0] == "{" or request[0] == "[":
				valueSearch(testNum, ast.literal_eval(request))

		return
