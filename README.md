# Scraper for gmw.cn
This is a web crawling program which collect news from gmw.cn .
This README.MD illustrates the process of this program.
This scraper intends to use selenium package to start a Firefox browser and obtain html through that browser. Selenium is a python package which provides functions of operating on javascript to simulate human browsing. However, with the time and effort spent on this website, the actual url for query is identified. which is 
* http://search.gmw.cn/search.do?c=n&cp=%s&q=%s&tt=false&to=true&sourceName=%s&beginTime=%s&endTime=%s&adv=true&limitTime=0
    * cp - page
    * q - keyword
    * to - order of result; true for descend false for ascend
    * beginTime - begin time; format: yyyy-mm-dd
    * endTime - end time; format: yyyy-mm-dd
    * adv, limitTime - set adv=true and limitTime=0 to make sure conditions take effects

## Files
* `test.py` - For testing functions use
* `gmw_scraper.py` - The scraper prototype of scraping data with Selenium
* `scraper.py` - The scraper in traditional way of obtaining news information
* `news_detail.csv` - the file that stores all news information

## How to run the scraper
* This program relies on several python packages where a user need to install them manually before running the program.
* Install pip
* pip install bs4
* pip install selenium

### Note
for digital ocean we have my edinburgh email address with fortran password there are $55 in the account
