import requests#Serve a Selenium per poter accedere alla pagina
from datetime import datetime#Importa la data del sistema per poterla stampare successivamente
from selenium import webdriver#Importa selenium
import signal#Importa signal che servira' per poter interrompere il funzionamento di PhantomJS
import mysql.connector#importa my sql connector che servira' per far interagire python con il linguaggio SQL
from time import sleep#Serve per far attendere selenium che la pagina sia caricata completamente prima di iniziare

# a partire dal link del risultato di una qualsivoglia ricerca sul sito Tripadvisor, questa funzione restituisce tutti i link delle singole strutture che ne risultano
def crea_lista(url):#Funzione che crea una lista contenente tutti i link delle singole strutture, viene dato il link della ricerca e da quello scorrera' tutte le pagine prendendo tutti i link
    lista = []#creo la lista vuota
    driver = webdriver.PhantomJS()#carico il web driver che verra' assegnato a selenium
    driver.get(url)#Dico a selenium che lavorera' sull'argomento url della funzione
    html = driver.page_source#variabile che contiene tutto il testo contenuto nella pagina web che sto analizzando con il web driver di selenium
    cerca_indicatore_numero_pagine = html.find('class="pageNum last taLnk')#dico a selenium di cercare una stringa perche' questa sta sempre vicina all'indicazione del numero di pagine mostrate nei risultati. Non cercare direttamente il numero di pagine perche' ovviemante cambia ogni volta ma questa dicitura rimane fissa in tutte le ricerche
    dati_con_numero_pagine_totali = html[cerca_indicatore_numero_pagine:]#seleziono la parte di testo html che sta dopo la ul testo che ho cercato nel comando precedente, cosi' facendo verra' selezionato anche il numero che indica in numero di pagine
    inizio_numero_pagine = dati_con_numero_pagine_totali.find('>')#cerco nel il carattere immediatamente precedente a cio' che indica il numero delle pagine in modo da delimitare la futura area di ricerca di esso
    fine_numero_pagine = dati_con_numero_pagine_totali.find('<')#cerco nel il carattere immediatamente successivo a cio' che indica il numero delle pagine in modo da delimitare la futura area di ricerca di esso
    numero_pagine = dati_con_numero_pagine_totali[inizio_numero_pagine+1:fine_numero_pagine]#la ricerca del numero viene ripulita da possibili altri caratteri trovati
    numero_pagine_intero = int(numero_pagine)#il numero della pagina viene convertito da stringa ad intero
    for i in range (0,numero_pagine_intero):#viene creato un ciclo che scorrera' le varie pagine e verra' ripetuto tante volte quanto sono il numero dell pagine
        conto = i * 30#l'indice del ciclo viene incrementato sempre di una unita' e successivamente moltiplicato per 30
        conto_stringa = str(conto)#il risultato viene convertito in stringa
        mark1 = url.find("oa")#viene cercata la posizione di queste due lettere contenute nell'url
        url_part2 = url[mark1:]#seleziono una parte dell'url in questione
        mark2_part = url_part2.find("-")#cerco all'interno della seconda parte un carattere che serve per far cambiare la pagina dei risultati in modon da trovarli tutti
        mark2 = mark2_part + mark1#sommo la posizione di questo carattere all'interno della seconda parte dell'url al numero dei caratteri della prima parte in modo tale da ottenerne la sua posizione all'interno dell'intero url, tutta questa operazione e' stata fatta perche' il carattere che delimita la parte finale dell'area di ricerca compare all'interno dell'url ripetuto,per trovare quello giusto e' necessario quindi dividere l'url in due parti in modo da selezionare quello che serve
        url2 = url[0:mark1+2]+conto_stringa+url[mark2:]#viene aggiunto "conto_stringa" al centro di queste due ricerche nell'url, questo perche' ogni volta che viene cambiata pagina tripadvisor aumenta di trenta un numero che si trova in mezzo al link, cosi' facendo io glielo faccio aumentare  manualmente
        driver.get(url2)#Dico a selenium che lavorera' sull'argomento url della funzione che in questo caso saranno tutte le pagine di una determinata ricerca che scorrono grazie al ciclo for
        html2 = driver.page_source#variabile che contiene tutto il testo contenuto nella pagina web che sto analizzando con il web driver di selenium
        cerca_inizio_link_hotel = html2.find("BODYCON")#cerco l'inizio dell'elenco dei link delle strutture
        cerca_fine_link_hotel = html2.find("disclaimer  ui_section")#cerco la fine dell'elenco dei link delle strutture
        sezione_link_hotel = html2[cerca_inizio_link_hotel:cerca_fine_link_hotel]#seleziono questo elenco
        ind = ''.join(c for c in sezione_link_hotel if c not in '"')#sottraggo da questo elenco il carattere (") perche' potrebbe generare errori
        index = [i for i in range(len(ind)) if ind.startswith('href=/Hotel_Review', i)]#cerco quante volte questa dicitura: "href=/Hotel_Review" compare all'interno dell'elenco perche' e' la dicitura che sta prima di ogni link delle strutture. Questo mpassaggio e' utile per creare un ciclo for che scandisca tutte la strutture
        for i in range(0, len(index)):#creo un ciclo che si ripete tante volte quanti sono i link relativi alle strutture all'interno del testo
            part =  ind[index[i]:index[i]+500]#seleziono una parte di testo entro la quale e' contenuto il link di una struttura
            end = part.find(".html")#cerco la parte finale del link in modo tale poi da riuscire a selezionare il link solo senza caratteri superflui
            link_hotel = (part[:end+5]).replace("href=","https://www.tripadvisor.it")#sostituisco la parte inizziale del link ottenuto con un'altra che rendera' il mio link funzionante
            lista.append(link_hotel)#aggiungo il link estrapolato alla lista
    driver.service.process.send_signal(signal.SIGTERM)#alla fine del ciclo chiudo PhantomJS con questo speciale comando
    return lista#restituisco i link di tutte le strutture derivate della ricerca

