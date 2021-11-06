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
samples = 300
executionsTrain = 30
executionsTest = 30
input_type = 'BERT'

# INTERNAL CONFIGURATION #

xpath = os.getcwd() + "/" + input_type
print('experiment path: ' + xpath)

bpath = os.getcwd() + "/"
print('bin path: '+ bpath)

exefiles = glob.glob(bpath+"/run_classifier*.py")
exefiles += (glob.glob(bpath+"/run_squad*.py"))
print(exefiles)

output_path,prefix = create_output_dir(xpath)

experiment_tag = 'data'
prefix = experiment_tag
print("Configuration: "+ prefix)

configs = {
	#"MRPC":	    ["--task_name=MRPC","--data_dir=C:/Dev/bert-master/glue_data/MRPC"],
    #"CoLA":		["--task_name=CoLA","--data_dir=C:/Dev/bert-master/glue_data/CoLA"],
	#"XNLI":		["--task_name=XNLI","--data_dir=C:/Dev/bert-master/glue_data/XNLI"],
	#"MNLI":		["--task_name=MNLI","--data_dir=C:/Dev/bert-master/glue_data/MNLI"],
	"SQuADv1":	["--train_file=C:/Dev/bert-master/squad_dir/train-v1.1.json","--predict_file=C:/Dev/bert-master/squad_dir/dev-v1.1.json"],
	"SQuADv2":	["--train_file=C:/Dev/bert-master/squad_dir/train-v2.0.json","--predict_file=C:/Dev/bert-master/squad_dir/dev-v2.0.json"]
}

for sut_server in exefiles:
	sut_server = sut_server.replace('\\','/')
	working_path = xpath
	sut_exe = sut_server[sut_server.rfind("/")+1:]
	print ('working path: ' + working_path)
	print ('SUTs: ' + sut_server)

	if sut_server[-17:] == "run_classifier.py" or sut_server[-12:] == "run_squad.py":
		executions = executionsTrain
	else:
		executions = executionsTest

	for key, config in configs.items():
		if (sut_exe[:9] == "run_squad" and key[:5] == "SQuAD") or (sut_exe[:14] == "run_classifier" and len(key) == 4):
			for i in range(executions):
				print(sut_exe, key)
				print ("execution " + str(i))
				m = monitor(sut_server,key,config,output_path,interval,samples,False,True)
				m.get_samples()
				m.dump_csv(i)
		else:
			print("Skipping missmatched config:", sut_server, key)

print("Finished")
