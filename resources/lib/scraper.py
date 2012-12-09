import mechanize
import cookielib
from time import sleep
import re, sys
import ElementSoup

class scraper:
    def __init__(self):
        self.br = mechanize.Browser()
    def load(self, stationField):
        print "scraper loads with %s"%stationField

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)

        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        # The site we will navigate into, handling it's session
        self.br.open('http://fahrplan.oebb.at/bin/stboard.exe/ds')
#        self.br.open('file:////home/ra/.xbmc/addons/x2/src/ds.html')
        
        # Forms
        self.br.select_form(nr=0)
        text1name=self.br.form.find_control(type="text", nr=0).name  #eg. 'input'
        self.br.form[text1name] = stationField  #"Wien arbeiterstrandbad"
        print "req1 at "+self.br.geturl()
        sleep(1)
        self.br.submit()

        self.br.select_form(nr=0)
        print "req2 at "+self.br.geturl()
        sleep(1)
        self.br.submit()
        

        self.br.select_form(nr=0)
        #<input name="boar.." value="Abfahrtstafel" type="submit">
        #     for c in self.br.form.controls....
        print "req3 at "+self.br.geturl()
        sleep(1)
        self.br.submit(label='Abfahrtstafel')

    def parse(self):
        print "scraper parses"
        #<tr class="depboard-dark">
        #<td class="time">16:51</td>
        #<td class="prognosis"><span class="rtLimit3">16:51</span></td></td>
        #<td class="product centeredText">
        # <a href="hta=sq&"><img class="product" src="/f" alt="U 6" /><br /><span class="nowrap">U 6</span></a></td>
        #<td class="timetable">
        # <strong><a href="http:tart=yes">Siebenhirten</a></strong><br />
        # <a href="http:tart=yes">Wien</a>16:51 - <a href="httyes">W..</td>
        #<td class="platform">2</td>

        
        html = ElementSoup.parse(self.br.response().read(), argIsHtml=True)
        #html = ElementSoup.parse("/home/jo/.xbmc/addons/x2/src/ds.html")

        #print self.br.response().read()
        #for t in html.findall(".//*"): print t.text
        # html is an Element instance
        stuff = {}
        def findxpath(xp):      #accesses current row object
            cc=''
            for f in row.findall(xp) or range(-1):
                cc += f.text or ''
                cc = re.sub("(?m)\\s+", " ", cc)
                cc = re.sub("^ ", "", cc)
                cc = re.sub(" $", "", cc)
            return cc
        
        for row,r in zip(html.findall(".//td[@class='time']/.."), range(3)):
            stuff[r] = {}
                      
            ti=findxpath("./td[@class='time']")
            pr=findxpath("./td[@class='prognosis']//*")
            if pr=="" or re.search("p.nktlich", pr) is not None:
                stuff[r][0]=ti
            else:
                stuff[r][0]=pr+"!"

            stuff[r][1]=findxpath("./td[@class='product centeredText']//*")
            stuff[r][2]=findxpath("./td[@class='timetable']//strong//*")
            stuff[r][3]=findxpath("./td[@class='platform']")
            

        for row in stuff:
            for col in stuff[row]:
                cc = stuff[row][col]
                cc = re.sub('(.{50}).*', '\\1', cc)
                if col==1:
                    cc=re.sub("Bus\s*", "", cc)
                    cc=re.sub("Tram\s*", "", cc)
                stuff[row][col]=cc

                    
        for r in range(3):
            if not r in stuff:
                stuff[r]= {}
            for c in range(4):
                if not c in stuff[r]:
                    stuff[r][c]= ""
        
        #print stuff
        print 'scraper parsing done'#, found %s..'%stuff[0][0]
        return stuff
    
    def reload(self):
        print "scraper reloads"
        self.br.reload()


