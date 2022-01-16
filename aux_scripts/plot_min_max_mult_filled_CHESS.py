import matplotlib.pyplot as plt
from csv import reader
import numpy as np
import pandas as pd
import seaborn as sns

# Caminho para os arquivos com os arquivos csv
CSV_PATH = "C:\\shared\\CHESS\\raw"
# Nome dos arquivos sem o nome inicial da carga (Ex: LARGE_) e sem o número da execução e csv final (ex: _22_csv)
CSV_NAME = "run_py"
# Total de execuções
EXEC_NUMBER = 50
# Número de amostras em cada arquivo
SAMPLE_COUNT = 300

# Nome da carga das quais serão geradas as métricas
LOAD_NAME = [
    'eval',
    'optStep',
    'optType',
    'self',
    'sl'
]
    
# Lista de métricas, na ordem que aparecem nos CSVs
metrics = [
    "CPU",
    "RAM",
    "IO",
    "BYTE",
    "GPU",
    "VRAM"
]

metrics_unit = [
    "%",
    "MB",
    "Acess",
    "MB",
    "%",
    "MB"
]

# Indice da métrica no CSV (Ex: CPU = 0, RAM = 1)
METRIC_INDEX = 1

# Tamanho do gráfico em polegadas
#plt.figure(figsize =(11, 6))

# Cores
colors = ['b','g','r','m','y']

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

    maximum = []
    minimum = []

    # Para cada número de amostra, itera todas as execuções e pega max, min e mediana
    for sample_idx in range(SAMPLE_COUNT):
        maximum.append(max([exec[sample_idx] for exec in execution_data]))
        minimum.append(min([exec[sample_idx] for exec in execution_data]))

    plt.plot(maximum, color=colors[idx], alpha=0.90)
    plt.plot(minimum, color=colors[idx], alpha=0.90)
    plt.fill_between(range(300),maximum,minimum, color=colors[idx], label=LOAD_NAME[idx], alpha=0.20)

plt.legend()
plt.show()
