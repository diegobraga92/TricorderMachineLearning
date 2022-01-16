# -*- coding: utf-8 -*-
"""DTC_experiment_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_hW93H88tRWDxB8UWPpcsdkVHYhGhPYq

# Importação das bibliotecas
"""

import warnings
warnings.filterwarnings("ignore")

import random
import numpy as np
import pandas as pd
import sys
import threading
import psutil
from prettytable import PrettyTable
from matplotlib import pyplot as plt
from IPython.display import clear_output

from sklearn.datasets import load_iris
from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer

from sklearn.model_selection import KFold
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import train_test_split

from sklearn import tree
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import cross_val_score

"""# Funções utilitárias"""

def my_ceil(n):
  if n == 0:
    return 0.1
  else:
    return abs(n * 0.1) + n

def my_floor(n):
  if n == 0:
    return -0.1
  else:
    return n - abs(n * 0.1)

def fillDatasetBlanks(data, df):
  """
  Preenche os espaços vazios do dataset
  -----------------------------------------------------
  data:    Conjunto de dados com campos vazio
  df:      Conjunto de dados base
  -----------------------------------------------------
  Preenche cada celula vazia com um valor aleatório
  entre os mais comuns
  """
  for index in data.columns:
    rows, columns = data.shape
    for i in range(rows):
      value = data.at[i, index]
      if pd.isna(value):
        new_value = df[index].mode()
        data.at[i, index] = new_value[random.randint(0, len(new_value)-1)]
  
  return data

"""# Manipulação da base de dados

Para importar um arquivo é necessário acessar o painel a esquerda, aba 'arquivos', clicar no primeiro ícone e selecionar o arquivo desejado do seu diretorio.
"""

def handleDataset(key, file):
  """
  Importa o conjunto de dados desejado
  ----------------------------------------------------
  file:       Nome do arquivo a ser importado
  target:     Nome do atributo do conjunto de dados
              que será utilizado como a variável alvo
  ----------------------------------------------------
  Importa o conjunto de dados, transforma em um Dataset
  Pandas, elimina as colunas que possuem somente valores
  NaN e separa os dados em atributos (X) e classes (y).
  Retorna o dataset (df), os atributos (X) e as classes
  (y).
  """

  if key == 'heart_disease':
    column_headers = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                      'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    heart_disease = pd.read_csv(file, header=None, names=column_headers, skiprows=100)
    df = pd.DataFrame(data = heart_disease, columns = column_headers)
    df.replace({"target": {2: 1, 3: 1, 4:1}}, inplace=True)
    df = df[df.ca != '?']
    df = df[df.thal != '?']
    df.reset_index(inplace=True)
    df = df.astype('float64')

    return df
    
  elif key == 'banknote':
    column_headers = ['variance', 'curtosis', 'entropy', 'target']
    banknote  = pd.read_csv(file, header=None, names=column_headers, skiprows=400)
    df = pd.DataFrame(data = banknote, columns = column_headers)
    df = df.astype('float64')
    
    return df

  elif key == 'haberman_survival':
    column_headers = ['age', 'year', 'target']
    haberman_survival  = pd.read_csv(file, header=None, names=column_headers, skiprows=100)
    df = pd.DataFrame(data = haberman_survival, columns = column_headers)
    df = df.astype('float64')
    
    return df

  elif key == 'pima_indians_diabetes':
    column_headers = ['n_pregnant', 'glucose', 'blood_pressure', 'triceps_skinfold', 'insulin',
                  'body_mass', 'diabetes', 'age', 'target']
    pima_indians_diabetes = pd.read_csv(file, header=None, names=column_headers, skiprows=250)
    df = pd.DataFrame(data = pima_indians_diabetes, columns = column_headers)
    df = df.astype('float64')

    return df

  elif key == 'sonar':
    sonar = pd.read_csv(file, header=None, skiprows=60)
    df = pd.DataFrame(data = sonar, columns = sonar.columns)
    df.replace({60: {'R': 0, 'M': 1}}, inplace=True)
    df.rename(columns={60: 'target'}, inplace=True)
    df = df.astype('float64')

    return df

  elif key == 'ionosphere':
    abalone = pd.read_csv(file, header=None, skiprows=120)
    df = pd.DataFrame(data = abalone, columns = abalone.columns)
    df.replace({34: {'g': 0, 'b': 1}}, inplace=True)
    df.rename(columns={34: 'target'}, inplace=True)
    df = df.astype('float64')

    return df
  
  elif key == 'phoneme':
    column_headers = ['V1', 'V2', 'V3', 'V4', 'V5', 'target']
    phoneme = pd.read_csv(file, header=None, names=column_headers, skiprows=1800)
    df = pd.DataFrame(data = phoneme, columns = column_headers)
    df = df.astype('float64')
    return df

  elif key == 'mammography':
    column_headers = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'target']
    mammography = pd.read_csv(file, header=None, names=column_headers, skiprows=3500)
    df = pd.DataFrame(data = mammography, columns = column_headers)
    df.replace({'target': {"'-1'": 0, "'1'": 1}}, inplace=True)
    df = df.astype('float64')
    return df

  elif key == 'oil_spill':
    oil_spill = pd.read_csv(file, header=None, skiprows=300)
    df = pd.DataFrame(data = oil_spill, columns = oil_spill.columns)
    df.rename(columns={49: 'target'}, inplace=True)
    df = df.astype('float64')

    return df

