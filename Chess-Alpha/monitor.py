import sys
import time
import psutil
import time
import datetime
import h5py
import os.path
import numpy
import csv
import matplotlib.pyplot as plt
import subprocess
import GPUtil

class monitor:

    def __init__(self,sut,prefix,config,output_path,interval=0.2,sample_count=100, onefileconcat = False, show_plot=False):

        self.sut = sut
        self.prefix = prefix
        self.config = config
        self.output_path = output_path
        self.interval = interval
        self.sample_count = sample_count
        self.onefile = onefileconcat
        self.show_plot = show_plot
        
        self.cpu_data = []
        self.mem_data = []        
        self.io_data = []
        self.io_bytes = []
        self.gpu_load = []
        self.gpu_memory = []
        self.last_io = 0
        self.last_io_bytes = 0

        print(prefix, config)
        print(sut)

        if sut[-12:] == "run_MODEL.py":
            p = psutil.Popen([sys.executable, sut, "--cmd", config[0], "--type", "normal"])
        else:
            p = psutil.Popen([sys.executable, sut, "--cmd", config[0], "--type", "mini"])

        pid = p.pid

        if (pid != -1):
            self.date = str(datetime.datetime.now())
            self.pid = pid
            self.proc = psutil.Process(pid)
            self.proc_name = os.path.basename(sut)
        else:
            print ('Process not found')

    def get_sample_line(self):

        p = psutil.Process(self.pid)
        
        # the first line is blocking, being responsible for the sampling interval
        raw_cpu = p.cpu_percent(self.interval) / psutil.cpu_count()
        raw_mem = p.memory_info().rss
        sample_io = p.io_counters()
        raw_io_diff =  (sample_io.read_count + sample_io.write_count) - self.last_io
        self.last_io = sample_io.read_count + sample_io.write_count
        # io bytes
        io_bytes_diff =  (sample_io.read_bytes + sample_io.write_bytes) - self.last_io_bytes
        self.last_io_bytes = sample_io.read_bytes + sample_io.write_bytes

        return raw_cpu,raw_mem,raw_io_diff,io_bytes_diff

    def get_samples(self):
        if (self.show_plot == True):
            plt.figure(0)
            plt.axis([0, self.sample_count, 0, 100])
            plt.figure(1)
            plt.axis([0, self.sample_count, 0, 16000])
            plt.figure(2)
            plt.axis([0, self.sample_count, 0, 200])
            plt.figure(3)
            plt.axis([0, self.sample_count, 0, 100])
            plt.figure(4)
            plt.axis([0, self.sample_count, 0, 8000])
            plt.figure(5)
            plt.axis([0, self.sample_count, 0, 1000])
            plt.figure(6)
            plt.axis([0, self.sample_count, 0, 1000])

        # waste the first acquisition to get valid normalize values
        raw_cpu,raw_mem,raw_io_diff,raw_io_bytes = self.get_sample_line()
        for i in range(0,self.sample_count):
            try:
                raw_cpu,raw_mem,raw_io_diff,raw_io_bytes = self.get_sample_line()
                self.cpu_data.append(round(raw_cpu, 1))
                self.mem_data.append(round(raw_mem / (1024*1024), 1))
                self.io_data.append(round(raw_io_diff / 10.0, 1))
                self.io_bytes.append(round(raw_io_bytes / (1024*1024), 1))
                self.gpu_load.append(round(GPUtil.getGPUs()[0].load * 100, 1))
                self.gpu_memory.append(round(GPUtil.getGPUs()[0].memoryUtil * GPUtil.getGPUs()[0].memoryTotal, 1))
            except:
                continue

        if (self.show_plot == True):
            plt.figure(0)
            plt.plot(self.cpu_data, color='b')
            cpuLabel = 'CPU(%)-Mean:'+'{:.1f}'.format(sum(self.cpu_data) / len(self.cpu_data))+'-Max:'+'{:.1f}'.format(max(self.cpu_data))+'-Min:'+'{:.1f}'.format(min(self.cpu_data))
            plt.legend([cpuLabel])
            plt.figure(1)
            plt.plot(self.mem_data, color='g')
            memLabel = 'Mem(MB)-Mean:'+'{:.1f}'.format(sum(self.mem_data) / len(self.mem_data))+'-Max:'+'{:.1f}'.format(max(self.mem_data))+'-Min:'+'{:.1f}'.format(min(self.mem_data))
            plt.legend([memLabel])
            plt.figure(2)
            plt.plot(self.io_data, color='r')
            ioLabel = 'IO-Mean:'+'{:.1f}'.format(sum(self.io_data) / len(self.io_data))+'-Max:'+'{:.1f}'.format(max(self.io_data))+'-Min:'+'{:.1f}'.format(min(self.io_data))
            plt.legend([ioLabel])
            plt.figure(3)
            plt.plot(self.gpu_load, color='y')
            gpuLabel = 'GPU(%)-Mean:'+'{:.1f}'.format(sum(self.gpu_load) / len(self.gpu_load))+'-Max:'+'{:.1f}'.format(max(self.gpu_load))+'-Min:'+'{:.1f}'.format(min(self.gpu_load))
            plt.legend([gpuLabel])
            plt.figure(4)
            plt.plot(self.gpu_memory, color='c')
            vramLabel = 'VRAM(MB)-Mean:'+'{:.1f}'.format(sum(self.gpu_memory) / len(self.gpu_memory))+'-Max:'+'{:.1f}'.format(max(self.gpu_memory))+'-Min:'+'{:.1f}'.format(min(self.gpu_memory))
            plt.legend([vramLabel])
            plt.figure(5)
            plt.plot(self.io_bytes, color='m')
            bytesLabel = 'Bytes(MB)-Mean:'+'{:.1f}'.format(sum(self.io_bytes) / len(self.io_bytes))+'-Max:'+'{:.1f}'.format(max(self.io_bytes))+'-Min:'+'{:.1f}'.format(min(self.io_bytes))
            plt.legend([bytesLabel])
            plt.figure(6)
            plt.plot(self.cpu_data, color='b', label="CPU")
            plt.plot(self.mem_data, color='g', label="RAM")
            plt.plot(self.io_data, color='r', label="IO Access")
            plt.plot(self.io_bytes, color='m', label="IO Bytes")
            plt.plot(self.gpu_load, color='y', label="GPU")
            plt.plot(self.gpu_memory, color='c', label="VRAM")

    def dump_csv(self, num):

        if (self.show_plot == True):
            pname = self.proc_name.replace('.','_')
            plt.figure(0)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_CPU.png")
            plt.close()
            plt.figure(1)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_RAM.png")
            plt.close()
            plt.figure(2)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_IO.png")
            plt.close()
            plt.figure(3)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_GPU.png")
            plt.close()
            plt.figure(4)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_VRAM.png")
            plt.close()
            plt.figure(5)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_Bytes.png")
            plt.close()
            plt.figure(6)
            frame1 = plt.gca()
            frame1.axes.yaxis.set_visible(False)
            plt.savefig(self.output_path+'/'+self.prefix+"_"+pname+'_'+str(num)+"_All.png")
            plt.close()
            
        if (self.onefile == False):
            fname = self.proc_name + '_' + str(num) + '.csv'            
            mode = 'w'
        else:
            fname = self.proc_name + '.csv'
            mode = 'a'

        fname = self.prefix + '_' + fname
        fname = fname.replace('.','_')
        self.output_file_name = self.output_path + '/' + fname
        with open(self.output_file_name, mode) as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in zip(self.cpu_data,self.mem_data,self.io_data,self.io_bytes,self.gpu_load,self.gpu_memory): # no net data for now
                spamwriter.writerow(row)

        try:
            p = psutil.Process(self.pid)
            p.kill()
            print('Process Killed')
        except:
            print('Process Done')



