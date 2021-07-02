import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def save_and_clear(name):
    plt.savefig(name+".pdf")
    plt.clf()
    
def graphing_jointplot(data_name, x, y, title, color):
    data = pd.read_csv(data_name)
    sns.jointplot(x=x, y=y, data=data, kind='reg', color=color)
    save_and_clear(title)

def graphing_jointplot_data(data, x, y, title, color):
    sns.jointplot(x=x, y=y, data=data, kind='reg', color=color)
    save_and_clear(title)
    
def graphing_one_tricker_histogram():
    num_bin = 10
    data = pd.read_csv("one_trickers.csv").values[:,1]

    n, bins, patches = plt.hist(data, num_bin, facecolor='purple', alpha =0.5)
    plt.xlabel("Winrates")
    plt.ylabel("Frequency")
    plt.title("One-Tricker Win Rates")
    save_and_clear("One-Tricker Win Rates")
    
def graphing_generalist_histogram():
    num_bin = 10
    data = pd.read_csv("generalists.csv").values[:,1]
    #ADD X LABEL AND Y LABEL TO DATA NAMES
    
    n, bins, patches = plt.hist(data, num_bin, facecolor='green', alpha =0.5)
    plt.xlabel("Winrates")
    plt.ylabel("Frequency")
    plt.title("Generalist Win Rates")
    save_and_clear("Generalist Win Rates")
    
def graphing_both_histogram():
    num_bin = 10
    data1 = pd.read_csv("generalists.csv").values[:,1]
    data2 = pd.read_csv("one_trickers.csv").values[:,1]
    n, bins, patches = plt.hist(data1, num_bin, facecolor='green', alpha =0.5)
    n, bins, patches = plt.hist(data2, num_bin, facecolor='purple', alpha =0.5)
    
    plt.xlabel("Winrates")
    plt.ylabel("Frequency")
    plt.title("Win Rates Comparison")
    save_and_clear("Win Rates Histogram Comparison")
    
##for the line

def graphing_comparison_of_winrate_and_eliminations():
    generalist_data = pd.read_csv("generalists.csv")
    one_tricker_data = pd.read_csv("one_trickers.csv")
    both_sets = pd.concat([generalist_data.assign(dataset="Generalist"),one_tricker_data.assign(dataset="One Tricker")])
     
    sns.scatterplot(x="AvgEliminations",y="Winrate", hue ="dataset", data=both_sets)
    save_and_clear("Comparing Winrates and Average Eliminations")
    
def graphing_comparison_of_winrate_and_deaths():
    generalist_data = pd.read_csv("generalists.csv")
    one_tricker_data = pd.read_csv("one_trickers.csv")
    both_sets = pd.concat([generalist_data.assign(dataset='generalists'),one_tricker_data.assign(dataset="one_trickers")])
    
    sns.scatterplot(x="AvgDeaths",y="Winrate", hue ="dataset", data=both_sets)
    save_and_clear("Comparing Winrates and Average Deaths")
    
def graphing_comparison_of_winrate_and_time_on_fire():
    generalist_data = pd.read_csv("generalists.csv")
    one_tricker_data = pd.read_csv("one_trickers.csv")
    both_sets = pd.concat([generalist_data.assign(dataset='generalists'),one_tricker_data.assign(dataset="one_trickers")])
    
    sns.scatterplot(x="TimeOnFire",y="Winrate", hue ="dataset", data=both_sets)
    save_and_clear("Comparing Winrates and Average Time on Fire")