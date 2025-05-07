import sys, getopt
import argparse
import movie_budget_scraper,imdb_scraper,imdb_info_scraper,extract
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
if __name__ == '__main__':
    parser = argparse.ArgumentParser('input args：***.py')
    parser.add_argument('-s','--static', default='all') # all/part
    args = parser.parse_args()
    static = args.static
    if static not in ["all","part"]:
        print("the static is an error value ")
        sys.exit(0)
    if static == "all":
        movie_budget_scraper.get_movie_metadat()
        imdb_scraper.get_imdb_url()
        imdb_info_scraper.parse_item_info()
        import movie_by_api
        extract.parse_all_movies()
        print("data has been store,then analyze it...")
    print(static)

    movie_info_ = pd.read_csv('../data/movie_imb_data.csv')
    movie_info = movie_info_.where(movie_info_['title_year']>=2018).dropna(subset=['movie_title'])
    movie_info.head()
    mean_score_per_year = movie_info.groupby(movie_info['title_year']).mean()
    mean_score_per_year.reset_index(inplace=True)
    mean_score_per_year.head()
    fig, axes = plt.subplots(1, 1)
    m1 = sns.distplot(movie_info.imdb_score, bins=15)
    movie_info.genres.value_counts()
    vis1 = sns.lmplot(data=movie_info, x='num_user_for_reviews', y='imdb_score',                  fit_reg=False, hue='genres', size=6, aspect=1)
    fig, axes = plt.subplots(2, 2)
    fig.set_size_inches(11.7, 5.27)
    plt.subplots_adjust(wspace=0.2, hspace=0.4)

    sns.boxplot(data=movie_info, x='genres', y='imdb_score', ax=axes[0, 0])
    sns.boxplot(data=movie_info, x='genres', y='num_user_for_reviews', ax=axes[0, 1])
    sns.boxplot(data=movie_info, x='genres', y='time', ax=axes[1, 0])
    sns.boxplot(data=movie_info, x='genres', y='num_critic_for_reviews', ax=axes[1, 1])

    plt.suptitle('Some data according to their genre')

    plt.show()

    df1 = movie_info.where(movie_info['imdb_score']>=7)
    pl = df1.groupby('genres').movie_title.count()
    pl.plot.pie()

    columnsToEncode = list(movie_info[['title_year','genres']])
    print(columnsToEncode)
    le = LabelEncoder()
    df = movie_info[['title_year','genres','num_user_for_reviews','plot_keywords',
                     'time','imdb_score','num_critic_for_reviews']]
    #df.head()
    for feature in columnsToEncode:
        try:
            df[feature] = le.fit_transform(df[feature])
        except:
            print('Error encoding ' + feature)
    df.head()
    X = df.dropna()
    y = X['imdb_score']
    X = X.drop(['imdb_score','plot_keywords'], axis=1)


    scaler=StandardScaler()
    X = scaler.fit_transform(X)
    y = np.array(y*10).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=33)

    clf = RandomForestClassifier(n_estimators=20)
    print(X_train)
    clf = clf.fit(X_train, y_train)
    clf_y_predict = clf.predict(X_test)
    #print(accuracy_score(y_test, clf_y_predict))

