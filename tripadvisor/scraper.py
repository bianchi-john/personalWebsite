import requests
from datetime import datetime
from selenium import webdriver
import signal
import mysql.connector
from time import sleep

def crea_lista(url):
    lista = []
    driver = webdriver.PhantomJS()
    driver.get(url)
    html = driver.page_source
    cerca_indicatore_numero_pagine = html.find('class="pageNum last taLnk')
    dati_con_numero_pagine_totali = html[cerca_indicatore_numero_pagine:]
    inizio_numero_pagine = dati_con_numero_pagine_totali.find('>')
    fine_numero_pagine = dati_con_numero_pagine_totali.find('<')
    numero_pagine = dati_con_numero_pagine_totali[inizio_numero_pagine+1:fine_numero_pagine]
    numero_pagine_intero = int(numero_pagine)
    for i in range (0,numero_pagine_intero):
        conto = i * 30
        conto_stringa = str(conto)
        mark1 = url.find("oa")
        url_part2 = url[mark1:]
        mark2_part = url_part2.find("-")
        mark2 = mark2_part + mark1
        url2 = url[0:mark1+2]+conto_stringa+url[mark2:]
        driver.get(url2)
        html2 = driver.page_source
        cerca_inizio_link_hotel = html2.find("BODYCON")
        cerca_fine_link_hotel = html2.find("disclaimer  ui_section")
        sezione_link_hotel = html2[cerca_inizio_link_hotel:cerca_fine_link_hotel]
        ind = ''.join(c for c in sezione_link_hotel if c not in '"')
        index = [i for i in range(len(ind)) if ind.startswith('href=/Hotel_Review', i)]
        for i in range(0, len(index)):
            part =  ind[index[i]:index[i]+500]
            end = part.find(".html")
            link_hotel = (part[:end+5]).replace("href=","https://www.tripadvisor.it")
            lista.append(link_hotel)
    driver.service.process.send_signal(signal.SIGTERM)
    return lista


def crea_ricerca(url):
    pagine = []
    driver = webdriver.PhantomJS()
    driver.get(url)
    html = driver.page_source
    cerca_indicatore_numero_pagine = html.find('class="pageNum last taLnk')
    dati_con_numero_pagine_totali = html[cerca_indicatore_numero_pagine:]
    inizio_numero_pagine = dati_con_numero_pagine_totali.find('>')
    fine_numero_pagine = dati_con_numero_pagine_totali.find('<')
    numero_pagine = dati_con_numero_pagine_totali[inizio_numero_pagine+1:fine_numero_pagine]
    numero_pagine_intero = int(numero_pagine)
    for i in range (0,numero_pagine_intero):
        conto = i * 30
        conto_stringa = str(conto)
        mark1 = url.find("oa")
        url_part2 = url[mark1:]
        mark2_part = url_part2.find("-")
        mark2 = mark2_part + mark1
        url2 = url[0:mark1+2]+conto_stringa+url[mark2:]
        pagine.append(url2)
    driver.service.process.send_signal(signal.SIGTERM)
    return pagine

