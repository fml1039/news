
# coding: utf-8

# In[42]:


# Author: Schicheng Zhang (bottle1039@gmail.com) <--- if you have a more permanent email messsage use that
'''
This web scrapper allows one to scrape news information for a particular topic
 in a particular time. This is the traditional way to obtain search result from 
 this website, which is directly add parameters to the actual query url. 

Note there can be replicated data as the website post the same article in different categories 
'''
import datetime, time, bs4, urllib2, smtplib
import re # for regular expression
from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.support.ui import Select
import os.path, os
from httplib import BadStatusLine


# In[43]:

file_location = ''

# Parameters definition
my_key_words = "日本+地震"
search_url = "http://zhannei.baidu.com/cse/search?q=@key&p=@page&s=16378496155419916178&entry=1&area=2"
init_id = 1


# In[44]:

# Function for obtain job list
def obtain_page_html(page_url):
    page_url = str(page_url)
    print ('start download from')
    print page_url
    page_html = urllib2.urlopen(urllib2.Request(page_url)) 

    # Use beautifulsoup to parse the content
    page_html = BeautifulSoup(page_html.read(), 'html.parser')
    print 'Page obtained'
    return page_html


# In[45]:

def construct_search_query(page_id, key_words, address):
    search_query = str(address).replace('@page',str(page_id)).replace('@key', str(key_words))
    return search_query


# In[46]:

def extract_search_information(result_object_list):
    result_str = ''
    for result_object in result_object_list:
        result_object = BeautifulSoup(str(result_object), 'html.parser')
        news_title = result_object.find('a').getText().encode('utf-8').replace('\n','').replace('\r','').replace(',','')
        news_url = result_object.find('a')['href']
        news_date = result_object.find('span',{'class':'c-showurl'}).getText().encode('utf-8').split('...')[1].replace('-','').replace(' ','')
        #obtain_news_detail()
        result_str = result_str + news_title + ',' + str(news_url) + ',' + news_date + '\n'
    return result_str


# In[51]:

def parse_search_result(result):
    output = open('result_list.csv', 'w')
    have_result = result.find('div', {'class':'nors'})
    if have_result != None:
        print "No result found under current condition"
        return -1
    else:
        result_number = result.find('span', {'class':'support-text-top'}).getText().encode('utf-8')
        result_number =  int(re.sub('[^0-9]','',result_number))
        if result_number > 750:
            max_page=74
        else:
            max_page = result_number / 10
    result_object_list = result.findAll('div', {'class':'result f s0'})
    result_str  =''
    result_str = extract_search_information(result_object_list)
    output.write(result_str)
    i = 0
    while i < max_page:
        result_str = ''
        page_id = i+1
        next_query = construct_search_query(page_id, my_key_words, search_url)
        try:
            search_result = obtain_page_html(next_query)
            original_search_html = open('original_html/search_' + str(i) + '.htm', 'w')
            original_search_html.write(str(search_result))
            original_search_html.close()
            result_object_list = search_result.findAll('div', {'class':'result f s0'})
            result_str = extract_search_information(result_object_list)
            i = i + 1
        except BadStatusLine:
            print "BadStatusLine; retrying"
        output.write(result_str)
    output.close()
    return 0


# In[52]:

def extract_news_detail(news_list):
    detail_output = open('news_detail.csv', 'a')
    scraped_list = file('scraped_list.csv', 'r').readlines()
    scraped_output = open('scraped_list.csv', 'a')
    news_id = len(scraped_list)
    for news_info in news_list:
        # catch httperror to handle 404
        try:
            news_detail = ''
            scraped = ''
            news = news_info.split('|')
            if len(news) == 1:
                print news
            if (str(news[1]) + '\n') not in scraped_list and 'v.gmw.cn' not in news[1]:
                news_html = obtain_page_html(news[1])
                if news_html.find('body', {'xmlns':'http://www.w3.org/1999/xhtml'}) != None:
                    news_content = news_html.find('body', {'xmlns':'http://www.w3.org/1999/xhtml'}).getText().encode('utf-8').replace('\n','').replace('\r','')
                elif news_html.find('div', {'id':'contentMain'}) != None:
                    news_content = news_html.find('div', {'id':'contentMain'}).getText().encode('utf-8').replace('\n','').replace('\r','')
                elif news_html.find('div', {'id':'ArticleContent'}) != None:
                    news_content = news_html.find('div', {'id':'ArticleContent'}).getText().encode('utf-8').replace('\n','').replace('\r','')
                elif news_html.find('td', {'id':'body'}) != None:
                    news_content = news_html.find('td', {'id':'body'}).getText().encode('utf-8').replace('\n','').replace('\r','')
                else:
                    print 'new content format'
                    detail_output.close()
                    return 0
                news_detail = news_detail + news[0] + '|' + news[1] + '|' + news[2].replace('\n','') + '|' + news_content + '\n'
                detail_output.write(news_detail)
                original_html = open('original_html/' + str(news_id) + '.htm', 'w')
                original_html.write(str(news_html))
                original_html.close()
                scraped = news[1] + '\n'
                scraped_output.write(str(scraped))
            else:
                print "scraped"
            news_id = news_id + 1
        except urllib2.HTTPError, err:
            print "page not found"
            news = news_info.split('|')
            scraped = news[1] + '\n'
            scraped_output.write(str(scraped))
    detail_output.close()
    scraped_output.close()
    print "news detail collected"


# In[53]:

def output_html_file(file_name, content):
    return 0

def construct_output_file_name(my_key_words, search_url, begin_time, end_time, search_mode, source):
    return 0



# In[54]:

if __name__ == '__main__':
# Obtain current date
    dt = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
    '''
    my_query = construct_search_query(0, my_key_words, search_url)
    search_result = obtain_page_html(my_query)
    parse_search_result(search_result)
    '''
    news_list = file('result_list.csv', 'r').readlines()
    extract_news_detail(news_list)
    


# In[ ]:




# In[ ]:




# In[ ]:



