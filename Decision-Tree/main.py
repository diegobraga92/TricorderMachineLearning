import sys
print ('Running Inspector Gadget version 02/2019')
print (sys.version)

import time
import glob
import os
import subprocess
from monitor import monitor
from os import listdir
from os.path import isfile, join
import shutil
import json
import hashlib

def create_output_dir(workingdir):
	csvdir = 'raw'
	curdate = time.strftime("%d_%m_%Y")
	curtime = time.strftime("%H%M%S")
	dir = workingdir + '/' + str(curdate)
	
	try:
		os.mkdir(dir)
	except:
		print ('already created dir ' + dir)

	csvdir = dir + '/raw'
	try:
		os.mkdir(csvdir)
	except:
		print ('already created dir ' + csvdir)

	prefix = str(curdate)+'_'+str(curtime)
	return csvdir,prefix

# EXPERIMENT CONFIGURATION #
interval = 0.1
samples = 60
executionsTrain = 30
executionsTest = 30
input_type = 'Decision_Tree'

# INTERNAL CONFIGURATION #

xpath = os.getcwd() + "/" + input_type
print('experiment path: ' + xpath)

bpath = os.getcwd() + "/"
print('bin path: '+ bpath)

exefiles = glob.glob(bpath+"/dtc_experiment_code*.py")

output_path,prefix = create_output_dir(xpath)

experiment_tag = 'data'
prefix = experiment_tag
print("Configuration: "+ prefix)

configs = {
	"SMALLEST":		"iris haberman_survival",
	"SMALL":		"wine heart_disease",
	"MEDIUM-SMALL":	"banknote pima_indians_diabetes",
	"MEDIUM-LARGE":	"ionosphere sonar",
	"LARGE":		"breast_cancer phoneme",
	"LARGEST":		"oil_spill mammography"
}

for sut_server in exefiles:
	sut_server = sut_server.replace('\\','/')
	working_path = xpath

	print ('working path: ' + working_path)
	print ('SUTs: ' + sut_server)

	if sut_server[-22:] == "dtc_experiment_code.py":
		executions = executionsTrain
	else:
		executions = executionsTest

	for key, config in configs.items():
		for i in range(executions):
			print ("execution " + str(i))
			m = monitor(sut_server,key,config,output_path,interval,samples,False,True)
			m.get_samples()
			m.dump_csv(i)

print("Finished")
