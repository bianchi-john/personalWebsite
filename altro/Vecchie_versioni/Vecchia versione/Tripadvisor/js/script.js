//Sript per lapagina html "index.html"



var map; //mappa
var citta; //variabile che contiene la città cliccata nell'input
var markers = []; //coordinate geografiche delle strutture

//Icone dei merker personalizzati per città
var iconLu = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"; //LUCCA
var iconLi = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_blue.png"; //LIVORNO
var iconPi = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_orange.png"; //PIETRASANTA
var iconCa = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_green.png";//CASCINA

//Variabile che permettera' di generare la tabella contenentela media prezzo delle trutture nel codice HTML
var varibialeRiempiTabella;
//

//Invoco la funzione che inizializza tutte le altre e si avvia automaticamente al caricamento della pagina
$(document).ready(function () {
  prendiLatLon();//funzione che gestisce il funzionamento della mappa
  datiIstat();//Funzione che grazie alla libreria di Highcharts mostra i dati forniti dal seguente link: http://www.regione.toscana.it/statistiche/dati-statistici/turismo
  $(function() {//Funzione che permette di scorrere la pagina verso il basso se si clicca su di un determinato pulsante
   $('.scroll-down').click (function() {
     $('html, body').animate({scrollTop: $('section.ok').offset().top }, 'slow');
     return false;
   });
 });
  map = new google.maps.Map(document.getElementById("mappa"),{//Dichiaro che la mappa fornita da google dovra' essere generta sull'elemnto che ha come id "mappa" all'interno del codice html
    zoom: 8,
    center : {lat: 43.6614100, lng: 10.6306700},
  })
})

//funzione che gestisce il funzionamento della mappa
function prendiLatLon()
{
    $('input').change(function ()//Tutte le volte che nel codice html un elemento di tipo "input" subisce un cambiamento allora si verifica il codice sottostante
    {
        if ($(this).prop('checked')==true)//se l'elemento input risulta avere la spunta presente allora verra' eseguito il codice sottotante
        {
            citta = this.value;//La variabile "citta" prendera' come valore il valore assegnato all'elemento di tipo input nel codice html che in questo caso e' stato impostato con il nome della citta' associata al bottone che l'utente ha selezionato
            prendiStrutture(citta);//viene avviata la funzione "prendiStrutture" con paramentro il nome della citta' selezionata dal'utente
            $('#tabs').show();//Viene rimosso l'attributo "nascosto" dalla tabella
            $('#tab'+citta).show();//Creo un elemento html con id "tab" unito al nome della citta' in questione che, grazie all'attributo "show" appare e scompare a seconda dello stato della checkbox
            $('#periodo').show();//Viene rimosso l'attributo "nascosto" dalla tabella
            $('#informazioniTabella').show();//Viene rimosso l'attributo "nascosto" dal titolo della tabella
        }
        else //che e' equivalente a "if ($(this).prop('checked')==false)" ovvero se l'elemento di tipo input risulta deselezionato
        {
          citta = this.value; //prende il valore della città deselezionata
          $('#tab'+citta).hide();//Creo un elemento html con id "tab" unito al nome della citta' in questione che, grazie all'attributo "toggle" appare e scompare a seconda dello stato della checkbox
          for(var j in markers) //scorre l'array contenente tutti i marker posizionati
          {
            //mi permette di eliminare i marker che non sono stati deselezionati
            if(markers[j].city == citta)//city e' una parola chiave di google
            {
              markers[j].setMap(null);//i marker della citta' selezionata vengono rimossi
            }
          }
        }

    })
}