def dati_hotel(lista_con_duplicati, pagine_ricerca):
    lista = []
    for j in lista_con_duplicati:
        if j not in lista:
            lista.append(j)
    now = datetime.today().strftime("20%y-%m-%d %H:%M:%S")
    driver = webdriver.PhantomJS()
    mydb = mysql.connector.connect(
      host="localhost",
      user="phpmyadmin",
      passwd="qazxswedc1",
      database="tripadvisor",
    )
    mycursor = mydb.cursor()
    for i in range(0, len(lista)) :
        driver.get(lista[i])
        html = driver.page_source
        driver.get(lista[i])
        id = lista[i][49:57]
        id_solo_numeri = aggiusta_id(id)
        cerca_titolo = html.find('class="ui_header h1"')
        titolo = html[cerca_titolo:cerca_titolo+200]
        titolo_aggiustato = aggiusta_titolo(titolo)
        cerca_numero_recensioni = html.find('reviewCount">')
        numero_recensioni = html[cerca_numero_recensioni:cerca_numero_recensioni+200]
        numero_recensioni_aggiustato = aggiusta_numero_recensioni(numero_recensioni)
        cerca_mappa = html.find('_pin.png|')
        mappa_da_aggiustare = html[cerca_mappa+9:cerca_mappa+27]
        mappa = aggiusta_mappa(mappa_da_aggiustare)
        lati = ottieni_latitudine(mappa)
        longi = ottieni_longitudine(mappa)
        cerca_punteggio = html.find('Punteggio ')
        punteggio = html[cerca_punteggio+7:cerca_punteggio+15]
        punteggio_aggiustato = aggiusta_punteggio(punteggio)
        cerca_numero_stelle = html.find('ui_star_rating star_')
        numero_stelle = html[cerca_numero_stelle+20:cerca_numero_stelle+22]
        numero_stelle_aggiustato = aggiusta_numero_stelle(numero_stelle)
        inizio_lista_servizi = html.find('Servizi della struttura')
        lista_servizi_senza_fine = html[inizio_lista_servizi:]
        fine_lista_servizi = lista_servizi_senza_fine.find('</div></div></div>')
        servizi_totali1 = lista_servizi_senza_fine[:fine_lista_servizi]
        servizi_disponibili = aggiusta_servizi1(servizi_totali1)
        if inizio_lista_servizi == -1:
            inizio_lista_servizi2 = html.find('SERVIZI DELL\'HOTEL')
            lista_servizi_senza_fine2 = html[inizio_lista_servizi2:]
            fine_lista_servizi2 = lista_servizi_senza_fine2.find('</div></div></div>')
            servizi_totali2 = lista_servizi_senza_fine2[:fine_lista_servizi2+1]
            servizi_disponibili = aggiusta_servizi2(servizi_totali2)

        print (id_solo_numeri, titolo_aggiustato, lati, longi, now, numero_recensioni_aggiustato, punteggio_aggiustato, numero_stelle_aggiustato, lista[i], servizi_disponibili)
        mycursor.execute("SELECT ID FROM strutture")
        myresult = mycursor.fetchall()
        id_strutture = []
        for x in myresult:
            id_strutture.append(x)
        id_strutture_stringa = ' '.join(str(x) for x in id_strutture)
        if id_strutture_stringa.find(id_solo_numeri) == -1:
            sql1 = "INSERT INTO strutture (ID, Nome_Struttura, Lat, Lon, Stelle, Link) VALUES (%s, %s, %s, %s, %s, %s)"
            val1 = (id_solo_numeri, titolo_aggiustato, lati, longi, numero_stelle_aggiustato, lista[i])
            mycursor.execute(sql1, val1)
            print(mycursor.rowcount, "Nuovo record inserito nella tabella 'strutture'")
        if lati != "":
            sql2 = "UPDATE strutture SET Lat = %s WHERE ID = %s"
            val2 = (lati, id_solo_numeri)
            mycursor.execute(sql2, val2)
            sql3 = "UPDATE strutture SET Lon = %s WHERE ID = %s"
            val3 = (longi, id_solo_numeri)
            mycursor.execute(sql3, val3)
            print("Record modfificato nella tabella 'strutture'")
        sql4 = "INSERT INTO informazioni (Data, Media_Recensioni, Numero_Recensioni, ID, Servizi) VALUES (%s, %s, %s, %s, %s)"
        val4 = ( now, punteggio_aggiustato, numero_recensioni_aggiustato, id_solo_numeri, ', '.join(servizi_disponibili))
        mycursor.execute(sql4, val4)
        print(mycursor.rowcount, "Nuovo record inserito nella tabella 'informazioni'")
        mydb.commit()
    driver.service.process.send_signal(signal.SIGTERM)

    for i in range(0, len(pagine_ricerca)):
        browser = webdriver.Chrome()
        browser.get(pagine_ricerca[i])
        sleep(20)
        html = browser.page_source
        if html.find('rsdc-prev rsdc-nav ui_icon single-chevron-left rsdc-inactive') == -1:
            browser.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div[2]/div[2]').click()
            sleep(20)
        html2 = browser.page_source
        parte1 = html2.find('rsdc-cell rsdc-day rsdc-disabled')
        now2 = str(now)
        now2_aggiustato = aggiusta_data(now2)
        parte2 = html2.find(now2_aggiustato)
        parte = html2[parte1:parte2]
        conto = parte.count('rsdc-cell rsdc-day rsdc-disabled')
        conto_finale = int(conto)+3
        conto_finale3 = int(conto)+3
        conto_finale_stringa = str(conto_finale)
        conto_finale_stringa3 = str(conto_finale3)

        inizio_giorni = '//*[@id=\"BODY_BLOCK_JQUERY_REFLOW\"]/span/div[3]/div/div[2]/div[3]/span[1]/span['+ conto_finale_stringa +']'
        inizio_giorni_stringa = str(inizio_giorni)
        inizio_giorni2 = '//*[@id=\"BODY_BLOCK_JQUERY_REFLOW\"]/span/div[3]/div/div[2]/div[3]/span[1]/div['+ conto_finale_stringa3 +']'
        inizio_giorni_stringa2 = str(inizio_giorni2)

        try:
            browser.find_element_by_xpath(inizio_giorni_stringa).click()
        
        except:
            browser.find_element_by_xpath(inizio_giorni_stringa2).click()
        
        sleep(20)
        html3 = browser.page_source
        inizio_strutture = html3.find('bodycon_main')
        fine_strutture = html3.find('disclaimer  ui_section')
        strutture = html3[inizio_strutture:fine_strutture]
        ind = ''.join(c for c in strutture if c not in '"')
        index = [i for i in range(len(ind)) if ind.startswith('<a target=_blank href=', i)]
        for i in range(0, len(index)):
            part1 =  ind[index[i]:]
            end1 = part1.find("id=property_")
            link_struttura = (part1[+17:end1]).replace("href=","https://www.tripadvisor.it")
            seleziona_id_struttura = link_struttura[49:57]
            id_struttura_pulito = aggiusta_id(seleziona_id_struttura)
            part2 = part1.find('<div class=price __resizeWatch data-sizegroup=mini-meta-price data-clickpart=chevron_price data-index=0>')
            end2 = part1.find('div class=provider __resizeWatch')
            prezzo = part1[part2+104:end2-13]
            prezzo_aggiustato = ''.join(i for i in prezzo if i.isdigit())
            part3 = part1.find('provider_logo')
            end3 = part1.find('<span class=provider_text>')
            provider = part1[part3+18:end3-3]
            mycursor = mydb.cursor()
            if part3 == -1:
                provider = None
                prezzo_aggiustato = None

            print(provider)
            print()
            print(prezzo_aggiustato)
            print()
            print(id_struttura_pulito)
            sql5 = "UPDATE informazioni SET Provider = %s  WHERE ID = %s and Data=%s"
            val5 = (provider, id_struttura_pulito, now)
            mycursor.execute(sql5, val5)
            sql6 = "UPDATE informazioni SET Prezzo = %s  WHERE ID = %s and Data=%s"
            val6 = (prezzo_aggiustato, id_struttura_pulito, now)
            mycursor.execute(sql6, val6)
        browser.quit()
        mydb.commit()

