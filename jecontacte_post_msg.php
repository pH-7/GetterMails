<?php
include('PH7Client.php');
use PH7\External\Http\Client\PH7Client;

$sUrl = 'http://www.jecontacte.com/';
$sReauest1 = 'editercompte.php';
$sRequest2 = 'envoyer.php?type=message&dest=mayamaya2015&source=profil';
$sUser = 'mamoooo';
$sPass = '123456';
$sBody = 'ffff';
$sTitle = 'ffffffffff';

$oPH7CMSApi = new PH7Client($sUrl);

/***** Log a user *****/
$aLogin = [
        'pseudo' => $sUser,
        'motdepasse' => $sPass,
        'logging_in' => 1
       ];

// Login the user
$oPH7CMSApi->post($sReauest1, $aLogin)->send();


$aMsg = [
  'dest' => 'mayamaya2015',
  'action'=> 'message',
  'source' => 'profile',
  'pasted' => 0,
  'publier' => 1,
  'message' => 'Salut! Comment ca va? Tu parrais super symapa. Tiens, je suis souvent sur coolonweb.com (car ici il y a trop de vieux). Est-ce que tu es dessus, si oui, on peut se partager les pseudos :)',
];

// Send Msg
$oPH7CMSApi->post($sRequest2, $aMsg)->setHeader(false)->send();

echo $oPH7CMSApi->getResponse();