# a partire dal link ricavato da una qualsivoglia ricerca sul sito Tripadvisor, questa funzione restituisce tutti i link della prima e delle successive pagine di risultati
def crea_ricerca(url):
    pagine = []#creo una lista vuota la quale conterra' i link delle varie pagine di ricerca
    driver = webdriver.PhantomJS()#carico il web driver che verra' assegnato a selenium
    driver.get(url)#Dico a selenium che lavorera' sull'argomento url della funzione
    html = driver.page_source#variabile che contiene tutto il testo contenuto nella pagina web che sto analizzando con il web driver di selenium
    cerca_indicatore_numero_pagine = html.find('class="pageNum last taLnk')#dico a selenium di cercare una stringa perche' questa sta sempre vicina all'indicazione del numero di pagine mostrate nei risultati. Non cercare direttamente il numero di pagine perche' ovviemante cambia ogni volta ma questa dicitura rimane fissa in tutte le ricerche
    dati_con_numero_pagine_totali = html[cerca_indicatore_numero_pagine:]#seleziono la parte di testo hatml che sta dopo la ul testo che ho cercato nel comando precedente, cosi' facendo verra' selezionato anche il numero che indica in numero di pagine
    inizio_numero_pagine = dati_con_numero_pagine_totali.find('>')#cerco nel il carattere immediatamente precedente a cio' che indica il numero delle pagine in modo da delimitare la futura area di ricerca di esso
    fine_numero_pagine = dati_con_numero_pagine_totali.find('<')#cerco nel il carattere immediatamente successivo a cio' che indica il numero delle pagine in modo da delimitare la futura area di ricerca di esso
    numero_pagine = dati_con_numero_pagine_totali[inizio_numero_pagine+1:fine_numero_pagine]#la ricerca del numero viene ripulita da possibili altri caratteri trovati
    numero_pagine_intero = int(numero_pagine)#il numero della pagina viene convertito da stringa ad intero
    for i in range (0,numero_pagine_intero):#viene creato un ciclo che scorrera' le varie pagine e verra' ripetuto tante volte quanto sono il numero dell pagine
        conto = i * 30#l'indice del ciclo viene incrementato sempre di una unita' e successivamente moltiplicato per 30
        conto_stringa = str(conto)#il risultato viene convertito in stringa
        mark1 = url.find("oa")#viene cercata la posizione di queste due lettere contenute nell'url
        url_part2 = url[mark1:]#seleziono una parte dell'url in questione
        mark2_part = url_part2.find("-")#cerco all'interno della seconda parte un carattere che serve per far cambiare la pagina dei risultati in modon da trovarli tutti
        mark2 = mark2_part + mark1#sommo la posizione di questo carattere all'interno della seconda parte dell'url al numero dei caratteri della prima parte in modo tale da ottenerne la sua posizione all'interno dell'intero url, tutta questa operazione e' stata fatta perche' il carattere che delimita la parte finale dell'area di ricerca compare all'interno dell'url ripetuto,per trovare quello giusto e' necessario quindi dividere l'url in due parti in modo da selezionare quello che serve
        url2 = url[0:mark1+2]+conto_stringa+url[mark2:]#viene aggiunto "conto_stringa" al centro di queste due ricerche nell'url, questo perche' ogni volta che viene cambiata pagina tripadvisor aumenta di trenta un numero che si trova in mezzo al link, cosi' facendo io glielo faccio aumentare  manualmente
        pagine.append(url2)#aggiungo alla lista le pagine dei risultati
    driver.service.process.send_signal(signal.SIGTERM)#alla fine del ciclo chiudo PhantomJS con questo speciale comando
    return pagine#restituisco i link di tutte le pagine della ricerca