def ottieni_id_citta(i):
    return i[40:47]

def aggiusta_id(cod):
    a = ''.join(i for i in cod if i.isdigit())
    return a

def aggiusta_titolo(tit):
    mark1 = tit.find("header")
    mark2 = tit.find("</h1>")
    return tit[mark1+11:mark2]

def aggiusta_numero_recensioni(num):
    mark2 = num.find("recensioni")
    a = num[13:mark2-1]
    a = ''.join(i for i in a if i.isdigit())
    return a

def aggiusta_prezzi(pre):
    mark1 = pre.find(">")
    mark2 = pre.find("</div>")
    a = pre[mark1+1:mark2]
    a = ''.join(i for i in a if i.isdigit())
    return a

def aggiusta_punteggio(punt):
    mark1 = punt.find("o")
    mark2 = punt.find("su")
    a = punt[mark1+1:mark2]
    return a

def aggiusta_provider(pro):
    mark1 = pro.find("alt=")
    mark2 = pro.find(">")
    return pro[mark1+4:mark2]

def aggiusta_servizi1(ser):
    a = ''.join(c for c in ser if c not in '"')
    lista = []
    index = [i for i in range(len(a)) if a.startswith('hotels-hotel-review-about-with-photos-Amenity__name--SRjUW>', i)]
    for i in range(0, len(index)):
        part =  a[index[i]+59:index[i]+200]
        end = part.find("<")
        lista.append(part[:end])
    return lista

