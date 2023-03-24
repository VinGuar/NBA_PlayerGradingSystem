from scipy import stats
import pandas as pd
import numpy as np
from itertools import chain
from unidecode import unidecode



def nopunct(word):

        punctuations = '''!()-[];:'"\,<>./?@#$%^&*_~'''

        no_punct = ""
        for char in word:
            if char not in punctuations:
                no_punct = no_punct + char

        return no_punct





def percentile(stats1, year, name):
    #year = 1980
    df1 = pd.read_csv("Book2.csv")
    df1 = df1.drop('birth_year', axis=1)
    df1 = df1.fillna(0)
    df1["player"] = df1["player"].apply(nopunct)
    df1['player'] = df1['player'].str.lower()
    df1["player"] = df1["player"].apply(unidecode)
    name = nopunct(name)
    name = name.lower()
    name = unidecode(name)



    df = df1[df1.season == year]
    df = df.reset_index()


    playerDF = df[df.player == name]
    playerDF = playerDF.reset_index()
    position = playerDF.iloc[0]["pos"]

    if (position[:1] == "C"):
        position = "C"
    else:
        position = position[:2]

    df = df[df.pos == position]
    df = df.reset_index()
    

    for key in stats1:
        current = stats1[key]
        header = df[df.columns[df.columns.str.contains(pat = key.lower())]] 
        array1 =  header.values.tolist()
        array1 = list(chain.from_iterable(array1))

      
        percent = stats.percentileofscore(list(array1), float(current))
        stats1[key] = percent

    return stats1