def dati_hotel(lista_con_duplicati, pagine_ricerca):#definisco la funzione che estrapolera' i dati dalle strutture fornitegli attraverso la funzione precedente ovvero "crea_lista"
    lista = []#creo una lista vuota che verra' usata per rimuovere i duplicati dalla originale, data come unico argomento alla funzione
    for j in lista_con_duplicati:#con questo ciclo aggiungo elementi alla lista nuova lista scartando i duplicati che si erano generati dalle sponsorizzazioni nei risultati di ricerca ovvero alcune strutture comparivano piu' volte
        if j not in lista:
            lista.append(j)
    now = datetime.today().strftime("20%y-%m-%d %H:%M:%S")#definisco una variabile che successivamente stampera' quando e' stato eseguito il programma, e di conseguenza, a quando appartengono i risultati
    driver = webdriver.PhantomJS()#carico il web driver che verra' assegnato a selenium
    mydb = mysql.connector.connect(#attraverso questo comando fornisco le credenziali a python per accedere e comunicare con il database sul quale verranno salvati i risultati
      host="localhost",
      user="phpmyadmin",
      passwd="qazxswedc1",
      database="tripadvisor",
    )
    mycursor = mydb.cursor()#comando che mi permettera' di operare modifiche al database
    for i in range(0, len(lista)) :#creo un ciclo che scorrera' tutta la lista che contiene i link delle varie strutture, senza duplicati
        driver.get(lista[i])#come sopra
        html = driver.page_source#come sopra
        driver.get(lista[i])#come sopra
        id = lista[i][49:57]#l'identificativo della struttura e' indicato nel link, in questo comando viene selezionato
        id_solo_numeri = aggiusta_id(id)#elimino attraverso una funzione specifica, la possibile presenza di caratteri non utili alla definizione dell'identificativo
        cerca_titolo = html.find('class="ui_header h1"')#cerco il nome della struttura
        titolo = html[cerca_titolo:cerca_titolo+200]#come sopra con ulteriore precisione
        titolo_aggiustato = aggiusta_titolo(titolo)#elimino attraverso una funzione specifica, la possibile presenza di caratteri non utili alla definizione del nome della struttura
        cerca_numero_recensioni = html.find('reviewCount">')#cerco il numero delle recensioni
        numero_recensioni = html[cerca_numero_recensioni:cerca_numero_recensioni+200]#definisco gli estremi di ricerca
        numero_recensioni_aggiustato = aggiusta_numero_recensioni(numero_recensioni)#elimino attraverso una funzione specifica, la possibile presenza di caratteri non utili alla definizione del nome del numero delle recensioni
        cerca_mappa = html.find('_pin.png|')#vedi sopra
        mappa_da_aggiustare = html[cerca_mappa+9:cerca_mappa+27]#vedi sopra
        mappa = aggiusta_mappa(mappa_da_aggiustare)#rimuovo eventuali caratteri superflui dalle coordinate della struttura
        lati = ottieni_latitudine(mappa)#seleziono dalle coordinate solamente la latitudine
        longi = ottieni_longitudine(mappa)#seleziono dalle coordinate solamente la longitudine
        cerca_punteggio = html.find('Punteggio ')#cerco il punteggio della struttura
        punteggio = html[cerca_punteggio+7:cerca_punteggio+15]#definisco gli estremi di ricerca
        punteggio_aggiustato = aggiusta_punteggio(punteggio)#con una funzione specifica su lavora la stringa in modo tale che venga mostrato solo il numero corrispondente al punteggio
        cerca_numero_stelle = html.find('ui_star_rating star_')#cerco la posizione dove mi e' indicato il numero di stelle
        numero_stelle = html[cerca_numero_stelle+20:cerca_numero_stelle+22]#assegno la posizione che contiene il numero di stelle ad una variabile che poi faro' uscire nei risultati
        numero_stelle_aggiustato = aggiusta_numero_stelle(numero_stelle)#attraverso una funzione specifica rimuovo caratteri superflui dal risultato della ricerca del sumero di stelle
        inizio_lista_servizi = html.find('Servizi della struttura')#cerco l'inizio della sezione che contiene i servizi della struttura
        lista_servizi_senza_fine = html[inizio_lista_servizi:]#seleziono la parte del testo che contiene tutti i servizi che la struttura possiede
        fine_lista_servizi = lista_servizi_senza_fine.find('</div></div></div>')#cerco la fine della sezione che contiene i servizi della struttura
        servizi_totali1 = lista_servizi_senza_fine[:fine_lista_servizi]#seleziono la sezione che contiene i servizi della struttura
        servizi_disponibili = aggiusta_servizi1(servizi_totali1)#attraverso una funzione specifica rimuovo caratteri superflui dal risultato della ricerca dei servizi di una struttura
        if inizio_lista_servizi == -1:#nel caso in cui non si trovasse la lista dei servizi allora si deve ricorre a cercarla in una maniera differente, questo capita in maniera casuale
            inizio_lista_servizi2 = html.find('SERVIZI DELL\'HOTEL')#cerco l'inizio della sezione che contiene i servizi della struttura
            lista_servizi_senza_fine2 = html[inizio_lista_servizi2:]#seleziono la parte del testo che contiene tutti i servizi che la struttura possiede
            fine_lista_servizi2 = lista_servizi_senza_fine2.find('</div></div></div>')#cerco la fine della sezione che contiene i servizi della struttura
            servizi_totali2 = lista_servizi_senza_fine2[:fine_lista_servizi2+1]#seleziono la sezione che contiene i servizi della struttura
            servizi_disponibili = aggiusta_servizi2(servizi_totali2)#attraverso una funzione specifica rimuovo caratteri superflui dal risultato della ricerca dei servizi di una struttura