def createDecisionTree(X, y):
  """
  Cria a árvore de decisão
  ----------------------------------------------------
  X:    Conjunto de atributos
  y:    Conjunto de classes
  ----------------------------------------------------
  Cria o modela da árvore de decisão utilizando todos os
  dados passados, armazena as características do modelo
  criado e cria uma lista com os nós folhas da árvore.
  Retorna o modelo criado e o conjunto de características
  da árvore.
  """
  
  # Definição da árvore de decisão
  estimator = tree.DecisionTreeClassifier()
  estimator.fit(X = X, y = y)

  # Armazenando as caracteristicas do modelo
  n_nodes = estimator.tree_.node_count
  children_left = estimator.tree_.children_left
  children_right = estimator.tree_.children_right
  feature = estimator.tree_.feature
  threshold = estimator.tree_.threshold

  # Verificando quais nós da árvore são folhas
  is_leaves = np.zeros(shape=n_nodes, dtype=bool)
  
  for node_id in range(n_nodes):
    if not (children_left[node_id] != children_right[node_id]):
      is_leaves[node_id] = True

  return estimator, n_nodes, children_left, children_right, feature, threshold, is_leaves

"""# Criação dos casos de teste"""

def getPaths(t, paths=None, current_path=None):
  """
  Verifica quais são os caminhos únicos da árvore
  ----------------------------------------------------
  t:            Nó inicial
  paths         Conjunto de caminhos da árvore
  current_path: Caminho atual sendo gerado pela função
  ----------------------------------------------------
  Função recursiva que percorre a estrutura da árvore
  e encontra um caminho único da raiz para cada folha da.
  Retorna lista com todos os caminhos encontrados.
  """

  # Função que percorre a árvore e verifica os
  # caminhos únicos do nó a cada folha da árvore

  if paths is None:
    paths = []
  if current_path is None:
    current_path = []

  current_path.append(t)
  if is_leaves[t]:
    paths.append(current_path)
  else:
      getPaths(children_right[t], paths, list(current_path))
      getPaths(children_left[t], paths, list(current_path))
  return paths

