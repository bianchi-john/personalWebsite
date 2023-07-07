//Sript per lapagina html "servizi.html"




$(document).ready(function () {
  prendiServizi();
})



function prendiServizi() {
  var a1 = 0;
  var b1 = 0;

  var a2 = 0;
  var b2 = 0;
  var c2 = 0;

  var a3 = 0;
  var b3 = 0;
  var c3 = 0;

  var a4 = 0;
  var b4 = 0;
  var c4 = 0;

  var a5 = 0;
  var b5 = 0;
  var c5 = 0;

  var arrayContenitoreServiziTutti = [];
  var arrayContenitoreServiziLucca = []
  var arrayContenitoreServiziCascina = []
  var arrayContenitoreServiziLivorno = []
  var arrayContenitoreServiziPietrasanta = []

  var objServizi = {};
  var objNumeroServiziLucca = {};
  var objNumeroServiziCascina = {};
  var objNumeroServiziLivorno = {};
  var objNumeroServiziPietrasanta = {};
  var objNumeroServizi = {};
  var tableData = [];


  var modal = document.getElementById('myModal');
  var btn = document.getElementById("myBtn");
  var span = document.getElementsByClassName("close")[0];


  $.getJSON('api/getServizi.php', function (data) {////TUTTI I SERVIZI///////////////
    for (var i in data)//Scorro tutti gli elementi del file
    {
      a1 = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
      var b1 = a1.split(", ");
      for (var k in b1)//creo un ciclo che mi scorre tutti gli elemnti di "c"
      {
        if (b1[k] != "Nessun Servizio") {
          arrayContenitoreServiziTutti.push(b1[k]);//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
        }
      }
    }
    var arrayContenitoreServiziUnici = arrayContenitoreServiziTutti.filter(onlyUnique);
    //////////////LUCCA///////////////////
    for (var i in data)//Scorro tutti gli elementi del file
    {
      if (data[i].luogo == 'Lucca') {
        a2 = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
        var b2 = a2.split(", ");
        c2++;// questa variabile mi e' utile per fare confronti tra le varie citta' varie citta
        for (var k in b2)//creo un ciclo che mi scorre tutti gli elemnti di "c"
        {
          arrayContenitoreServiziLucca.push(b2[k]);//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
        }
      }
    }
    ////////////////////////////////////////
    //////////////CASCINA///////////////////
    for (var i in data)//Scorro tutti gli elementi del file
    {
      if (data[i].luogo == 'Cascina') {
        a3 = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
        var b3 = a3.split(", ");
        c3++;// questa variabile mi e' utile per fare confronti tra le varie citta' varie citta
        for (var k in b3)//creo un ciclo che mi scorre tutti gli elemnti di "c"
        {
          arrayContenitoreServiziCascina.push(b3[k]);//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
        }
      }
    }
    ////////////////////////////////////////
    //////////////LIVORNO///////////////////
    for (var i in data)//Scorro tutti gli elementi del file
    {
      if (data[i].luogo == 'Livorno') {
        a4 = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
        var b4 = a4.split(", ");
        c4++;// questa variabile mi e' utile per fare confronti tra le varie citta' varie citta
        for (var k in b4)//creo un ciclo che mi scorre tutti gli elemnti di "c"
        {
          arrayContenitoreServiziLivorno.push(b4[k]);//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
        }
      }
    }

    ////////////////////////////////////////
    //////////////PIETRASANTA///////////////////
    for (var i in data)//Scorro tutti gli elementi del file
    {
      if (data[i].luogo == 'Pietrasanta') {
        a5 = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
        var b5 = a5.split(", ");
        c5++;// questa variabile mi e' utile per fare confronti tra le varie citta' varie citta
        for (var k in b5)//creo un ciclo che mi scorre tutti gli elemnti di "c"
        {
          arrayContenitoreServiziPietrasanta.push(b5[k]);//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
        }
      }
    }
    ///////////////////////////////////////
    ////////////LUCCA/////////////////////
    for (var i = 0; i < arrayContenitoreServiziTutti.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziLucca[arrayContenitoreServiziTutti[i]] = 0;//viene creata una chiave che ha per nome quell'elemnto e come valore 1
    }
    for (var i = 0; i < arrayContenitoreServiziLucca.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziLucca[arrayContenitoreServiziLucca[i]]++;
    }
    ////////////////////////////////////
    ////////////CASCINA/////////////////////
    for (var i = 0; i < arrayContenitoreServiziTutti.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziCascina[arrayContenitoreServiziTutti[i]] = 0;//viene creata una chiave che ha per nome quell'elemnto e come valore 1
    }
    for (var i = 0; i < arrayContenitoreServiziCascina.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziCascina[arrayContenitoreServiziCascina[i]]++;
    }
    ////////////////////////////////////
    ////////////LIVORNO/////////////////////
    for (var i = 0; i < arrayContenitoreServiziTutti.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziLivorno[arrayContenitoreServiziTutti[i]] = 0;//viene creata una chiave che ha per nome quell'elemnto e come valore 1
    }
    for (var i = 0; i < arrayContenitoreServiziLivorno.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziLivorno[arrayContenitoreServiziLivorno[i]]++;
    }
    ////////////////////////////////////
    ////////////PIETRASANTA/////////////////////
    for (var i = 0; i < arrayContenitoreServiziTutti.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziPietrasanta[arrayContenitoreServiziTutti[i]] = 0;//viene creata una chiave che ha per nome quell'elemnto e come valore 1
    }
    for (var i = 0; i < arrayContenitoreServiziPietrasanta.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      objNumeroServiziPietrasanta[arrayContenitoreServiziPietrasanta[i]]++;
    }
    /////////////////////////////////////////////////////
    ////////////////////////////////////////////////////
    for (var i = 0; i < arrayContenitoreServiziUnici.length; i++)//per fare cio' devo scorrere tutti gli elementi dell'array che contiene i servizi della citta' in questione
    {
      tableData.push({ Nome_Servizio: arrayContenitoreServiziUnici[i], Lucca: (objNumeroServiziLucca[arrayContenitoreServiziUnici[i]] / c2 * 100).toFixed(1), Cascina: (objNumeroServiziCascina[arrayContenitoreServiziUnici[i]] / c3 * 100).toFixed(1), Livorno: (objNumeroServiziLivorno[arrayContenitoreServiziUnici[i]] / c4 * 100).toFixed(1), Pietrasanta: (objNumeroServiziPietrasanta[arrayContenitoreServiziUnici[i]] / c5 * 100).toFixed(1) })
    }
    // var tableData = [objServizi]
    var table = new Tabulator("#tabellaServizi", {
      data: tableData, //set initial table data
      layout: "fitDataFill",
      columns: [
        {
          title: "Nome Servizio", field: "Nome_Servizio", sorter: "string", cellClick: function (e, cell) {
            // alert("The cell has a value of:" + cell.getValue());
            $.getJSON('api/getServizi.php', function (data) {
              var struttureAventiServizio = [];
              var a = 0;
              var b = 0;
              for (var i in data)//Scorro tutti gli elementi del file
              {
                a = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
                var b = a.split(", ");
                for (var k in b)//creo un ciclo che mi scorre tutti gli elemnti di "c"
                {
                  if (cell.getValue() == b[k]) {
                    struttureAventiServizio.push({ Nome_Struttura: data[i].Nome_Struttura, Link: data[i].Link, Luogo: data[i].luogo });
                  };//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
                };
              };
              // var arrayContenitoreServiziUnici = arrayContenitoreServiziTutti.filter( onlyUnique );
              // alert(struttureAventiServizio.filter( onlyUnique ));
              struttureAventiServizio = (multiDimensionalUnique(struttureAventiServizio));
              modal.style.display = "block";
              // document.getElementById("contenuto").innerHTML = multiDimensionalUnique(struttureAventiServizio);
              var table2 = new Tabulator("#struttureServizi", {
                height: "311px",
                data: struttureAventiServizio, //set initial table data
                columns: [
                  { title: "Nome Struttura", field: "Nome_Struttura", sorter: "string" },
                  { title: "Luogo", field: "Luogo", sorter: "string" },
                  { title: "Link", field: "Link", formatter: "link", formatterParams: { label: "Link" } },
                ],
              });
              span.onclick = function () {
                modal.style.display = "none";
              }
              window.onclick = function (event) {
                if (event.target == modal) {
                  modal.style.display = "none";
                }
              }
              // Get the modal
            })
          }
        },
        {
          title: "Lucca", field: "Lucca", sorter: "number", cellClick: function (e, cell) {
            // alert("The cell has a value of:" + cell.getValue());
            $.getJSON('api/getServiziLuogo.php?luogo=Lucca', function (data) {
              var struttureAventiServizio = [];
              var a = 0;
              var b = 0;
              for (var i in data)//Scorro tutti gli elementi del file
              {
                a = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
                var b = a.split(", ");
                for (var k in b)//creo un ciclo che mi scorre tutti gli elemnti di "c"
                {
                  if ((cell.getRow().getData().Nome_Servizio) == b[k]) {
                    struttureAventiServizio.push({ Nome_Struttura: data[i].Nome_Struttura, Link: data[i].Link, Luogo: data[i].luogo });
                  };//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
                };
              };
              // var arrayContenitoreServiziUnici = arrayContenitoreServiziTutti.filter( onlyUnique );
              // alert(struttureAventiServizio.filter( onlyUnique ));
              struttureAventiServizio = (multiDimensionalUnique(struttureAventiServizio));
              modal.style.display = "block";
              // document.getElementById("contenuto").innerHTML = multiDimensionalUnique(struttureAventiServizio);
              var table2 = new Tabulator("#struttureServizi", {
                height: "311px",
                data: struttureAventiServizio, //set initial table data
                columns: [
                  { title: "Nome Struttura", field: "Nome_Struttura", sorter: "string" },
                  { title: "Luogo", field: "Luogo", sorter: "string" },
                  { title: "Link", field: "Link", formatter: "link", formatterParams: { label: "Link" } },
                ],
              });
              span.onclick = function () {
                modal.style.display = "none";
              }
              window.onclick = function (event) {
                if (event.target == modal) {
                  modal.style.display = "none";
                }
              }
              // Get the modal
            })
          }
        },
        {
          title: "Livorno", field: "Livorno", sorter: "number", cellClick: function (e, cell) {
            // alert("The cell has a value of:" + cell.getValue());
            $.getJSON('api/getServiziLuogo.php?luogo=' + "Livorno", function (data) {
              var struttureAventiServizio = [];
              var a = 0;
              var b = 0;
              for (var i in data)//Scorro tutti gli elementi del file
              {
                a = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
                var b = a.split(", ");
                for (var k in b)//creo un ciclo che mi scorre tutti gli elemnti di "c"
                {
                  if ((cell.getRow().getData().Nome_Servizio) == b[k]) {
                    struttureAventiServizio.push({ Nome_Struttura: data[i].Nome_Struttura, Link: data[i].Link, Luogo: data[i].luogo });
                  };//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
                };
              };
              // var arrayContenitoreServiziUnici = arrayContenitoreServiziTutti.filter( onlyUnique );
              // alert(struttureAventiServizio.filter( onlyUnique ));
              struttureAventiServizio = (multiDimensionalUnique(struttureAventiServizio));
              modal.style.display = "block";
              // document.getElementById("contenuto").innerHTML = multiDimensionalUnique(struttureAventiServizio);
              var table2 = new Tabulator("#struttureServizi", {
                height: "311px",
                data: struttureAventiServizio, //set initial table data
                columns: [
                  { title: "Nome Struttura", field: "Nome_Struttura", sorter: "string" },
                  { title: "Luogo", field: "Luogo", sorter: "string" },
                  { title: "Link", field: "Link", formatter: "link", formatterParams: { label: "Link" } },
                ],
              });
              span.onclick = function () {
                modal.style.display = "none";
              }
              window.onclick = function (event) {
                if (event.target == modal) {
                  modal.style.display = "none";
                }
              }
              // Get the modal
            })
          }
        },
        {
          title: "Cascina", field: "Cascina", sorter: "number", cellClick: function (e, cell) {
            // alert("The cell has a value of:" + cell.getValue());
            $.getJSON('api/getServiziLuogo.php?luogo=' + "Cascina", function (data) {
              var struttureAventiServizio = [];
              var a = 0;
              var b = 0;
              for (var i in data)//Scorro tutti gli elementi del file
              {
                a = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
                var b = a.split(", ");
                for (var k in b)//creo un ciclo che mi scorre tutti gli elemnti di "c"
                {
                  if ((cell.getRow().getData().Nome_Servizio) == b[k]) {
                    struttureAventiServizio.push({ Nome_Struttura: data[i].Nome_Struttura, Link: data[i].Link, Luogo: data[i].luogo });
                  };//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
                };
              };
              // var arrayContenitoreServiziUnici = arrayContenitoreServiziTutti.filter( onlyUnique );
              // alert(struttureAventiServizio.filter( onlyUnique ));
              struttureAventiServizio = (multiDimensionalUnique(struttureAventiServizio));
              modal.style.display = "block";
              // document.getElementById("contenuto").innerHTML = multiDimensionalUnique(struttureAventiServizio);
              var table2 = new Tabulator("#struttureServizi", {
                height: "311px",
                data: struttureAventiServizio, //set initial table data
                columns: [
                  { title: "Nome Struttura", field: "Nome_Struttura", sorter: "string" },
                  { title: "Luogo", field: "Luogo", sorter: "string" },
                  { title: "Link", field: "Link", formatter: "link", formatterParams: { label: "Link" } },
                ],
              });
              span.onclick = function () {
                modal.style.display = "none";
              }
              window.onclick = function (event) {
                if (event.target == modal) {
                  modal.style.display = "none";
                }
              }
              // Get the modal
            })
          }
        },
        {
          title: "Pietrasanta", field: "Pietrasanta", sorter: "number", cellClick: function (e, cell) {
            // alert("The cell has a value of:" + cell.getValue());
            $.getJSON('api/getServiziLuogo.php?luogo=' + "Pietrasanta", function (data) {
              var struttureAventiServizio = [];
              var a = 0;
              var b = 0;
              for (var i in data)//Scorro tutti gli elementi del file
              {
                a = data[i].Servizi;//assegno alla variable "a" la lista dei servizi
                var b = a.split(", ");
                for (var k in b)//creo un ciclo che mi scorre tutti gli elemnti di "c"
                {
                  if ((cell.getRow().getData().Nome_Servizio) == b[k]) {
                    struttureAventiServizio.push({ Nome_Struttura: data[i].Nome_Struttura, Link: data[i].Link, Luogo: data[i].luogo });
                  };//finalemnte aggiungo i servizi ad un array in modo tale da poterci operare senza intoppi
                };
              };
              // var arrayContenitoreServiziUnici = arrayContenitoreServiziTutti.filter( onlyUnique );
              // alert(struttureAventiServizio.filter( onlyUnique ));
              struttureAventiServizio = (multiDimensionalUnique(struttureAventiServizio));
              modal.style.display = "block";
              // document.getElementById("contenuto").innerHTML = multiDimensionalUnique(struttureAventiServizio);
              var table2 = new Tabulator("#struttureServizi", {
                height: "311px",
                data: struttureAventiServizio, //set initial table data
                columns: [
                  { title: "Nome Struttura", field: "Nome_Struttura", sorter: "string" },
                  { title: "Luogo", field: "Luogo", sorter: "string" },
                  { title: "Link", field: "Link", formatter: "link", formatterParams: { label: "Link" } },
                ],
              });
              span.onclick = function () {
                modal.style.display = "none";
              }
              window.onclick = function (event) {
                if (event.target == modal) {
                  modal.style.display = "none";
                }
              }
              // Get the modal
            })
          }
        },
      ],
    });
  })
}

function multiDimensionalUnique(arr) {
  var uniques = [];
  var itemsFound = {};
  for (var i = 0, l = arr.length; i < l; i++) {
    var stringified = JSON.stringify(arr[i]);
    if (itemsFound[stringified]) { continue; }
    uniques.push(arr[i]);
    itemsFound[stringified] = true;
  }
  return uniques;
}



function onlyUnique(value, index, self) {
  return self.indexOf(value) === index;
}
