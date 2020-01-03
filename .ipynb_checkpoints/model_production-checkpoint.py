import pandas as pd
import pickle
from io import StringIO
import time
import datetime

import os

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier

#https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
#https://stackoverflow.com/questions/28656736/using-scikits-labelencoder-correctly-across-multiple-programs

filename = 'model_cler.sav'
best_model = pickle.load(open(filename, 'rb'))

pkl_file = open('MinMaxScaler.pkl', 'rb')
sc = pickle.load(pkl_file) 
pkl_file.close()

pkl_file = open('LabelEncoder.pkl', 'rb')
encoder = pickle.load(pkl_file) 
pkl_file.close()

path = r"C:\Users\André\AppData\Roaming\MetaQuotes\Tester\D0E8209F77C8CF37AD8BF550E51FF075\Agent-127.0.0.1-3000\MQL5\Files"
file_ask_ml = path + "\\ask_ml.csv";
file_confirmation = path + "\\confirmation";

def confirmationFile():
    if os.path.exists(file_confirmation):
        os.remove(file_confirmation)
        return True
    return False;

while True:
    try:
        if os.path.exists(file_ask_ml):
        #if confirmationFile():
            time.sleep(1)
            value = pd.read_csv(file_ask_ml, sep=";", encoding='utf-16')
            #value.drop(['take','status','oper'], axis=1, inplace=True)
            
            columns_categorical = value.select_dtypes(include=['object']).columns
            for col_cat in columns_categorical:
                value[col_cat] = encoder.fit_transform(value[col_cat])
                
            value = sc.transform(value)
            predict = best_model.predict(value)
            predict_proba = best_model.predict_proba(value)
            
            proba = predict_proba[0] >= 0.9;
            
            fileName = '\\nada.txt';
            if(predict == 'Gain'):
                fileName = '\\gain.txt';
            elif(predict == 'Loss'):
                fileName = '\\loss.txt';

            """fileName = '\\nada.txt';
            if proba[0] == True:
                fileName = '\\gain.txt';
            if proba[1] == True:
                fileName = '\\loss.txt';"""
                
            fwrite = path + fileName
            file1 = open(fwrite,"a")
            file1.write(str(predict[0]))
            file1.close() 
    
            print(proba[0], predict_proba)
            print('Predict:', datetime.datetime.now().time(), '->', predict[0])
            print('')
            os.remove(file_ask_ml)
    except:
        print("An exception occurred")
        os.remove(file_ask_ml)


            
