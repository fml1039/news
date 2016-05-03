# -*- coding: UTF-8 -*-

from selenium import webdriver  
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

mykey = u"日本 地震"
print mykey

browser = webdriver.Firefox()  
browser.get('http://search.gmw.cn/search.do?advType=news')  
'''
The following statement can be used to fill the keyword form, yet I don't want to use that

input =  browser.find_element_by_css_selector('input[type="text"]')
input.send_keys(mykey)
print "done"
'''

browser.execute_script("document.getElementById('keyword').value='"+mykey+"'")

select = Select(browser.find_element_by_id("time"))
select.select_by_visible_text("2011")
button =  browser.find_element_by_css_selector('button')
button.click()
#browser.quit()  