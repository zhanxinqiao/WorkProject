import pandas as pd
import numpy as np

datetime=pd.read_table('./data/data.txt',sep=',',header=None,names=['id','sid','behavior','date'])
print(datetime)