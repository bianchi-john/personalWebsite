<?php

function esegui_query($sql, $campi)
{
	include('../api/config.php');
	$risultato = select($db,$sql);

	$return = array();
	for($i = 0; $i < count($risultato); $i++)
	{
		foreach($campi as $chiave => $formato)
		{
			if(isset($risultato[$i][$chiave]))
				$risultato[$i][$chiave] = $formato($risultato[$i][$chiave]);
		}
		$return[] = $risultato[$i];
	}

	closeDB($db);

	return json_encode($return);

}
?>
