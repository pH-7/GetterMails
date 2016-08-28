<?php
include('PH7Client.php');
use PH7\External\Http\Client\PH7Client;

$sUrl = 'http://demo.hizup.com/pH2Date/';
$sReauest1 = 'user/login/';
$sRequest2 = 'user/message_box/ticklishpeacock430';
$sUser = 'demo@ph2date.com';
$sPass = 'ph2date';
$sBody = 'Hi are you well';
$sTitle = 'ffffffffff';

$oPH7CMSApi = new PH7Client($sUrl);

/***** Log a user *****/
$aLogin = [
        'identity' => $sUser,
        'password' => $sPass,
        'remember' => 'on',
        'submit' => 'Login'
       ];

// Login the user
$oPH7CMSApi->post($sReauest1, $aLogin)->send();
// Send message
$oPH7CMSApi->post($sRequest2, ['message' => $sBody])->setHeader(false)->send();

echo $oPH7CMSApi->getResponse();
echo 'ok';