def createTestCases(df, paths, children_left, children_right, feature, threshold, is_leaves, clf, target):
  """
  Cria os casos de teste
  ----------------------------------------------------------
  df:             Dataset. Conjunto de dados
  paths:          Conjunto de caminhos da árvore
  children_left:  Referência ao filho a esquerda de cada nó
  children_right: Referência ao filho a direita de cada nó
  feature:        Referência ao atributo (coluna) utilizada
                  como critério em cada nó de decisão
  threshold:      Referência ao valor de decisão utilizado
                  em cada nó de decisão
  is_leaves:      Referência aos nós que são folha
  clf:            Modelo de aprendizagem de máquina
  ----------------------------------------------------------
  Percorre cada caminho único da árvore (gerado anteriormente).
  Em uma cópia do Dataframe realiza as operações de decisão
  presentes na árvore, dessa forma em cada iteração o df é 
  reduzido a amostras que satisfazem todos os critérios do 
  caminho. Se existir uma amostra ela é salva em um novo
  Dataframe, que irá conter um caso de teste para cada caminho
  único. Ainda, cria um novo dataset com o limite (inferior
  ou superior) de cada regra de decisão, e para os outros
  campos valores aleatorios. Retorna o Dataframe contendo os
  casos de teste.
  """

  test_index = []
  test_cases_limit = pd.DataFrame(columns=df.columns)

  for id, item in enumerate(paths):
    test = df.copy(deep=True)
    limit = pd.DataFrame(columns=df.columns)

    # print(item)
    for i in range(len(item)):
      node = item[i]
      column = test.columns[feature[node]]
      value = threshold[node]

      if is_leaves[node]:
        limit.at[0, target] = clf.classes_[np.argmax(clf.tree_.value[node])]
        break

      if item[i+1] == children_right[node]:
        test = test.loc[test[column] > value].copy(deep=True)
        limit.at[0, column] = my_ceil(value)
      else:
        test = test.loc[test[column] <= value].copy(deep=True)
        limit.at[0, column] = my_floor(value)
       
    if not test.empty:
      index = test.index.values
      test_index.append(index[0])
    # print()

    test_cases_limit.loc[id] = limit.iloc[0]
    test_cases_limit = fillDatasetBlanks(test_cases_limit, df)

  return test_index, test_cases_limit

"""
# Execução e teste dos modelos"""

def modelTester(data, train_index, test_index, columns, target):
  """
  Cria os casos de teste
  ----------------------------------------------------------
  train_set:    Conjunto de dados utilizado como treino
  test_set:     Conjunto de dados utilizado como teste
  target:       Nome do atributo que é a variável alvo
  ----------------------------------------------------------
  Realiza a classificação em utilizando qualquer modelo
  definido no dicionário 'testes'. O desempenho é calculado
  utilizando as métricas acurácia balanceada, f1, precisão
  e revocação. É retornado um dicionário com todos os 
  resultados obtidos para cada modelo
  """
  scores = {}  

  clf =  KNeighborsClassifier(n_neighbors=3)

  X_train, y_train = data.iloc[train_index, columns], data.iloc[train_index, target]
  X_test, y_test = data.iloc[test_index, columns], data.iloc[test_index, target]

  clf.fit(X_train, y_train)

  y_pred = clf.predict(X_test) 
  
  scores['accuracy'] = accuracy_score(y_test, y_pred)
  scores['f1'] = f1_score(y_test, y_pred, average='weighted')
  scores['recall'] = recall_score(y_test, y_pred, average='weighted')
  scores['precision'] = precision_score(y_test, y_pred, average='weighted')
      
  return scores

def modelTesterLimit(data, columns, target, df_limit):
  """
  Cria os casos de teste
  ----------------------------------------------------------
  train_set:    Conjunto de dados utilizado como treino
  test_set:     Conjunto de dados utilizado como teste
  target:       Nome do atributo que é a variável alvo
  ----------------------------------------------------------
  Realiza a classificação em utilizando qualquer modelo
  definido no dicionário 'testes'. O desempenho é calculado
  utilizando as métricas acurácia balanceada, f1, precisão
  e revocação. É retornado um dicionário com todos os 
  resultados obtidos para cada modelo
  """

  scores = {}

  clf =  KNeighborsClassifier(n_neighbors=3)

  X_train, y_train = data.iloc[:, columns], data.iloc[:, target]
  X_test, y_test = df_limit.iloc[:, columns], df_limit.iloc[:, target]

  clf.fit(X_train, y_train)

  y_pred = clf.predict(X_test) 
    
  scores['accuracy'] = accuracy_score(y_test, y_pred)
  scores['f1'] = f1_score(y_test, y_pred, average='weighted')
  scores['recall'] = recall_score(y_test, y_pred, average='weighted')
  scores['precision'] = precision_score(y_test, y_pred, average='weighted')
      
  return scores

"""# Testes

Datasets taken from:
- https://jamesmccaffrey.wordpress.com/2018/03/14/datasets-for-binary-classification/
- https://machinelearningmastery.com/standard-machine-learning-datasets/
- https://github.com/jbrownlee/Datasets
"""

THREAD_PERC = 100
NUMBER_OF_THREADS = psutil.cpu_count() * (THREAD_PERC / 100)

arguments = sys.argv[1].split(" ")

print(arguments)

datasets = {}

if "iris" in arguments:
    datasets['iris'] = load_iris()
if "wine" in arguments:
    datasets['wine'] = load_wine()
if "breast_cancer" in arguments:
    datasets['breast_cancer'] = load_breast_cancer()
if "heart_disease" in arguments:
    datasets['heart_disease'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
if "banknote" in arguments:
    datasets['banknote'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt'
if "haberman_survival" in arguments:
    datasets['haberman_survival'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/haberman/haberman.data'
if "pima_indians_diabetes" in arguments:
    datasets['pima_indians_diabetes'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv'
if "sonar" in arguments:
    datasets['sonar'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data'
if "ionosphere" in arguments:
    datasets['ionosphere'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/ionosphere/ionosphere.data'
if "phoneme" in arguments:
    datasets['phoneme'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/phoneme.csv'
if "mammography" in arguments:
    datasets['mammography'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/mammography.csv'
if "oil_spill" in arguments:
    datasets['oil_spill'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/oil-spill.csv'

scores = {}
scores_limit = {}
results = {}

for key, data in datasets.items():
  if type(data) != str:
    df = pd.DataFrame(data = np.c_[data['data'], data['target']], 
                      columns = np.append(data['feature_names'], 'target'))
  else:
    df = handleDataset(key, data)
  
  X = df.loc[:, df.columns != 'target']
  y = df.iloc[:, df.columns == 'target']

  estimator, n_nodes, children_left, children_right, feature, threshold, is_leaves = createDecisionTree(X, y)
  paths = getPaths(0)

  results[key] = {}
  results[key]['number_nodes'] = n_nodes
  results[key]['number_leaves'] = sum(is_leaves)
  results[key]['number_paths'] = len(paths)
  results[key]['leaves'] = [i for i, x in enumerate(is_leaves) if x]
  results[key]['paths'] = paths

  test_index, test_cases_limit = createTestCases(df, paths, children_left, children_right, feature, threshold, is_leaves, estimator, 'target')
  all_index = list(df.index.values)
  train_index = list(np.setdiff1d(all_index, test_index))

  results[key]['number_test_samples'] = len(test_index)
  results[key]['number_limit_test_samples'] = test_cases_limit.shape[0]
  
  columns_index = []
  target_index = 0

  for index in df:
    if index != 'target':
      columns_index.append(df.columns.get_loc(index))
    else:
      target_index = df.columns.get_loc(index)

  scores[key] = modelTester(df, train_index, test_index, columns_index, target_index)
  scores_limit[key] = modelTesterLimit(df, columns_index, target_index, test_cases_limit)

  print(key, ' done')

table = PrettyTable(['', 'accuracy', 'f1', 'recall', 'precision'])
table_limit = PrettyTable(['', 'accuracy', 'f1', 'recall', 'precision'])

for index in scores:
  table.add_row([index, 
                str(round(np.mean(scores[index]['accuracy']), 2)),
                str(round(np.mean(scores[index]['f1']), 2)),
                str(round(np.mean(scores[index]['recall']), 2)),
                str(round(np.mean(scores[index]['precision']), 2))])
  
  table_limit.add_row([index, 
                str(round(np.mean(scores_limit[index]['accuracy']), 2)),
                str(round(np.mean(scores_limit[index]['f1']), 2)),
                str(round(np.mean(scores_limit[index]['recall']), 2)),
                str(round(np.mean(scores_limit[index]['precision']), 2))])

print(table)
print(table_limit)

"""# Teste com 10-fold"""

def modelTesterKFold(data, columns, target):
  """
  Cria os casos de teste
  ----------------------------------------------------------
  train_set:    Conjunto de dados utilizado como treino
  test_set:     Conjunto de dados utilizado como teste
  target:       Nome do atributo que é a variável alvo
  ----------------------------------------------------------
  Realiza a classificação em utilizando qualquer modelo
  definido no dicionário 'testes'. O desempenho é calculado
  utilizando as métricas acurácia balanceada, f1, precisão
  e revocação. É retornado um dicionário com todos os 
  resultados obtidos para cada modelo
  """

  clf = KNeighborsClassifier(n_neighbors=3)
  
  scores = {}
  scores['accuracy'] = []
  scores['f1'] = []
  scores['recall'] = []
  scores['precision'] = []

  cv = KFold(n_splits=10, shuffle=True)

  for train_index, test_index in cv.split(data):

    data.columns != target

    X_train, y_train = data.iloc[train_index, columns], data.iloc[train_index, target]
    X_test, y_test = data.iloc[test_index, columns], data.iloc[test_index, target]

    clf.fit(X = X_train, y = y_train)

    y_pred = clf.predict(X_test) 

    y_test = np.array(y_test)
    
    scores['accuracy'].append(accuracy_score(y_test, y_pred))
    scores['f1'].append(f1_score(y_test, y_pred, average='weighted'))
    scores['recall'].append(recall_score(y_test, y_pred, average='weighted'))
    scores['precision'].append(precision_score(y_test, y_pred, average='weighted'))

  return scores

THREAD_PERC = 100
NUMBER_OF_THREADS = psutil.cpu_count() * (THREAD_PERC / 100)

arguments = sys.argv[1].split(" ")

print(arguments)

datasets = {}

if "iris" in arguments:
    datasets['iris'] = load_iris()
if "wine" in arguments:
    datasets['wine'] = load_wine()
if "breast_cancer" in arguments:
    datasets['breast_cancer'] = load_breast_cancer()
if "heart_disease" in arguments:
    datasets['heart_disease'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
if "banknote" in arguments:
    datasets['banknote'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt'
if "haberman_survival" in arguments:
    datasets['haberman_survival'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/haberman/haberman.data'
if "pima_indians_diabetes" in arguments:
    datasets['pima_indians_diabetes'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv'
if "sonar" in arguments:
    datasets['sonar'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data'
if "ionosphere" in arguments:
    datasets['ionosphere'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/ionosphere/ionosphere.data'
if "phoneme" in arguments:
    datasets['phoneme'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/phoneme.csv'
if "mammography" in arguments:
    datasets['mammography'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/mammography.csv'
if "oil_spill" in arguments:
    datasets['oil_spill'] = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/oil-spill.csv'

scores = {}
threads = []
lock = threading.Lock()

def processDataSetKFold(key, data, lock):
  if type(data) != str:
    df = pd.DataFrame(data = np.c_[data['data'], data['target']], 
                      columns = np.append(data['feature_names'], 'target'))
  else:
    df = handleDataset(key, data)
  
  columns_index = []
  target_index = 0

  for index in df:
    if index != 'target':
      columns_index.append(df.columns.get_loc(index))
    else:
      target_index = df.columns.get_loc(index)

  lock.acquire()
  scores[key] = modelTesterKFold(df, columns_index, target_index)
  lock.release()

for key, data in datasets.items():
  t = threading.Thread(None, processDataSetKFold, None, [key, data, lock])
  threads.append(t)
  t.start()

for t in threads:
  t.join()

table = PrettyTable(['', 'accuracy', 'f1', 'recall', 'precision'])

for index in scores:
  table.add_row([index, 
                str(np.mean(scores[index]['accuracy'])),
                str(np.mean(scores[index]['f1'])),
                str(np.mean(scores[index]['recall'])),
                str(np.mean(scores[index]['precision']))])

print(table)

"""# Outros códigos

"""

import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

import json
with open('scores_10_fold_raw.json', 'w') as fp:
    json.dump(scores, fp, cls=NpEncoder, sort_keys=True, indent=2)

# Download the file.
# from google.colab import files
# files.download('scores_10_fold_raw.json')

my_dpi = 96

test = plt.figure(figsize=(4000/my_dpi, 2000/my_dpi), dpi=my_dpi)
tree.plot_tree(estimator, filled=True)

test.savefig(key + '_tree.png', dpi=my_dpi)
# files.download(key + '_tree.png')