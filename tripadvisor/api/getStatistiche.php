<?php
  include('../php/funzioni.php');
  header("Content-Type: application/json");

  if (isset($_GET['luogo']))
  {
    $luogo = $_GET['luogo'];
      $sql = "SELECT Provider, Prezzo, Data, Media_Recensioni, Numero_Recensioni, strutture.Link, informazioni.ID, Stelle FROM informazioni JOIN strutture ON informazioni.ID = strutture.ID WHERE luogo = '$luogo' ORDER BY informazioni.Data";
      $campi = array("Prezzo" => "intval", "Media_Recensioni" => "floatval", "Numero_Recensioni" => "intval", "ID" => "intval","Stelle" =>"intval");
      echo esegui_query($sql,$campi);
   }

?>
