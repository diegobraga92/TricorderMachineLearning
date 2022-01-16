import matplotlib.pyplot as plt
from csv import reader

CSV_PATH = "C:\\shared\\raw"
CSV_NAME = "dtc_experiment_code_py"
EXEC_NUMBER = "6"
SAMPLE_COUNT = 100

class LoadData:
    load_name = ''
    color_char = ''

    def __init__(self,a:str, b: str):
        self.load_name = a
        self.color_char = b
    
LOAD_LIST = [
    LoadData("OIL_MAMMO",'b'),
    LoadData("CANCER_PHON",'g'),
    LoadData("IONO_SOLAR",'r'),
    LoadData("BANK_PIMA",'m'),
    LoadData("WINE_HEART",'y'),
    LoadData("IRIS_HABER",'c')
]

class PerfData:
    data_name = ''
    start_y = 0
    metric_y = 0
    x_label = ''
    y_label = ''
    title = ''
    metric_map = {}

    def __init__(self,a:str, b: int, c: int, d: str, e: str, f: str):
        self.data_name = a
        self.start_y = b
        self.metric_y = c
        self.x_label = d
        self.y_label = e
        self.title = f
        self.metric_map = {}

perf_list = [
    PerfData("cpu",0,100,"Samples (100ms)","Percentage (%)","CPU Usage"),
    PerfData("ram",150,350,"Samples (100ms)","Megabytes (MB)","RAM Usage"),
    PerfData("io",0,2500,"Samples (100ms)","Accesses (/10)","I/O Accesses"),
    PerfData("byte",0,350,"Samples (100ms)","Megabytes (MB)","I/O Bytes")
]

for idx,perf in enumerate(perf_list):
    plt.figure(idx)
    plt.title(perf.title)
    plt.axis([0, SAMPLE_COUNT, perf.start_y, perf.metric_y])
    plt.xlabel(perf.x_label)
    plt.ylabel(perf.y_label)
    for load in LOAD_LIST:
        perf.metric_map[load.load_name] = []

load_names = []

for load in LOAD_LIST:
    load_names.append(load.load_name)
    file_path = CSV_PATH + "\\" + load.load_name + "_" + CSV_NAME + "_" + EXEC_NUMBER + "_csv"

    with open(file_path,'r') as read_obj:
        csv_reader = reader(read_obj)

        for row in csv_reader:
            try:
                values = row[0].split(';')
                for idx,perf in enumerate(perf_list):
                    perf.metric_map[load.load_name].append(float(values[idx]))
            except:
                continue

for perf_idx,perf in enumerate(perf_list):
    plt.figure(perf_idx)
    for load_idx,load in enumerate(LOAD_LIST):
        plt.plot(perf.metric_map[load.load_name], color=load.color_char, label=load.load_name)

    plt.legend(load_names)
    plt.savefig(perf.data_name+".png")
    plt.close()

