

import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import axis


initialBalance = 100.0
lossFraction = 0.83
winFraction = 1.2
nPlayers = 200
nRounds = 1000
maxTransaction = 1000
minTransactuion = 1

   

def doSimulation():
    df = pd.DataFrame(index=np.arange(nPlayers))
    df['balance'] = initialBalance
    print(df)
    previousBalanceColumn = 'balance'
    
    for round in range(nRounds):
        balanceColumn = f'balance-{round}'
        df[balanceColumn] =  df.apply(lambda p: p[previousBalanceColumn] * (lossFraction if random.random() >= 0.5 else winFraction), axis=1)
            
        dfSorted = df.sort_values(balanceColumn)
        totalWealth = dfSorted[balanceColumn].sum()
        
        dfSorted['cumulativeWealth'] = dfSorted[balanceColumn].cumsum() / totalWealth
        dfSorted['cumulativePopulation'] = (dfSorted.reset_index().index + 1.0) / len(dfSorted)
        dfSorted['giniNumbers'] = dfSorted['cumulativePopulation'] - dfSorted['cumulativeWealth']
        giniIndex = dfSorted['giniNumbers'].sum() / len(df) * 2
        print(f'After round {round}, Gini index is {giniIndex}')
        previousBalanceColumn = balanceColumn


if __name__ == '__main__':
    doSimulation()