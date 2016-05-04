i=1
news_list = file('news_detail.csv','r').readlines()
for news in news_list:
    news = news.split('|')
    if len(news) == 4:
        output = open('data/'+str(i)+'.txt','w')
        my_str = news[0] + '\n' + news[1] + '\n' +news[3]
        output.write(my_str)
        output.close()
        i = i+1