#stampo i risultati per avere una conferma visiva del funzionamento del programma
        print (id_solo_numeri, titolo_aggiustato, lati, longi, now, numero_recensioni_aggiustato, punteggio_aggiustato, numero_stelle_aggiustato, lista[i], servizi_disponibili)
        mycursor.execute("SELECT ID FROM strutture")#dico a python di selezionare il campo ID dalla tabella strutture
        myresult = mycursor.fetchall()#creo una variabile alla quale assegnero' un comando che mostra il contenuto di una tabella
        id_strutture = []#creo una lista vuota
        for x in myresult:#con questo ciclo aggiungo alla mia lista tutti gli id contenuti nella tabella "strutture"
            id_strutture.append(x)
        id_strutture_stringa = ' '.join(str(x) for x in id_strutture)#trasformo la lista in una stringa in modo da poterci effetuare ricerche, cosi' facendo posso capire se una struttura e' gia' inclusa nel mio database oppure no
        if id_strutture_stringa.find(id_solo_numeri) == -1:#con questa condizione controllo se la strutture che ho trovato e' gia' presente o meno nel mio database, se non ne fa parte vengono aggiunti i dati
            sql1 = "INSERT INTO strutture (ID, Nome_Struttura, Lat, Lon, Stelle, Link) VALUES (%s, %s, %s, %s, %s, %s)"#inserisco i dati nel database
            val1 = (id_solo_numeri, titolo_aggiustato, lati, longi, numero_stelle_aggiustato, lista[i])#come sopra
            mycursor.execute(sql1, val1)#come sopra
            print(mycursor.rowcount, "Nuovo record inserito nella tabella 'strutture'")#stampo i risultati per avere una conferma visiva del funzionamento del programma
        if lati != "":#nel caso in cui nel database esistesse una struttura con lo stesso identificativo di quella che ho trovato e dovessero essere assenti le sue coordinate geografiche allora queste vengono aggiornate, ovviemnte cio' succede solo se le coordinatedella strutture trovata sono presenti
            sql2 = "UPDATE strutture SET Lat = %s WHERE ID = %s"#come sopra
            val2 = (lati, id_solo_numeri)#come sopra
            mycursor.execute(sql2, val2)#come sopra
            sql3 = "UPDATE strutture SET Lon = %s WHERE ID = %s"#come sopra
            val3 = (longi, id_solo_numeri)#come sopra
            mycursor.execute(sql3, val3)#come sopra
            print("Record modfificato nella tabella 'strutture'")#stampo i risultati per avere una conferma visiva del funzionamento del programma
        sql4 = "INSERT INTO informazioni (Data, Media_Recensioni, Numero_Recensioni, ID, Servizi) VALUES (%s, %s, %s, %s, %s)"#inserisco i dati nel database all'interno della tabella "informazioni"
        val4 = ( now, punteggio_aggiustato, numero_recensioni_aggiustato, id_solo_numeri, ', '.join(servizi_disponibili))#come sopra
        mycursor.execute(sql4, val4)#come sopra
        print(mycursor.rowcount, "Nuovo record inserito nella tabella 'informazioni'")#stampo i risultati per avere una conferma visiva del funzionamento del programma
        mydb.commit()#applico le modifiche al database
    driver.service.process.send_signal(signal.SIGTERM)#alla fine del ciclo chiudo PhantomJS con questo speciale comando