def aggiusta_servizi2(ser):
    a = ''.join(c for c in ser if c not in '"')
    lista = []
    index = [i for i in range(len(a)) if a.startswith('<div class=textitem data-prwidget-name=text data-prwidget-init=>', i)]
    for i in range(0, len(index)):
        part =  a[index[i]+64:index[i]+200]
        end = part.find("<")
        lista.append(part[:end])
    return lista

def aggiusta_mappa(map):
    a = ''.join(c for c in map if c not in '"')
    b = ''.join(c for c in a if c not in '>')
    return b

def ottieni_latitudine(map):
    mark1 = map.find(",")
    if mark1 == -1:
        return ""
    a = map[0:mark1]
    b = ''.join(c for c in a if c not in ',')
    return b


def ottieni_longitudine(map):
    mark1 = map.find(",")
    if mark1 == -1:
        return ""
    a = map[mark1:]
    b = ''.join(c for c in a if c not in ',')
    return b


def aggiusta_numero_stelle(ste):
    if ste == '50':
        ste = '5'
    elif ste == '45':
        ste = '4,5'
    elif ste == '40':
        ste = '4'
    elif ste == '35':
        ste = '3,5'
    elif ste == '30':
        ste = '3'
    elif ste == '25':
        ste = '2,5'
    elif ste == '20':
        ste = '2'
    elif ste == '15':
        ste = '1,5'
    elif ste == '10':
        ste = '1'
    elif ste == 'l ':
        ste = None
    elif ste == -1:
        ste = None
    return ste

def aggiusta_data(tem):
    if tem[5:7] == "01":
        a = datetime.today().strftime("20%y-0-%d")
    elif tem[5:7] == "02":
        a = datetime.today().strftime("20%y-1-%d")
    elif tem[5:7] == "03":
        a = datetime.today().strftime("20%y-2-%d")
    elif tem[5:7] == "04":
        a = datetime.today().strftime("20%y-3-%d")
    elif tem[5:7] == "05":
        a = datetime.today().strftime("20%y-4-%d")
    elif tem[5:7] == "06":
        a = datetime.today().strftime("20%y-5-%d")
    elif tem[5:7] == "07":
        a = datetime.today().strftime("20%y-6-%d")
    elif tem[5:7] == "08":
        a = datetime.today().strftime("20%y-7-%d")
    elif tem[5:7] == "09":
        a = datetime.today().strftime("20%y-8-%d")
    elif tem[5:7] == "10":
        a = datetime.today().strftime("20%y-9-%d")
    elif tem[5:7] == "11":
        a = datetime.today().strftime("20%y-10-%d")
    else:
        a = datetime.today().strftime("20%y-11-%d")
    return a




lucca = 'https://www.tripadvisor.it/Hotels-g187898-oa00-Lucca_Province_of_Lucca_Tuscany-Hotels.html'
livorno = 'https://www.tripadvisor.it/Hotels-g187897-oa00-Livorno_Province_of_Livorno_Tuscany-Hotels.html'
cascina= 'https://www.tripadvisor.it/Hotels-g793691-oa00-Cascina_Province_of_Pisa_Tuscany-Hotels.html'
pietrasanta = 'https://www.tripadvisor.it/Hotels-g1016839-oa00-Pietrasanta_Province_of_Lucca_Tuscany-Hotels.html'



a1 = crea_lista(cascina)
b1 = crea_ricerca(cascina)
print (dati_hotel(a1,b1))
c1 = crea_lista(lucca)
d1 = crea_ricerca(lucca)
print (dati_hotel(c1,d1))
e1 = crea_lista(livorno)
f1 = crea_ricerca(livorno)
print (dati_hotel(e1,f1))
g1 = crea_lista(pietrasanta)
h1 = crea_ricerca(pietrasanta)
print (dati_hotel(g1,h1))