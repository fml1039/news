
# coding: utf-8

# In[ ]:


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
#from selenium import webdriver  
#from selenium.webdriver.support.ui import Select
import os.path, os
from httplib import BadStatusLine
from socket import error as SocketError


# In[ ]:

file_location = ''

# Parameters definition
#search_url = "http://news.ifeng.com/world/special/ribendizhen/content-2/list_0/@page.shtml"
search_url = "http://news.ifeng.com/listpage/11574/@page/1/rtlist.shtml"
#search_url2 = "http://news.ifeng.com/listpage/11574/@page/1/rtlist.shtml"
init_id = 1


# In[ ]:

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


# In[ ]:

def construct_search_query(page_id, address):
    search_query = str(address).replace('@page',str(page_id))
    return search_query


# In[ ]:

def extract_search_information(result_object_list):
    result_str = ''
    for result_object in result_object_list:
        #result_object = BeautifulSoup(str(result_object), 'html.parser')
        news_title = result_object.getText().encode('utf-8').replace('\n','').replace('\r','').replace(',','')
        news_url = result_object['href']
        #news_date = result_object.find('span',{'class':'c-showurl'}).getText().encode('utf-8').split('...')[1].replace('-','').replace(' ','')
        #obtain_news_detail()
        result_str = result_str + news_title + ',' + str(news_url) + '\n'
    return result_str


# In[ ]:

def parse_search_result(result):
    output = open('result_list.csv', 'w')
    have_result = result.find('div', {'class':'nors'})
    if have_result != None:
        print "No result found under current condition"
        return -1
    else:
        max_page = 127
    result_object_list = BeautifulSoup(str(result.find('div',{'class':'newsList'}))).findAll('a', {'target':'_blank'})
    result_str  =''
    result_str = extract_search_information(result_object_list)
    output.write(result_str)
    i = 20161201
    while i in range(20161201,20161225):
        result_str = ''
        page_id = i
        next_query = construct_search_query(page_id, search_url)
        try:
            search_result = obtain_page_html(next_query)
            original_search_html = open('original_html/search_' + str(i) + '.htm', 'w')
            original_search_html.write(str(search_result))
            original_search_html.close()
            result_object_list = BeautifulSoup(str(search_result.find('div',{'class':'newsList'}))).findAll('a', {'target':'_blank'})
            result_str = extract_search_information(result_object_list)
            i = i + 1
        except BadStatusLine:
            print "BadStatusLine; retrying"
        output.write(result_str)
    output.close()
    return 0


# In[ ]:

def extract_news_detail(news_list):
    detail_output = open('news_detail.csv', 'a')
    scraped_list = file('scraped_list.csv', 'r').readlines()
    scraped_output = open('scraped_list.csv', 'a')
    news_id = len(scraped_list)+1
    for news_info in news_list:
        # catch httperror to handle 404
        try:
            news_detail = ''
            scraped = ''
            news_date=''
            news = news_info.replace('\n','').split(',')
            if str(news[1] + '\n') not in scraped_list:
                news_html = obtain_page_html(news[1])
                for script in news_html(["script", "style"]):
                    script.extract() 
                error_class = news_html.find('div',{'class':'mat'})
                if error_class == None:
                    news_content = news_html.find('div', {'id':'artical_real'}).findAll('p')
                    my_content = ''
                    for content in news_content:
                        my_content = my_content + str(content.getText().encode('utf-8').replace('\n','').replace('\r',''))
                    news_date = str(news[1]).split('/')[4] 
                    news_date = news_date[:4] + '-' + news_date[4:6] + '-' + news_date[6:]
                    #print news_date
                    news_detail = news_detail + news[0] + '|' + news_date + '|' + news[1].replace('\n','') + '|' + my_content + '\n'
                    detail_output.write(news_detail)
                    original_html = open('original_html/' + str(news_id) + '.htm', 'w')
                    original_html.write(str(news_html))
                    original_html.close()
                    scraped = news[1] + '\n'
                    scraped_output.write(str(scraped))
                else:
                    print "page not found"
                    scraped = news[1] + '\n'
                    scraped_output.write(str(scraped))
            else:
                print "scraped"
            news_id = news_id + 1
        except AttributeError:
            print "page not found"
            news = news_info.split(',')
        except urllib2.HTTPError as err:
            print "page not found"
            news = news_info.split(',')
            scraped = news[1] + '\n'
            scraped_output.write(str(scraped))
        except SocketError as e:
            print "page not found"
    detail_output.close()
    scraped_output.close()
    print "news detail collected"


# In[ ]:

def output_html_file(file_name, content):
    return 0

def construct_output_file_name(my_key_words, search_url, begin_time, end_time, search_mode, source):
    return 0



# In[ ]:

if __name__ == '__main__':
# Obtain current date
    dt = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
    
    my_query = construct_search_query(0, search_url)
    search_result = obtain_page_html(my_query)
    parse_search_result(search_result)
    
    news_list = file('result_list.csv', 'r').readlines()
    extract_news_detail(news_list)
    

