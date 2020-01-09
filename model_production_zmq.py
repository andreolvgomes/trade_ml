#https://github.com/dingmaotu/mql-zmq

import zmq
import pandas as pd
import pickle
from io import StringIO
from datetime import datetime

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.svm import SVC

"""
 carregas os obj usados durante o treinamento
"""
best_model = pickle.load(open("SVC.ml", 'rb'))

pkl_file = open('MinMaxScaler.pkl', 'rb')
sc = pickle.load(pkl_file) 
pkl_file.close()

pkl_file = open('LabelEncoder.pkl', 'rb')
encoder = pickle.load(pkl_file) 
pkl_file.close()

"""
inicia o socket
"""
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

"""
   programação do model 
"""

while True:
    message_recv = socket.recv()
    #print(message_recv)
    
    #  Do some 'work'    
    data = message_recv.decode("utf-8")
    split_data = data.split("|")
    
    columns = split_data[0].split(";")
    df = pd.DataFrame([split_data[1].split(';')], columns=columns)
    
    # não consegui definir os tipos das colunas, exemplo: int, double, string. Então vou salvar um csv pra depois carregar novamente
    df.to_csv('to_csv.csv', index=False)
    # carrega tudo novamente, agora sim os tipos estarão definidos
    df = pd.read_csv('to_csv.csv')
    
    #socket.send_string("Env")
    
    #df.drop(['Ref'], axis=1, inplace=True)
    
    # trata os dados categóricos
    columns_categorical = df.select_dtypes(include=['object']).columns
    for col_cat in columns_categorical:
        df[col_cat] = encoder.transform(df[col_cat])
    
    # normaliza dos dados
    X = sc.transform(df)
    
    predict = best_model.predict(X)
    
    str_time = datetime.now().strftime("%H:%M:%S");
    print(str_time, ':', predict[0])
    
    dfc = df[columns_categorical]
    #  Send reply back to client
    socket.send_string(predict[0])
