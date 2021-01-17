# Plot the number of calls over a span of times
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sudogen as sg1
import sudogen1 as sg11
import sudogen2 as sg2
import sudogen3 as sg3


"""
This module's aim is to analyse number of calls made per algorithm
"""
sudo1calls = []
sudo1_10calls = []
sudo1_20calls = []
sudo1_50calls = []
sudo1_5calls = []
sudo1_2calls = []

sudo2calls = []
sudo3calls = []
num_puzzle = []
for ctr in range(1001):
    num_puzzle.append(ctr)
    sg1.generateSudoku()
    sudo1calls.append(sg1.getCalls())

    
    sg11.__recursionLimit = 2
    sg11.generateSudoku()
    sudo1_2calls.append(sg11.getCalls())
    sg11.__recursionLimit = 5
    sg11.generateSudoku()
    sudo1_5calls.append(sg11.getCalls())
    sg11.__recursionLimit = 10
    sg11.generateSudoku()
    sudo1_10calls.append(sg11.getCalls())
    sg11.__recursionLimit = 20
    sg11.generateSudoku()
    sudo1_20calls.append(sg11.getCalls())
    sg11.__recursionLimit = 50
    sg11.generateSudoku()
    sudo1_50calls.append(sg11.getCalls())
    
    """
    sg2.generateSudoku()
    sg3.generateSudoku()
    sudo2calls.append(sg2.getCalls())
    sudo3calls.append(sg3.getCalls())
    """

    # Check for potential infinite recursions
    print(ctr)

df = pd.DataFrame()
sudo1series = pd.Series(sudo1calls, name='sudogen1_calls')


# Recursion (Sudo1) Varying
sudo1_2series = pd.Series(sudo1_2calls, name='2 Rec Lim')
sudo1_5series = pd.Series(sudo1_5calls, name='5 Rec Lim')
sudo1_10series = pd.Series(sudo1_10calls, name='10 Rec Lim')
sudo1_20series = pd.Series(sudo1_20calls, name='20 Rec Lim')
sudo1_50series = pd.Series(sudo1_50calls, name='50 Rec Lim')
df = pd.concat([sudo1series, sudo1_2series, sudo1_5series, sudo1_10series, sudo1_20series, sudo1_50series], axis=1)

"""
# Algorithm Varying
sudo2series = pd.Series(sudo2calls, name='sudogen2_calls')
sudo3series = pd.Series(sudo3calls, name='sudogen3_calls')
sudo3series = pd.Series(sudo3calls, name='sudogen3_calls')
df = pd.concat([sudo1series, sudo2series, sudo3series], axis=1)
"""

def genSudo1Box():
    fig1, calls_plot = plt.subplots()
    calls_plot.boxplot(df, showfliers=True)
    calls_plot.set_xticklabels(['Control','2 Rec Lim', '5 Rec Lim','10 Rec Lim', '20 Rec Lim', '50 Rec Lim'], fontsize=10)
    plt.show()

def genSudo1Scatter():
    plot = plt.plot(num_puzzle, df['sudogen1_calls'], 'g.', label = 'Control')
    plot = plt.plot(num_puzzle, df['2 Rec Lim'], 'r.', label = '2 Rec')
    plot = plt.plot(num_puzzle, df['5 Rec Lim'], 'c.', label = '5 Rec')
    plot = plt.plot(num_puzzle, df['10 Rec Lim'], 'y.', label = '10 Rec')
    plot = plt.plot(num_puzzle, df['20 Rec Lim'], 'b.', label = '20 Rec')
    plot = plt.plot(num_puzzle, df['50 Rec Lim'], 'm.', label = '50 Rec')
    plt.xlabel("Puzzle Number")
    plt.ylabel("Number of Lookups")
    plt.legend()
    plt.show()


def generateScatter():
    # Scatter plot maker
    calls_plot = plt.plot(num_puzzle, df['sudogen1_calls'], 'g.', label = 'sudogen1')
    calls_plot = plt.plot(num_puzzle, df['sudogen2_calls'], 'b.', label = 'sudogen2')
    calls_plot = plt.plot(num_puzzle, df['sudogen3_calls'], 'r.', label = 'sudogen3')
    plt.xlabel("Puzzle Number")
    plt.ylabel("Number of Lookups")
    plt.legend()
    plt.show()

def generateBoxWhisker():
    # Box and whiskers
    fig1, calls_plot = plt.subplots()
    calls_plot.boxplot(df, showfliers=False)
    calls_plot.set_ylabel('Number of Lookups')
    calls_plot.set_xticklabels(['sudogen1','sudogen2','sudogen3'], fontsize=10)
    plt.show()

    