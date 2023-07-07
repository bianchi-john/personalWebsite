<?php
  include('../php/funzioni.php');
  header("Content-Type: application/json");

  if (isset($_GET['luogo']))
  {
    $luogo = $_GET['luogo'];
      $sql = "SELECT Servizi, informazioni.ID, Data,luogo,Nome_Struttura,Link FROM informazioni JOIN strutture ON informazioni.ID = strutture.ID WHERE luogo = '$luogo' ORDER BY informazioni.ID";
      $campi = array("ID" => "intval");
      echo esegui_query($sql,$campi);
   }
?>
