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
LOAD_NAME = [
    'OIL_MAMMO',
    'CANCER_PHON',
    'IONO_SOLAR',
    'BANK_PIMA',
    'WINE_HEART',
    'IRIS_HABER'
]
    
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

# Tamanho do gráfico em polegadas
plt.figure(figsize =(11, 6))

# Cores
colors = ['b','g','r','m','y','c']

plt.title(f"{metrics[METRIC_INDEX]}")
plt.xlabel('Sample (100ms)')
plt.ylabel(f'{metrics_unit[METRIC_INDEX]}')

for idx,load in enumerate(LOAD_NAME):
    # Criar uma lista para cada uma das métricas
    execution_data = []

    # Iterata por todos os arquivos de execução
    for exec in range(EXEC_NUMBER):

        file_path = CSV_PATH + "\\" + load + "_" + CSV_NAME + "_" + str(exec) + "_csv"

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

    x_data = []
    y_data = []

    for exect in execution_data:
        for count,sample in enumerate(exect):
            if sample != 0:
                y_data.append(sample)
                x_data.append(count)

    plt.hist(y_data, bins=100, density=False, alpha=0.75)
    #plt.scatter(x_data, y_data, color=colors[idx], label=LOAD_NAME[idx])

plt.legend(LOAD_NAME)
plt.show()
