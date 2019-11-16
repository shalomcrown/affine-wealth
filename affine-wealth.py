#!/usr/bin/python3
'''
Simulation of affine wealth model, loosely based on Scientific American article:
     Bruce M. Boghosian, 'The Inescapable Casino', Scientific American November 2019

Created on Nov 16, 2019

@author: shalom
'''

import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


initialBalance = 100.0
lossFraction = 0.99
winFraction = 1.01
nPlayers = 200
nRounds = 3000
maxTransaction = 100
minTransaction = 1


class Player:
    playerCounter = 0
    orderedTransactions = 0
    
    def __init__(self):
        self.balance = initialBalance
        self.id = Player.playerCounter
        Player.playerCounter += 1
        
    def transaction(self, other):
        if self.id > other.id:
            Player.orderedTransactions += 1
            
        transactionAmount = self.balance * random.random()
            
        if random.random() >= 0.5:
            amount = transactionAmount * winFraction
        else:
            amount = transactionAmount * lossFraction
            
        amount = max(minTransaction, amount)
        amount = min(maxTransaction, amount)
        amount = min(self.balance, amount)
        self.balance -= amount
        other.balance += amount
            
    def __str__(self):
        return f"{self.id}:{self.balance}"
        
        

def doSimulation():
    players = [Player() for _ in range(nPlayers)]
    
    for roundNumber in range(nRounds):
        Player.orderedTransactions = 0
        for transactionNumber in range(nPlayers):

#Commented code - every player must transact with every other player.
#             for transactionNumber2 in range(nPlayers):
#                 if transactionNumber == transactionNumber2:
#                     continue
#                 
#                 players[transactionNumber].transaction(players[transactionNumber2])
            participants = random.sample(players, 2)
            participants[0].transaction(participants[1])
         
        print(f"After round {roundNumber}. Ordered transactions {Player.orderedTransactions}, results: {','.join(str(p) for p in players)}")


    df = pd.DataFrame()
    for player in players:
        df.at[player.id, 'balance'] = player.balance
        
    df = df.sort_values('balance')
    totalWealth = df['balance'].sum()
    
    df['cumulativeWealth'] = df['balance'].cumsum() / totalWealth
    df['cumulativePopulation'] = (df.reset_index().index + 1.0) / len(df)
    df['giniNumbers'] = df['cumulativePopulation'] - df['cumulativeWealth']
    
    giniIndex = df['giniNumbers'].sum() / len(df) * 2
    print(df);
    print(f'Gini index is {giniIndex}')

    fig, ax = plt.subplots()
    ax.plot(df['cumulativePopulation'], df['cumulativeWealth'], label=f'After {nRounds} rounds')
    
    plt.show()

if __name__ == '__main__':
    doSimulation()