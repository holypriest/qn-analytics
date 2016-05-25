import os
from article import Article

articles = {}
for entry in os.listdir('./accesses'):
    articles[entry[0:23]] = Article(entry[0:23])

articles_last_year = {}
for entry in articles:
    if (articles[entry].year >= 2014):
        articles_last_year[entry] = articles[entry]

accesses = {}
for entry in articles_last_year:
    accesses[entry] = articles_last_year[entry].accesses_in_time_interval('2015-04-01', '2016-04-01')

my_articles = sorted(accesses, key=accesses.__getitem__, reverse=True)
for i in range(0,10):
    print(my_articles[i] + '\t' + str(accesses[my_articles[i]]))
