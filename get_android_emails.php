<?php
@set_time_limit(0);
@ini_set('memory_limit', '528M');

$sOutputFile = 'email_android.txt';
include_once('simple_html_dom.php');

$sTargetUrl = 'https://play.google.com/store/apps/new?hl=en';

$oHtml = new simple_html_dom;


    $oHtml->load_file($sTargetUrl);

    foreach($oHtml->find('div[class=card-content id-track-click id-track-impression] a') as $oPage)
    {
        $rPage = file_get_contents('https://play.google.com' . $oPage->href);

        if(preg_match_all('/[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+.[a-zA-Z]{2,4}/', $rPage, $aMatches)) {
            foreach ($aMatches[0] as $sEmail) {
                file_put_contents($sOutputFile, trim($sEmail) . PHP_EOL, FILE_APPEND);
            }
        }
    }

    /* Remove duplicates */
    $aEmails = file($sOutputFile);
    $aEmails = array_unique($aEmails);
    file_put_contents($sOutputFile, implode('', $aEmails));
