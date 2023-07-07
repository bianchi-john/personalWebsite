<?php
//includo il file "funzioni.php" che mi consente di accedere al database
include '../php/funzioni.php';
//dichiaro che verra' utilizzato un formato di tipo "JSON"
header("Content-Type: application/json");

if (isset($_GET['luogo']))
{
  $citta = $_GET['luogo'];
  //variabile che al suo interno contiene una stringa espressa in formato sql dove vengono richiesti determinati campi al database
  $sql = "SELECT * FROM strutture WHERE luogo like '$citta' ORDER BY ID";
  //creo un array associativo dove trasformo il valore di due campi risultati dalla precedente query in formato "floatval" ovvero decimale
  $campi = array("Lat" => "floatval", "Lon" => "floatval");
  //assegno queste due variabili alla funzione "esegui_query"
  echo esegui_query($sql,$campi);
}

?>