#in questa parte del programma inserisco i prezzi e i provider degli stessi all'interno del database. Per fare cio' devo utilizzare "Chromedriver" il quale a differenza di "Phnatomjs" riesce a comunicare con sito web in questione e cio' mi e' necessario per conoscere il prezzo delle strutture in un determinato periodo a mia scelta. Non ho utilizzato questo driver sin dal principio perche' dopo un certo numero di richieste il sito web tripadvisor blocca la connessione, cosa che al contrario non succede con "PhantomJS". Riesco a fare un numero limitato di richieste perche' per conioscere il prezzo migliore di una struttura non serve accedere alla pagina dedicata di una certa struttura queste informazioni sono presenti anche nella pagina che mostra i risultati#carico "Chromedriver"
    for i in range(0, len(pagine_ricerca)):#creo un ciclo che scorrera' tutta la lista che contiene i link delle pagine di ricerca
        browser = webdriver.Chrome()#carico "Chromedriver"
        browser.get(pagine_ricerca[i])#assegno a Chromedriver la pagina di ricerca, la quale scorrera' e fara' si che lavori su tutte le pagine di ricerca
        sleep(20)#attendo che la pagina venga caricata completamente
        html = browser.page_source#assegno il codice html della pagina in questione a questa variabile
        if html.find('rsdc-prev rsdc-nav ui_icon single-chevron-left rsdc-inactive') == -1:#questa condizione verificha che il pulsante per scorrere i mesi verso il presente sia disabilitato o meno, se non  lo e' lo preme, questo perche' a me interessano i risultati del giorno stesso della ricerca e se ci si trova a 2 settimane dalla fine del mese tripadvisor automaticamente ti mostrera' la selezione della data di arrivo per il mese successivo. Quindi grazie  a questo comando posso tornare indietro al mese attuale
            browser.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div[2]/div[2]').click()#clicco su questo pulsante
            sleep(20)#attendo che tripadvisor carichi la mia richiesta e mi mostri il mese attuale
        html2 = browser.page_source#assegno il codice html della pagina in questione a questa variabile il quale potrebbe essere cambiato se la condizione precedente si fosse verificata
        parte1 = html2.find('rsdc-cell rsdc-day rsdc-disabled')#per riuscire a selezionare la data odierna all'interno del calendario del sito, devo analizzare il codice html della parte del calendario del sito Tripadvisor in modo tale da poter inserire correttamente da data odierna
        now2 = str(now)#per riuscire a selezionare la data odierna trasformo il formato orario di python in quello di tripadvisor e lo faccio in 3 passaggi: nel primo lo faccio diventare una stringa, nel secodo lo trasformo attraverso una funzione e nel terzo lo ricerco all'interno del codice html del sito
        now2_aggiustato = aggiusta_data(now2)#vedi sopra
        parte2 = html2.find(now2_aggiustato)#vedi sopra
        parte = html2[parte1:parte2]#seleziono l'area di testo entro la qule ricercare le caselle dei giorni della sezione del calendario del sito
        conto = parte.count('rsdc-cell rsdc-day rsdc-disabled')#conto il numero dei giorni passati del mese corrente in modo da determinare la casella giusta da selezionare ovvero quella odierna
        conto_finale = int(conto)+3#a seconda dei meccanismi interni del sito tripadvisor ci sono due possibilita' di visulizzazione del calendario. Esse mostrano il calendario in manera uguale ma la sua truttura cambia leggermente a livello di codice html, percio' sara' necessario creare 4 variabili necessarie per impostare il giorno odierno e successivo nel primo (conto_finale, conto_finale2) caso ed il giorno odierno e successivo per il secondo caso (conto_finale3, conto_finale4) ed infine tranformo questi in formato stringa
        conto_finale3 = int(conto)+3#vedi sopra
        conto_finale_stringa = str(conto_finale)#vedi sopra
        conto_finale_stringa3 = str(conto_finale3)#vedi sopra
