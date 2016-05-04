#-*- coding: utf-8 -*-
# Author: Schicheng Zhang (bottle1039@gmail.com) <--- if you have a more permanent email messsage use that
'''
This web scrapper allows one to scrape news information for a particular topic
 in a particular time. There is an alternative way to obtain search result from 
 this website, which is directly add parameters to the actual query url. However,
 for education reason, this scraper use selenium which requires a real browser
 to obtain search result
'''
import datetime, time, bs4, urllib2, smtplib
import re # for regular expression
from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.support.ui import Select
import os.path, os

file_location = ''

# Parameters definition
my_key_words = u"日本 地震"
begin_time = "2011-03-10"
end_time = "2011-12-10"
source = "光明网"
search_url = "http://search.gmw.cn/search.do?advType=news"
search_mode = "title"
#search_mode = "content"

def browser_start(url):
    browser = webdriver.Firefox()
    browser.get(url)
    return browser

def set_search_options(my_browser, my_key_words, begin_time, end_time, source, search_mode):
    select_time = Select(my_browser.find_element_by_id("time"))
    select_time.select_by_visible_text("指定日期")
    my_browser.execute_script("document.getElementById('keyword').value='"+my_key_words+"'")
    my_browser.execute_script("document.getElementById('_beginTime').value='"+begin_time+"'")
    my_browser.execute_script("document.getElementById('_endTime').value='"+end_time+"'")
    my_browser.execute_script("document.getElementById('source').value='"+source+"'")
    if search_mode == "title":
        my_browser.execute_script("document.getElementById('location').value='true'")
    else:
        my_browser.execute_script("document.getElementById('location').value='false'")

    '''
    # The following statement can be used to fill the form, yet I don't want to use that
    # Thus, these statements are only take down for learning in case future use

    # Fill in key word
    input =  browser.find_element_by_css_selector('input[type="text"]')
    input.send_keys(mykey)

    # Select drop down option
    select = Select(browser.find_element_by_id("time"))
    select.select_by_visible_text("2011")

    # Click submit button
    button =  browser.find_element_by_css_selector('button')
    button.click()
    '''

def submit_search_options(my_browser, element):
    # Note that as long as the element is in the form which is about to submit, this function will work
    select_submit = my_browser.find_element_by_id(str(element))
    select_submit.submit()

def parse_search_result(html):
    soup = BeautifulSoup(html)
    have_result = soup.find('p', {'class':'no_search'})
    if have_result != None:
        print "No result found under current condition"
        return -1
    else:
        result_number = soup.find('div', {'class':'pull-left'}).getText().encode('utf-8').split('，')[0]
        # Important!!! Note that the comma used in the previous statement to split the string is Chinese comma"，"
        result_number =  int(re.sub('[^0-9]','',result_number))
        print result_number
    '''
    # Output html to local file
    search_result = open('result.html', 'w')
    search_result.write(str(soup))
    search_result.close()
    '''


if __name__ == '__main__':
    my_browser = browser_start(search_url)
    set_search_options(my_browser, my_key_words, begin_time, end_time, source, search_mode)
    submit_search_options(my_browser, 'source')
    parse_search_result(my_browser.page_source)
    #my_browser.quit()  