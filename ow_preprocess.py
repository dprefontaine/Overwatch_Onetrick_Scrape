# -*- coding: utf-8 -*-
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

def preprocess(dataframe_to_process):
    ##no categorical data to change to numericals
    ##data_import = pd.getdummies(data_import, drop_first = True, columns = transformed_columns)

    x = dataframe_to_process.iloc[:,1:]
    
    y = dataframe_to_process.iloc[:,-1]

    ##checking missing values and normalizing
    imputer = SimpleImputer()
    mn = MinMaxScaler()
    ##x

    ##x2 = x2.replace({0:1,1:-1,2:-1,3:-1,4:-1})
    
    x = x.replace("?", np.NaN)
    
    x = imputer.fit_transform(x)
    x = mn.fit_transform(x)

    return x,y