#imposto il percorso xpath delle caselle che rappresentano una il giorno odierno e l'altra del successivo, ne creo altre due perche' e' possibile che il sito tripadvisorcambi la sua struttura interna, quindi grazie a queste altre due variabili riesco a contrastare l'eventuale cambiamento del sito il quale avviene in modo totalmente casuale
        inizio_giorni = '//*[@id=\"BODY_BLOCK_JQUERY_REFLOW\"]/span/div[3]/div/div[2]/div[3]/span[1]/span['+ conto_finale_stringa +']'
        inizio_giorni_stringa = str(inizio_giorni)
        inizio_giorni2 = '//*[@id=\"BODY_BLOCK_JQUERY_REFLOW\"]/span/div[3]/div/div[2]/div[3]/span[1]/div['+ conto_finale_stringa3 +']'
        inizio_giorni_stringa2 = str(inizio_giorni2)
#provo quale dei due metodi di ricerca e' efficace e lo applico, per ulteriori dettagli vedi il commento precedente
        try:
            browser.find_element_by_xpath(inizio_giorni_stringa).click()
        #    print (inizio_giorni_stringa)
        except:
            browser.find_element_by_xpath(inizio_giorni_stringa2).click()
        #    print (inizio_giorni_stringa2)
        sleep(20)#attendo il caricamento della pagina con i risultati impostati alla data odierna
        html3 = browser.page_source#assegno il codice html della pagina in questione a questa variabile, il quale e' cambiato al causa del mio cambiamento di data
        inizio_strutture = html3.find('bodycon_main')#ricerco all'interno del codice html l'inizio della sezione dove sono mostrate le strutture
        fine_strutture = html3.find('disclaimer  ui_section')#ricerco all'interno del codice html la fine della sezione dove sono mostrate le strutture
        strutture = html3[inizio_strutture:fine_strutture]#seleziono il codice html dove si trovano i dati in merito alle strutture
        ind = ''.join(c for c in strutture if c not in '"')#per facilitare la ricerca dei risultati elimino dal testo il carattere dei doppi apici i quali potrebbero essere fonte di errore per il programma
        index = [i for i in range(len(ind)) if ind.startswith('<a target=_blank href=', i)]#seleziono tutte le singole caselle della ricerca dove sono contenute le informazioni relative alle strutture
        for i in range(0, len(index)):#creo un ciclo che scorre tutte le singole caselle della ricerca dove sono contenute le informazioni relative alle strutture
            part1 =  ind[index[i]:]#grazie al ciclo seleziono di volta in volta la parte iniziale della casella della struttura, man mano che scorre arrivera' a lavorare su tutte le strutture  della pagina
            end1 = part1.find("id=property_")#devo ottenere l'dentificativo della strutura e questo e' contenuto all'interno del link di essa all'interno della pagina coi risultati. L parte iniziale del link corrisponde alla variabile "part1" e invece con questa variabile sto ricercando la parte finale
            link_struttura = (part1[+17:end1]).replace("href=","https://www.tripadvisor.it")#sostituisco la parte iniziale del link ottenuto con un'altra che rendera' il mio link funzionante
            seleziona_id_struttura = link_struttura[49:57]#estrapolo l'identificativo della strutture dal link di essa
            id_struttura_pulito = aggiusta_id(seleziona_id_struttura)#attraverso una funzione specifica rimuovo caratteri superflui dalla definizione dell'identificativo della struttura
            part2 = part1.find('<div class=price __resizeWatch data-sizegroup=mini-meta-price data-clickpart=chevron_price data-index=0>')#ricerco all'interno del codice html la stringa immediatamente successiva alla definizione del prezzo
            end2 = part1.find('div class=provider __resizeWatch')#ricerco all'interno del codice html la stringa immediatamente precedente alla definizione del prezzo
            prezzo = part1[part2+104:end2-13]#seleziono la parte di codice html dove e' contenuto il prezzo in evidenza della struttura in questione
            prezzo_aggiustato = ''.join(i for i in prezzo if i.isdigit())#rimuovo eventuali caratteri superflui dalla definizione del prezzo
            part3 = part1.find('provider_logo')#ricerco all'interno del codice html la stringa immediatamente precedente alla definizione del provider
            end3 = part1.find('<span class=provider_text>')#ricerco all'interno del codice html la stringa immediatamente successiva alla definizione del provider
            provider = part1[part3+18:end3-3]#seleziono la parte di codice html dove e' contenuto il prezzo in evidenza della struttura in questione
            mycursor = mydb.cursor()#comando che mi permettera' di operare modifiche al database
            if part3 == -1:#condizione che verifica se e' stato effettivamente trovato un prezzo e un provider per una determinata strutura, questo puo' verificarsi perche' tripadvisor mostra anche le strutture non disponibili al momento
                provider = None
                prezzo_aggiustato = None
