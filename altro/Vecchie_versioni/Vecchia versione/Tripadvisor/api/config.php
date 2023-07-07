<?php
//includo la libreria "dblibrary.php" che fornira' le funzioni per interagire con il database

include('../libraries/dbLibrary.php');
//inizializzo le 4 variabili che andranno nella funzione "openDB" che sono le credenziali per acecdere al databasein questione ovvero "tripadvisor"
$database = "my_johnbianchi";
$username="johnbianchi";

$db = openDB($database,$username);
?>
