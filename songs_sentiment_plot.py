import pandas as pd
import matplotlib.pyplot as plt
import argparse

def get_album_start_index(df):
    start_album_index = len(df)
    for i in range(len(df)):
        year = df.loc[i,'year']
        if year != 0:
            start_album_index = i
            break
    return start_album_index

def plot_groups(names):
    plt.figure(figsize=(10,5))
    plt.ylim([0, 1])
    for name in names:
        df = pd.read_csv(name+'-scores.csv')
        df_year = df.groupby('year')['score_positive'].mean()
        df_year = df_year[1:]


        plt.plot(df_year)
    plt.legend(names)
    plt.xlabel('Year')
    plt.ylabel('Positiveness')
    plt.title('Sentiment of lyrics')
    plt.grid()
    plt.show()

def scatter_plot_group(name):
    df = pd.read_csv(name+'-scores.csv')
    album_start_index = get_album_start_index(df)
    df = df[album_start_index:]
    plt.figure(figsize=(30, 15))
    plt.ylim([0, 1])
    plt.xlabel('Year')
    plt.ylabel('Positiveness')
    plt.title('Sentiment of '+name+' lyrics')

    plt.plot(df['year'],df['score_positive'], 'ro',markersize=3)

    for i in range(album_start_index,len(df)+album_start_index):
        
        plt.text(df.loc[i,'year'], df.loc[i,'score_positive'], df.loc[i,'name'], 
                fontsize=9, ha='right', va='bottom')
    plt.grid()
    plt.show()

def addArgs(parser):
    parser.add_argument('-single',type=str,required=True,help='name of the group to show the single group plot')
    parser.add_argument('-multiple',nargs='+',required=True,help='name of the groups to show the multiple groups plot')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create the initial dataset.')
    addArgs(parser)

    args = parser.parse_args()

    plot_groups(args.multiple)
    scatter_plot_group(args.single)