#stampo i risultati per avere una conferma visiva del funzionamento del programma
            print(provider)
            print()
            print(prezzo_aggiustato)
            print()
            print(id_struttura_pulito)
            sql5 = "UPDATE informazioni SET Provider = %s  WHERE ID = %s and Data=%s"#aggiorno la tabella "informazioni" dove l'dentificativo della struttura e la data e ora della scansione coincidono
            val5 = (provider, id_struttura_pulito, now)#vedi sopra
            mycursor.execute(sql5, val5)#vedi sopra
            sql6 = "UPDATE informazioni SET Prezzo = %s  WHERE ID = %s and Data=%s"#aggiorno la tabella "informazioni" dove l'dentificativo della struttura e la data e ora della scansione coincidono
            val6 = (prezzo_aggiustato, id_struttura_pulito, now)#vedi sopra
            mycursor.execute(sql6, val6)#vedi sopra
        browser.quit()#chiudo il processo del driver "Chromedriver"
        mydb.commit()#applico le modifiche al database

def ottieni_id_citta(i):#seleziona l'identificativo della citta' prendendo in input il link della struttura
    return i[40:47]

def aggiusta_id(cod):#con questa funzione rimuovo possibili caratteri superflui dell'identificativo della struttura
    a = ''.join(i for i in cod if i.isdigit())#con questo comando si elimina qualsiasi carattere eccetto i numeri
    return a

def aggiusta_titolo(tit):#con questa funzione rimuovo possibili caratteri superflui dal titolo della struttura
    mark1 = tit.find("header")#Delimito l'area di ricerca
    mark2 = tit.find("</h1>")
    return tit[mark1+11:mark2]#Restituisco solo la parte della stringa contenente il titolo della struttura

def aggiusta_numero_recensioni(num):#con questa funzione rimuovo possibili caratteri superflui dal numero di recensioni della struttura
    mark2 = num.find("recensioni")
    a = num[13:mark2-1]
    a = ''.join(i for i in a if i.isdigit())#con questo comando si elimina qualsiasi carattere eccetto i numeri
    return a

def aggiusta_prezzi(pre):#con questa funzione rimuovo possibili caratteri superflui dal prezzo  della struttura
    mark1 = pre.find(">")
    mark2 = pre.find("</div>")
    a = pre[mark1+1:mark2]
    a = ''.join(i for i in a if i.isdigit())#con questo comando si elimina qualsiasi carattere eccetto i numeri
    return a

