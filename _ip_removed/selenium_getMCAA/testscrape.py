import mechanize
from time import sleep
from bs4 import BeautifulSoup
#import urllib2 
import http.cookiejar as cookielib ## http.cookiejar in python3

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://www.weblem.org/Admin/Account/Login")

br.select_form(nr=0)
br.form['UserName'] = '113678.shared'
br.form['Password'] = '11112222'
br.submit()
br.find_control(name='accept')
# sleep(5)
# br.open("https://www.weblem.org/Account/Disclaimer")
# sleep(5)
# br.submit(name='accept')
# sleep(5)
#br.open("https://www.weblem.org/")

print (br.response().read())