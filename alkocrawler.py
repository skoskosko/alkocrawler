
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import urllib2
import re
import time
import os
#improtin webdriver for getting list with javascript created content
urls=[
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=0.00&priceMax=2.50",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=2.50&priceMax=5.00",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=5.00&priceMax=7.50",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=7.50&priceMax=10.00",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=10.00&priceMax=12.50",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=12.50&priceMax=15.00",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=15.00&priceMax=17.50",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=17.50&priceMax=20.00",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=20.00&priceMax=22.50",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=22.50&priceMax=25.00",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=25.00&priceMax=50.00",
"http://www.alko.fi/haku/tuotteet/?tags=&page=49&priceMin=50.00&priceMax=100000.00"
]
#pages are divided so everything is show so everything can be crawled
link = []
driver = webdriver.Firefox()


delay = 3
# runned once for everything in folder
#make 12
for wot in range(0,12):
    driver.get(urls[wot])
    time.sleep(5)
    savetofile = repr(driver.page_source)
    savetofile = savetofile.split('muistilistaan', 1)[-1]
    amount = savetofile.count('class="search-result-details"')
    number = True
    while number == True:
        savetofile = savetofile.split('a href="', 1)[-1]
        dum,dummy = savetofile.split('" class="result', 1)
        link.append(dum)
        savetofile = savetofile.split('class="volume">', 1)[-1]
        if 0 == savetofile.count('class="volume"'):
            number = False
# getting links for products straight from returned source file


fdx = open('Viinat.xml','w')
rivi= ""
fdx.write(rivi)
fdx.close()
fdx = open('Viinat.xml','a')
rivi= "<VIINAT>\n"
fdx.write(rivi)

fd = open('Viinat.json','w')
rivi= ""
fd.write(rivi)
fd.close()
fd = open('Viinat.json','a')
rivi= '{"viinat":['
fd.write(rivi)
# created 2 different files, one has json and other has xml

for x in range(0, len(link)):
    placeholderurl = "http://www.alko.fi"
    placeholderurl += link[x]
    # we place url to product page and we go trough it
    req = urllib2.Request(placeholderurl)
    response = urllib2.urlopen(req)
    html = response.read()
    amount = html.count('Alkoholi:')
    #alko has alcohol marked down for all drinks so whit this we make sure that we do not get any napknins and such
    if amount != 0 :
        imagesmeinaa =  html.count('class="etalage_source_image"')
        if imagesmeinaa >= 1:
            html,baka = html.split('class="etalage_source_image"', 1)
        if imagesmeinaa == 0:
            html,baka = html.split('id="image-disclaimer"', 1)
        html = html.split('itemprop="name">', 1)[-1]
        product,dummy = html.split('</h1>', 1)
        html = html.split('class="product-details">', 1)[-1]
        size,dummy = html.split('<span>', 1)
        html = html.split('</span>', 1)[-1]
        html = html.split('</span>', 1)[-1]
        prize,dummy = html.split('<span>', 1)
        html = html.split('itemprop="category">', 1)[-1]
        category,dummy = html.split('</h3>', 1)
        amount = html.count('<p>')
        country ="";
        if amount > 1 :
            html = html.split('<p>', 1)[-1]
            country,dummy = html.split('</p>', 1)
        html = html.split('<p>', 1)[-1]
        manufacturer,dummy = html.split('</p>', 1)
        html = html.split('Alkoholi:', 1)[-1]
        html = html.split('<td> ', 1)[-1]
        alkoholi,dummy = html.split("</td>", 1)
        html = html.split('Energiaa:</td>', 1)[-1]
        html = html.split('<td>', 1)[-1]
        energy,dummy = html.split('</td>', 1)
        html = html.split('class="etalage_thumb_image hires"', 1)[-1]
        html = html.split('src="', 1)[-1]
        image,dummy = html.split('"', 1)
        # here we had lost of parsing from source file. deleting end and beginning and getting info.
        # Not optimized but does its job at getting data to files
        alkoholi = alkoholi.replace(' ', '')[:-1].upper()

        product = product.replace("<", "")
        product = product.replace(">", "")
        product = product.replace('"', "")
        product = product.replace(',', "")
        product = product.replace("\n", "")

        category = category.replace("<", "")
        category = category.replace(">", "")
        category = category.replace('"', "")
        category = category.replace(',', "")
        category = category.replace("\n", "")
        manufacturer = manufacturer.replace("<", "")
        manufacturer = manufacturer.replace(">", "")

        manufacturer = manufacturer.replace('"', "")
        manufacturer = manufacturer.replace('	', "")
        manufacturer = manufacturer.replace("\n", "")
        manufacturer = manufacturer.replace(',', "")
        #removing illegal chars before writing to json file




        product = product.replace("&", "&amp;")
        product = product.replace("'", "&apos;")
        category = category.replace("&", "&amp;")
        category =category.replace("'", "&apos;")
        manufacturer =manufacturer.replace("'", "&apos;")
        manufacturer =manufacturer.replace("&", "&amp;")

        #replacing rest of chars for xml
        alkoholi =alkoholi.replace(",", ".")
        size =size.replace(",", ".")
        prize =prize.replace(",", ".")
        contents = (float(alkoholi)*float(size))/float(prize)

        fdx = open('Viinat.xml','a')
        rivi =" <BOTTLE>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <TITLE>" + product + "</TITLE>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        size = re.sub('[^0-9,.]', '', size)
        rivi = "        <SIZE>" + size + "</SIZE>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        prize = re.sub('[^0-9,.]', '', prize)
        rivi = "        <PRIZE>" + prize + "</PRIZE>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <CATEGORY>" + category + "</CATEGORY>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <COUNTRY>" + country + "</COUNTRY>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <ALCOHOL>" + alkoholi + "</ALCOHOL>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <ENERGY>" + energy + "</ENERGY>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <MANUFACTURER>" + manufacturer + "</MANUFACTURER>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <LINK>" + placeholderurl + "</LINK>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <CONTENTS>" + str(contents) + "</CONTENTS>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi = "        <IMAGE>" + image + "</IMAGE>\n"
        fdx.write(rivi)
        fdx = open('Viinat.xml','a')
        rivi =" </BOTTLE>\n"
        fdx.write(rivi)
        fdx.close()

        product = product.replace("&amp;", "&")
        product = product.replace("&apos;", "'")
        category = category.replace("&amp;", "&")
        category =category.replace("&apos;", "'")
        manufacturer =manufacturer.replace("&apos;", "'")
        manufacturer =manufacturer.replace("&amp;", "&")



        fd = open('Viinat.json','a')
        rivi = '\n    {"title":"' + product + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        size = re.sub('[^0-9,.]', '', size)
        rivi = '"size":"' + size + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        prize = re.sub('[^0-9,.]', '', prize)
        rivi = '"prize":"' + prize + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"category":"' + category + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"country":"' + country + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"alcohol":"' + alkoholi + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"energy":"' + energy + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"manufacturer":"' + manufacturer + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"link":"' + placeholderurl + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"contents":"' + str(contents) + '" , '
        fd.write(rivi)
        fd = open('Viinat.json','a')
        rivi = '"image":"' + image + '"},'
        fd.write(rivi)
        fd.close()



fd = open('Viinat.json', 'rb+')
fd.seek(-1, os.SEEK_END)
fd.truncate()
# remove last comma

fd = open('Viinat.json','a')
rivi= "]}"
fd.write(rivi)
fd.close()


fdx = open('Viinat.xml','a')
rivi= "</VIINAT>"
fdx.write(rivi)
fdx.close()

# close files and exit
