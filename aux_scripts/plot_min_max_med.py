import matplotlib.pyplot as plt
from csv import reader
import numpy as np
import pandas as pd
import seaborn as sns

# Caminho para os arquivos com os arquivos csv
CSV_PATH = "C:\\shared\\01_01_2022\\raw"
# Nome dos arquivos sem o nome inicial da carga (Ex: LARGE_) e sem o número da execução e csv final (ex: _22_csv)
CSV_NAME = "dtc_experiment_code_py"
# Total de execuções
EXEC_NUMBER = 30
# Número de amostras em cada arquivo
SAMPLE_COUNT = 100

# Nome da carga das quais serão geradas as métricas
LOAD_NAME = 'OIL_MAMMO'
    #'OIL_MAMMO'
    #'CANCER_PHON'
    #'IONO_SOLAR'
    #'BANK_PIMA'
    #'WINE_HEART'
    #'IRIS_HABER'
    
# Lista de métricas, na ordem que aparecem nos CSVs
metrics = [
    "CPU",
    "RAM",
    "IO",
    "BYTE"
]

metrics_unit = [
    "%",
    "MB",
    "Acess",
    "MB"
]

# Indice da métrica no CSV (Ex: CPU = 0, RAM = 1)
METRIC_INDEX = 1

# Criar uma lista para cada uma das métricas
execution_data = []

# Iterata por todos os arquivos de execução
for exec in range(EXEC_NUMBER):

    file_path = CSV_PATH + "\\" + LOAD_NAME + "_" + CSV_NAME + "_" + str(exec) + "_csv"

    samples_data = [0] * SAMPLE_COUNT
    count = 0

    # Abre o arquivo
    with open(file_path,'r') as read_obj:
        csv_reader = reader(read_obj)

        # Itera por cada linha do CSV
        for row in csv_reader:
            # Tenta ler os dados do índice referente a métrica e armazena no samples_data
            try:
                values = row[0].split(';')
                samples_data[count] = (float(values[METRIC_INDEX]))
                count += 1
            except:
                continue

    execution_data.append(samples_data)

maximum = []
minimum = []
median = []

import statistics

# Para cada número de amostra, itera todas as execuções e pega max, min e mediana
for sample_idx in range(SAMPLE_COUNT):
    maximum.append(max([exec[sample_idx] for exec in execution_data]))
    minimum.append(min([exec[sample_idx] for exec in execution_data]))
    median.append(statistics.median([exec[sample_idx] for exec in execution_data]))

plt.title(f"{LOAD_NAME} - {metrics[METRIC_INDEX]}")
#plt.axis([0, SAMPLE_COUNT, 0, 300])
plt.xlabel('Sample (100ms)')
plt.ylabel(f'{metrics_unit[METRIC_INDEX]}')
plt.plot(maximum, color='r', label='MAX')
plt.plot(median, color='b', label='MED')
plt.plot(minimum, color='y', label='MIN')
plt.legend(['MAX','MED','MIN'])
plt.show()
#plt.savefig(f'{LOAD_NAME}_{metrics[METRIC_INDEX]}.png')
#plt.close()
