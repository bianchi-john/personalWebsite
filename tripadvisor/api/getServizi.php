<?php
  include('../php/funzioni.php');
  header("Content-Type: application/json");

      $sql = "SELECT Servizi, informazioni.ID, Data,luogo,Nome_Struttura,Link FROM informazioni JOIN strutture ON informazioni.ID = strutture.ID  ORDER BY informazioni.ID";
      $campi = array("ID" => "intval");
      echo esegui_query($sql,$campi);

?>
