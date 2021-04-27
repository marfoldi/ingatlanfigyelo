#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function
import time, datetime
import requests
import json
from bs4 import BeautifulSoup
from sys import stdout
import gmail
import re

#ide írd be a keresési url-t (csinálj egy keresést az ingatlan.com-on)
url="https://ingatlan.com/szukites/elado+lakas+i-ker+30-40-mFt+50-60-m2"

#ide írd be az e-mail címet, amire küldje
recipients = ['abc@gmail.com', 'cba@gmail.com']

#ide írd be, hogy hány órakor töltse le az ingatlanokat (indításkor azonnal letölti, majd ezekben az időpontokban)
hours=[8, 14, 20]

def sleep():
    global hours
    now=datetime.datetime.now()
    nextHour=0
    currentHour=now.hour
    for i in range(0, len(hours)):
        if hours[i] > currentHour:
            nextHour=hours[i]
            break
    then=datetime.datetime.now().replace(hour=nextHour, minute=0, second=0, microsecond=0)
    if nextHour == 0:
        then=then+datetime.timedelta(days=1)
    sleepSeconds=(then-now).seconds
    print("Sleeping for " + str(sleepSeconds) + " seconds until " + str(then))
    time.sleep(sleepSeconds)

class Ingatlan:
    def __init__(self, id, hely, ar, negyzetmeter, szobak, kepurl, url):
        self.id = id
        self.hely = hely
        self.ar = ar
        self.negyzetmeter = negyzetmeter[:negyzetmeter.index("terület")].strip()
        self.szobak = szobak
        self.kepurl = kepurl
        self.url=url
    def getUrl(self):
        return "https://ingatlan.com"+str(self.url)
    def getImageUrl(self):
        if self.kepurl=='Nincs kep':
            return 'https://www.jing.fm/clipimg/detail/0-853_house-black-and-white-clip-art-black-and.png'
        else:
            return self.kepurl
    def toString(self):
        return self.getUrl()
    def getMapsUrl(self):
        return "https://maps.google.com/maps/search/" + self.hely.replace(' ', '%20')
    def toHtml(self):
        return """<div class=WordSection1>
<table class=MsoTableGrid border=0 cellspacing=0 cellpadding=0 width=697
 style='width:522.45pt;margin-left:-.4pt;border-collapse:collapse;border:none;
 mso-yfti-tbllook:1184;mso-padding-alt:0cm 5.4pt 0cm 0cm;mso-border-insideh:
 none;mso-border-insidev:none'>
 <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes;height:9.6pt'>
  <td width=16 valign=top style='width:12.1pt;padding:0cm 5.4pt 0cm 0cm;
  height:9.6pt'>
  </td>
  <td width=252 style='width:189.3pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:9.6pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><span style='mso-no-proof:yes'><o:p>&nbsp;</o:p></span></p>
  </td>
  <td width=59 style='width:44.6pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:9.6pt'>
  <p class=MsoNormal align=right style='margin-bottom:0cm;margin-bottom:.0001pt;
  text-align:right;line-height:normal'><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'><o:p>&nbsp;</o:p></span></p>
  </td>
  <td width=369 style='width:276.45pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:9.6pt'>
  </td>
 </tr>
 <tr style='mso-yfti-irow:1;height:31.85pt'>
  <td width=16 valign=top style='width:12.1pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.85pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><span style='mso-no-proof:yes'><o:p>&nbsp;</o:p></span></p>
  </td>
  <td width=252 rowspan=4 style='width:189.3pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.85pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><span style='mso-no-proof:yes'><a href={URL_PH}><img width=228 height=171
  src="{IMAGE_PH}"
  alt="{IMAGE_PH}" v:shapes="Picture_x0020_1"></a></span></p>
  </td>
  <td width=59 style='width:44.6pt;border:none;mso-border-top-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 0cm;height:31.85pt'>
  <p class=MsoNormal align=right style='margin-bottom:0cm;margin-bottom:.0001pt;
  text-align:right;line-height:normal'><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'>Hely:<o:p></o:p></span></p>
  </td>
  <td width=369 style='width:276.45pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.85pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;mso-line-height-alt:
  11.2pt;background:white'><span style='font-size:12.0pt;mso-bidi-font-size:
  11.0pt;mso-fareast-font-family:"Times New Roman";mso-bidi-font-family:Calibri;
  mso-bidi-theme-font:minor-latin;color:#222222;background:white;mso-fareast-language:
  HU'><span style='mso-spacerun:yes'> </span>{HELY_PH} </span><span
  style='font-size:12.0pt;mso-bidi-font-size:11.0pt;mso-fareast-font-family:
  "Times New Roman";mso-bidi-font-family:Calibri;mso-bidi-theme-font:minor-latin;
  mso-fareast-language:HU'><a
  href="{MAPS_HELY_PH}"
  target="_blank"><span style='color:#1155CC;background:white'>(Google Maps)</span></a></span><span
  style='font-size:12.0pt;mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;
  mso-bidi-theme-font:minor-latin'><o:p></o:p></span></p>
  </td>
 </tr>
 <tr style='mso-yfti-irow:2;height:31.9pt'>
  <td width=16 valign=top style='width:12.1pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.9pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><o:p>&nbsp;</o:p></p>
  </td>
  <td width=59 style='width:44.6pt;padding:0cm 5.4pt 0cm 0cm;height:31.9pt'>
  <p class=MsoNormal align=right style='margin-bottom:0cm;margin-bottom:.0001pt;
  text-align:right;line-height:normal'><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'>Ár:<o:p></o:p></span></p>
  </td>
  <td width=369 style='width:276.45pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.9pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><span style='font-size:12.0pt;mso-bidi-font-size:11.0pt;mso-fareast-font-family:
  "Times New Roman";mso-bidi-font-family:Calibri;mso-bidi-theme-font:minor-latin;
  color:#222222;background:white;mso-fareast-language:HU'><span
  style='mso-spacerun:yes'> </span>{AR_PH}</span><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'><o:p></o:p></span></p>
  </td>
 </tr>
 <tr style='mso-yfti-irow:3;height:31.85pt'>
  <td width=16 valign=top style='width:12.1pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.85pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><o:p>&nbsp;</o:p></p>
  </td>
  <td width=59 style='width:44.6pt;padding:0cm 5.4pt 0cm 0cm;height:31.85pt'>
  <p class=MsoNormal align=right style='margin-bottom:0cm;margin-bottom:.0001pt;
  text-align:right;line-height:normal'><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'>Szobák:<o:p></o:p></span></p>
  </td>
  <td width=369 style='width:276.45pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.85pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><span style='font-size:12.0pt;mso-bidi-font-size:11.0pt;mso-bidi-font-family:
  Calibri;mso-bidi-theme-font:minor-latin'><span
  style='mso-spacerun:yes'> </span></span><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-fareast-font-family:"Times New Roman";
  mso-bidi-font-family:Calibri;mso-bidi-theme-font:minor-latin;color:#222222;
  background:white;mso-fareast-language:HU'>{SZOBAK_PH}</span><span
  style='font-size:12.0pt;mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;
  mso-bidi-theme-font:minor-latin'><o:p></o:p></span></p>
  </td>
 </tr>
 <tr style='mso-yfti-irow:4;height:31.9pt'>
  <td width=16 valign=top style='width:12.1pt;border:none;border-right:solid windowtext 1.0pt;
  mso-border-right-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.9pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><o:p>&nbsp;</o:p></p>
  </td>
  <td width=59 style='width:44.6pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 0cm;
  height:31.9pt'>
  <p class=MsoNormal align=right style='margin-bottom:0cm;margin-bottom:.0001pt;
  text-align:right;line-height:normal'><span style='font-size:12.0pt;
  mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'>Méret:<o:p></o:p></span></p>
  </td>
  <td width=369 style='width:276.45pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;mso-border-right-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 0cm;height:31.9pt'>
  <p class=MsoNormal style='margin-bottom:0cm;margin-bottom:.0001pt;line-height:
  normal'><span style='font-size:12.0pt;mso-bidi-font-size:11.0pt;mso-fareast-font-family:
  "Times New Roman";mso-bidi-font-family:Calibri;mso-bidi-theme-font:minor-latin;
  color:#222222;background:white;mso-fareast-language:HU'><span
  style='mso-spacerun:yes'> </span>{MERET_PH}</span><span style='font-size:
  12.0pt;mso-bidi-font-size:11.0pt;mso-bidi-font-family:Calibri;mso-bidi-theme-font:
  minor-latin'><o:p></o:p></span></p>
  </td>
 </tr>
</table>

<p class=MsoNormal><o:p>&nbsp;</o:p></p>

</div>""".replace('{IMAGE_PH}', self.getImageUrl()).replace('{HELY_PH}', self.hely).replace('{AR_PH}', str(self.ar)).replace('{SZOBAK_PH}', self.szobak).replace('{MERET_PH}', self.negyzetmeter).replace('{URL_PH}', self.getUrl()).replace('{MAPS_HELY_PH}', self.getMapsUrl())