def aggiusta_punteggio(punt):#con questa funzione rimuovo possibili caratteri superflui dal punteggio della struttura
    mark1 = punt.find("o")
    mark2 = punt.find("su")
    a = punt[mark1+1:mark2]
    return a

def aggiusta_provider(pro):#con questa funzione rimuovo possibili caratteri superflui dal provider della struttura
    mark1 = pro.find("alt=")
    mark2 = pro.find(">")
    return pro[mark1+4:mark2]

def aggiusta_servizi1(ser):#questa funzione serve a selezionare da una porzione di testo html, i vari servizi che una struttura possiede
    a = ''.join(c for c in ser if c not in '"')
    lista = []
    index = [i for i in range(len(a)) if a.startswith('hotels-hotel-review-about-with-photos-Amenity__name--SRjUW>', i)]
    for i in range(0, len(index)):
        part =  a[index[i]+59:index[i]+200]
        end = part.find("<")
        lista.append(part[:end])
    return lista

def aggiusta_servizi2(ser):#questa funzione serve a selezionare da una porzione di testo html, i vari servizi che una struttura possiede, si differenzia da quella sopra perche' questa funzione viene utilizzare qual'ora venga casualmento modificata la modalita' di visulizzazione dei risultati da parte del sito "Tripadvisor"
    a = ''.join(c for c in ser if c not in '"')
    lista = []
    index = [i for i in range(len(a)) if a.startswith('<div class=textitem data-prwidget-name=text data-prwidget-init=>', i)]
    for i in range(0, len(index)):
        part =  a[index[i]+64:index[i]+200]
        end = part.find("<")
        lista.append(part[:end])
    return lista

def aggiusta_mappa(map):#con questa funzione rimuovo possibili caratteri superflui dalle coordinate geografiche della struttura
    a = ''.join(c for c in map if c not in '"')
    b = ''.join(c for c in a if c not in '>')
    return b

def ottieni_latitudine(map):#A partire dalle coordinate geografiche seleziono solo la latitudine
    mark1 = map.find(",")
    if mark1 == -1:
        return ""
    a = map[0:mark1]
    b = ''.join(c for c in a if c not in ',')
    return b


def ottieni_longitudine(map):#A partire dalle coordinate geografiche seleziono solo la longitudine
    mark1 = map.find(",")
    if mark1 == -1:
        return ""
    a = map[mark1:]
    b = ''.join(c for c in a if c not in ',')
    return b


def aggiusta_numero_stelle(ste):#con questa funzione rimuovo possibili caratteri superflui dal numero di stelle della struttura
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

def aggiusta_data(tem):#questa funzione serve a generare una stringa che indica la data in maniera che sia identica alla stessa cge compare all'interno del codice html del sito "www.tripadvisor.com". Questo mi e' utile per operare sull'evento che permette di selezionare la data odierna all'interno del selezionatore fornito sempre dallo stesso.
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


# Creo 4 variabili alle quali assogno ciascuna il link della prima pagina di risultati di un deetrminato luogo, a partire da questo link potro' ottenere tutte le informazioni che mi servono

lucca = 'https://www.tripadvisor.it/Hotels-g187898-oa00-Lucca_Province_of_Lucca_Tuscany-Hotels.html'
livorno = 'https://www.tripadvisor.it/Hotels-g187897-oa00-Livorno_Province_of_Livorno_Tuscany-Hotels.html'
cascina= 'https://www.tripadvisor.it/Hotels-g793691-oa00-Cascina_Province_of_Pisa_Tuscany-Hotels.html'
pietrasanta = 'https://www.tripadvisor.it/Hotels-g1016839-oa00-Pietrasanta_Province_of_Lucca_Tuscany-Hotels.html'

# Per cascun luogo sempre a partire dal link del primo risultato di ricerca, eseguo una funzione che mi restituira' tutti i link delle singole strutture ed un'alrea funzione che invece restituira' tutti i link delle varie pagine di ricerca. Assegno questi dati a due variabili che a loro volta verranno date come argomanti della funzione dati hotel, la quale grazie a questi dati trovera tutti i dati sulle strutture (ulteriori dettagli sono forniti come commento all'interno della stessa funzione sempre all'interno di questo testo)

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
