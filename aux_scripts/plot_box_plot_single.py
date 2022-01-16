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
]
"""
    'CANCER_PHON',
    'IONO_SOLAR',
    'BANK_PIMA',
    'WINE_HEART',
    'IRIS_HABER'
]
"""
    
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
all_data = []

# Itera por todas as cargas
for idx,load in enumerate(LOAD_NAME):

    # Itera por todos os arquivos de execução
    for exec in range(EXEC_NUMBER):

        file_path = CSV_PATH + "\\" + load + "_" + CSV_NAME + "_" + str(exec) + "_csv"

        # Abre o arquivo
        with open(file_path,'r') as read_obj:
            csv_reader = reader(read_obj)

            # Itera por cada linha do CSV
            for row in csv_reader:
                # Tenta ler os dados do índice referente a métrica e armazena no samples_data
                try:
                    values = row[0].split(';')
                    all_data.append(float(values[METRIC_INDEX]))
                except:
                    continue

# Tamanho do gráfico em polegadas
plt.figure(figsize =(11, 6))

#Plotando o boxplot das espécies em relação ao tamanho das sépalas
bplots = plt.boxplot(all_data,  vert = 0, patch_artist = False)

# Adicionando Título ao gráfico
plt.title("Boxplot Cargas de Trabalho ", loc="center", fontsize=18)
plt.ylabel("Cargas de Trabalho")
plt.xlabel(f'{metrics[METRIC_INDEX]} ({metrics_unit[METRIC_INDEX]})')

plt.show()