# -*- coding: UTF-8 -*-

from selenium import webdriver  
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

mykey = "日本地震"
print mykey
browser = webdriver.Firefox()  
browser.get('http://search.gmw.cn/search.do?advType=news')  
input =  browser.find_element_by_css_selector('input[type="text"]')

input.send_keys(u"日本地震")
print "done"

#date = browser.find_element_by_id("time").value = "8"
select = Select(browser.find_element_by_id("time"))
#select.deselect_all()
select.select_by_visible_text("2011")
button =  browser.find_element_by_css_selector('button')
button.click()
#browser.quit()  