//questa funzione si avvia quando viene selezionata una città (checked == TRUE)
function prendiStrutture(citta)
{//Eseguo una chiamata ajax dove indico il parametro "luogo" grazie all'argomento della funzione
    $.getJSON('api/getStrutture.php?luogo='+citta, function (data)//a seconda del luogo selezioanto decido la tipologia di icone per i marker
    {
      if(citta == "Cascina")
      {
          icon = iconCa;
      }
      if(citta == "Livorno")
      {
          icon = iconLi;
      }
      if(citta == "Lucca")
      {
          icon = iconLu;
      }
      if(citta == "Pietrasanta")
      {
          icon = iconPi;
      }
        for(var i in data )
        {//ciclo che scorre tutti gli elementi della chiamata ajax, ovvero tutte le informazioni relative alle strutture di una determinata citta'
          myLatLon =//imposto la latitudine e longitudine
          {
            lat: data[i].Lat,
            lng: data[i].Lon
          }
          //creo l'oggetto marker della mappa di google
          marker = new google.maps.Marker({
            position : myLatLon,
            map : map,
            title :data[i].Nome_Struttura,
            icon : icon,
            link : data[i].Link,
            //il contenuto sara' la variabile "informazioneMarker" che contiene tutti i dati delle strutture, dichiarata a riga 560
            idMarker : data[i].ID,
            city : citta
          });
          //inserisco i marker dentro l'array markers man mano che vengono creati perche' qui siamo ancora dentro al for
          markers.push(marker);

          //creo un evento che si attivera' ogni volta che clicchero' su di un marker, cio' attivera' una funzione
          google.maps.event.addListener(marker,'click',function ()
          {
            $("#testo").empty();//prendo nell'html il tag che ha come id "testo" e lo svuoto
            $("#testo").html(this.content);//Riempio questo elemento con il contenuto della variabile "marker"
            avviaGrafico(this.idMarker,this.title,citta,this.link);//Funzione che ogni qualvolta si clicca su di un marker si potra' consultare l'andamento dei prezzi della struttura in questione all'interno di una finestra modale
          })
        }
        creaTabella(citta);
    })
}

//fuozione che permette di inserire i dati nella tabella creata dalla funzione "prendiLatLon"
function creaTabella(citta)
{
  //creo variabili che mi serviranno per ottenere prezzo e punteggio medio delle 4 aree in questione
    var contaPrezzi = 0;
    var contaMedieRecensioni = 0;
    var prezzoTOT = 0;
    var punteggioTOT = 0;
    var numeroStrutture = [];
    $.getJSON('api/getStatistiche.php?luogo='+citta, function (data)//eseguo una chiamata ajax per trovare tutti i dati che mi servono relativi l prezzo e media recensioni di una determinata citta'
    {
      for(var i in data)
      {
          if (data[i].Prezzo != null)//condizione necessaria per non considerare i luoghi che hanno un prezzo nullo
          {
            prezzoTOT += data[i].Prezzo;
            contaPrezzi++;
          }
          if (data[i].Media_Recensioni != null)//condizione necessaria per non considerare i luoghi che hanno una media recensioni nulla
          {
            punteggioTOT += data[i].Media_Recensioni;
            contaMedieRecensioni++;
          }
          numeroStrutture.push(data[i].Link)
      }//alla variabile "varibialeRiempiTabella" assegno codice html unito ai dati che mi indicano media recensionie prezzo dell'area in questione
      varibialeRiempiTabella = "<tr id='tab"+citta+"'><td>"+citta+"</td><td>"+(prezzoTOT/contaPrezzi).toFixed(2)+"</td><td>"+(punteggioTOT/contaMedieRecensioni).toFixed(2)+"</td><td>"+(numeroStrutture.filter(onlyUnique)).length+"</td></tr>";
      //genero la tabella all'interno della pagina html, sovrascrivendo il precedente attributo dell'elemento html con id "tabs" di "hidden" in modo tale da rendere invisibile la tabella fin tanto che non si facciano generare questi dati
      $("#tab"+citta).replaceWith(varibialeRiempiTabella);
    })
}


function avviaGrafico(valore, nome, luogo, link)//Funzione che ogni qualvolta si clicca su di un marker si potra' consultare l'andamento dei prezzi della struttura in questione all'interno di una finestra modale
{
  var contenitoreDate = [];//creo un array che conterra' le date di analisi
  var contenitorePrezzi = [];//creo un array che conterra' tutti i prezzi che sono stati analizzati in una determinata struttura
  var modal = document.getElementById('myModal');//creo una variabile alla quale assegno l'elemento html con id "myModal"
  var span = document.getElementsByClassName("close")[0];//creo una variabile alla quale assegno l'elemento html con classe  "close"
  modal.style.display = "block";//Assegno all'elementohtml con id "modal" lo stile di visualizzazione "block"
  document.getElementById("titolo_struttura").innerHTML ="<a href="+link+">"+nome+"</a>"
  // document.getElementById("link_struttura").innerHTML = link;//Assegno all'elemento html che ha come id "titolo_struttura" la variabile "nome"
  span.onclick = function() {//se si clicca sulla variabile span il suo stile di visualizzazione cambia diventando invisibile
  modal.style.display = "none";
  }
  //comando che serve a chiudere la finestra modale ogni qualvolta si clicchi al di fuori di essa
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
  $.getJSON('api/getStatistiche.php?luogo='+luogo, function (data)//chiamata ajax per ricavare le informazioni dei prezi e date alla singola struttura in questione
  {
    for(var i in data)//scorro tutti gli elementi
    {
      if(valore == data[i].ID && data[i].Prezzo != null)//se la variabile "valore" ovvero l'ID della struttura selezionata e' uguale all'id contenuto nell'elemento del file "getStatistiche.php" che sto scorrendo e il prezzo non e' nullo, allora:
      {//aggiungi all'array "contenitoreDate" il valore "data[i].Data"  e ripeti per "contenitorePrezzi" con il valore "data[i].Prezzo"
        contenitoreDate.push(data[i].Data);
        contenitorePrezzi.push(data[i].Prezzo);
      }

    }//variabili utili per la creazione del grafico con la libreria "Highcharts"
    var option = {
      chart: {
        renderTo: 'grafico',
        type: 'line',
        width: 950,
      },
      title: {
        text: 'Andamento Prezzi'
      },
      yAxis: {
        title: {
          text: 'Andamento Prezzi in €'
        }
      },
      xAxis: {
        categories: data[i].Data
      },
      series: [{}]
    }
    for (var j in contenitoreDate)
    {
      option.series[0].data = contenitorePrezzi;
      option.series[0].name = "Prezzo";
      option.xAxis.categories =  contenitoreDate;
    }//Creo una variabile alla quale assegno la creazione di un grafico con la libreria "highcharts" che ha come parametri, i parametri espressi nella variabile "option"
    var chart = new Highcharts.Chart(option);
  })
}



////////////////////////////////////////////////

//Funzione che grazie alla libreria di Highcharts mostra i dati forniti dal seguente link: http://www.regione.toscana.it/statistiche/dati-statistici/turismo
function datiIstat()
{
  //Imposto tutti i parametri che serviranno a generare la tabella
          Highcharts.chart('ViaRegioneToscana', {
              data: {//i dati che questo grafico mostrera' verranno forniti dalla tabella presente nel codice html con id "numeriPersone" la quale a sua volte non verra' mostrata (grazie ad un attributo a libello di stile) ma servira' appunto solo per forire dati al grafico in questione
                  table: 'numeriPersone'
              },
              chart: {
                  type: 'column',
                  height: (9 / 17  * 100) + '%' // Conferisce alla tabella un aspetto di 16:9
              },
              title: {
                  text: '<a href="http://www.regione.toscana.it/statistiche/dati-statistici/turismo">Movimento turistico per comune e provenienza - 2017 Via Regione Toscana</a>'
              },
              yAxis: {
                  allowDecimals: false,
                  title: {
                      text: 'Numero di persone'
                  }
              },
              tooltip: {
                  formatter: function () {
                      return '<b>' + this.series.name + '</b><br/>' +
                          this.point.y + ' ' + this.point.name.toLowerCase();
                  }
              }
          });
}


///Funzione che permette di eliminare gli elementi duplicati di un array
function onlyUnique(value, index, self) {
return self.indexOf(value) === index;
}
