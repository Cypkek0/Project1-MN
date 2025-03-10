import pandas as pd
import numpy as np

dataFrame = pd.read_csv("ubisoft.csv")
samples_arr = dataFrame["Zamkniecie"]
samples = samples_arr.to_numpy()
macd = []

def eman_calc (samples,n,index):
    sum_nom = 0
    sum_denom = 0
    alpha = 2/(n+1)
    for x in range(n):
        sum_nom += ((1-alpha)**x)*samples[index-x]
        sum_denom += (1-alpha)**x
    return sum_nom/sum_denom

def macd_calc (samples,index):
    ema12 = eman_calc(samples,12,index)
    ema26 = eman_calc(samples,26,index)
    return ema12-ema26


# for sample in samples[25:]:
#      macd.append(macd_calc(samples))

for index, sample in enumerate(samples[25:], start=25):
    macd.append(macd_calc(samples,index))

for e in macd:
    print(e)

def print_hi(name):

    print(f'{name}')



