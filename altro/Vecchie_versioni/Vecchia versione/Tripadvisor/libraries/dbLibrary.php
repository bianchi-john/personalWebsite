<?php

/******************************
 * Open a Connection to MySQL *
 ******************************/
function openDB($database="my_johnbianchi", $password=NULL, $username="johnbianchi"){
	// Create connection
	$conn = mysqli_connect($servername, $username, $password, $database);
	if (!$conn) die("dbLibrary: errore di connessione: " . mysqli_connect_error($conn));
	
	/* change character set to utf8 */
	if (!mysqli_set_charset($conn, "utf8"))	printf("Error loading character set utf8: %s\n", mysqli_error($conn));

	return $conn;
}

/******************************
 * Lettura dei records        *
 ******************************/
function select($conn,$sql,$err=0){
	// Esecuzione query
	$resultSet = mysqli_query($conn, $sql);
	if(!$resultSet){
		if($err==0) print("dbLibrary: Errore esecuzione $sql:" . mysqli_error($conn));
		return null;
	}
	else{
		// Copio i records in un array associativo
		$records=array();
		while ($record = mysqli_fetch_assoc($resultSet)) $records[]=$record;
		
		// Liberazione della memoria impegnata dal result set
		mysqli_free_result($resultSet);
		
		return $records;
	}
}

/*******************************
 * ESECUZIONE di un comando sql*
 *******************************/
function sql($conn,$sql,$err=0){
	if($err==3) print($sql);
	// Esecuzione query
	$resultSet = mysqli_query($conn, $sql);
	if(!$resultSet){
		if($err==0) print("dbLibrary: Errore esecuzione $sql:" . mysqli_error($conn));
		return(-1);
	}
	else return(1);
}

/******************************
 * Close the Connection to MySQL *
 ******************************/
 function closeDB ($conn){
	mysqli_close($conn);
}

?>