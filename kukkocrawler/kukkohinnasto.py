# just made with sligh modifications from alkocrawler
# all functionality is same as in alkocrawler
import urllib2
urls=[
"http://www.huoltokukko.fi/hinnasto/"
]
link = []
placeholderurl = "http://www.huoltokukko.fi/hinnasto/"
req = urllib2.Request(placeholderurl)
response = urllib2.urlopen(req)
html = response.read()
html = html.split('class="hinnasto"', 1)[-1]
html,dummy = html.split('class="heading-grey"', 1)

fdx = open('hinnat.xml','w')
rivi= ""
fdx.write(rivi)
fdx.close()
fdx = open('hinnat.xml','a')
rivi= "<HINNAT>\n"
fdx.write(rivi)
amount = html.count('<h2>')

for x in range(0,amount):
    html = html.split('<h2>', 1)[-1]
    merkki,dummy = html.split('</h2>', 1)
    ensimmainen,fummy=html.split('</ul>', 1)
    asioita = ensimmainen.count('<strong>')

    for x in range(0,asioita):
        fdx = open('hinnat.xml','a')
        rivi = "    <ASIA>\n"
        fdx.write(rivi)


        ensimmainen = ensimmainen.split('<strong>', 1)[-1]
        tuote,dummy = ensimmainen.split('</strong>', 1)
        ensimmainen = ensimmainen.split('</strong>', 1)[-1]
        hinta,dummy = ensimmainen.split('</li>', 1)
        fdx = open('hinnat.xml','a')
        rivi = "        <MERKKI>" + merkki + "</MERKKI>\n"
        fdx.write(rivi)
        fdx = open('hinnat.xml','a')
        rivi = "        <TUOTE>" + tuote + "</TUOTE>\n"
        fdx.write(rivi)
        fdx = open('hinnat.xml','a')
        rivi = "        <HINTA>" + hinta + "</HINTA>\n"
        fdx.write(rivi)

        fdx = open('hinnat.xml','a')
        rivi = "    </ASIA>\n"
        fdx.write(rivi)
fdx = open('hinnat.xml','a')
rivi= "</HINNAT>"
fdx.write(rivi)
fdx.close()