def handleUjIngatlanok(ujIngatlanLista):
    if len(ujIngatlanLista)==0:
        print("Nincs új feltöltött ingatlan")
        return
    print(str(len(ujIngatlanLista)) + " új ingatlan")
    sender_name = 'ingatlan.com'
    global recipients
    subject = 'Új ingatlanok!'
    if len(ujIngatlanLista)==1:
        subject='Új ingatlan!'
    emailBody=""
    for ingatlan in ujIngatlanLista:
        price=ingatlan.ar
        place=ingatlan.hely
        emailBody=emailBody+ ingatlan.toHtml() +"<br>"
    for recipient in recipients:
        print("Sending email to " + recipient)
        gmail.send_email(sender_name, recipient, subject, emailBody)


headers_params = {
'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,hu;q=0.7',
 'accept-encoding': 'text/html', 
 'authority': 'ingatlan.com', 
 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 
 'dnt': '1',
 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 
 'pragma': 'no-cache', 
 'cache-control': 'no-cache', 
 'upgrade-insecure-requests': '1'}

session = requests.session()

while True:
    try:
        timeString = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(timeString)
        ingatlanIds=[]
        try:
            ingatlanFile=open("ingatlanok.txt", "r")
            for row in ingatlanFile:
                ingatlanIds.append(row.strip())
            ingatlanFile.close()
        except:
            pass
        ujIngatlanok=[]
        response = session.get(url,  headers=headers_params)
        soup = BeautifulSoup(response.text, "html.parser")
        response=None
        try:
            pages = str(soup.find('div', {'class':'pagination__page-number'}).text)
            numberOfPages=pages[pages.index('/')+2:pages.index('oldal')-1]
        except:
            numberOfPages = 1
        soup=None
        
        pages=None
        for page in range(0,int(numberOfPages)):
            print('\r' + 'Downloading page ' +str(page+1) +'/' + str(numberOfPages), end='')
            stdout.flush()
            pageUrl=url+"?page="+str(page+1)
            response = session.post(pageUrl,  headers=headers_params)
            soup = BeautifulSoup(response.text, "html.parser")
            soup = soup.findAll('div', {'class':'resultspage__listings js-listings'})[0]
            response=None
            for ingatlan in soup.find_all('div', {'class':'listing__card'}):
                ingatlan=ingatlan.parent
                ujIngatlanId=str(ingatlan['data-id'])
                if ujIngatlanId not in ingatlanIds:
                    ar=ingatlan.find('div', {'class':'price'}).text
                    hely=ingatlan.find('div', {'class':'listing__address'}).text
                    negyzetmeter=ingatlan.find('div', {'class':'listing__parameter listing__data--area-size'}).text
                    szobak=ingatlan.find('div', {'class':'listing__parameter listing__data--room-count'}).text
                    kepSoup=ingatlan.find('img', {'class':'listing__image'})
                    ingatlanurl=ingatlan.find('a', {'title':'Részletek'})['href']
                    kepurl="Nincs kep"
                    if kepSoup is not None:
                        kepurl=kepSoup['src']
                    ujIngatlan=Ingatlan(ujIngatlanId, hely, ar, negyzetmeter, szobak, kepurl, ingatlanurl)
                    ujIngatlanok.append(ujIngatlan)
                    ingatlanIds.append(ujIngatlanId)
                    
            soup=None
        print(" - Finished downloading")
        handleUjIngatlanok(ujIngatlanok)
        ingatlanIds=sorted(set(ingatlanIds))
        ingatlanFile=open("ingatlanok.txt", "w")
        ingatlanFile.truncate()
        for ingatlan in ingatlanIds:
            ingatlanFile.write(str(ingatlan) + "\n")
        ingatlanFile.close()
    except KeyboardInterrupt:
        print("Closing application...")
        exit(0)
    except Exception as e:
        print(e)
        sender_name = 'ingatlan.com'
        recipient = recipients[0]
        subject = 'Hiba az ingatlanfigyelo alkalmazasban'
        emailBody="Exception:<br><br>"
        emailBody = emailBody+ str(e)
        gmail.send_email(sender_name, recipient, subject, emailBody)
        pass
    sleep()
