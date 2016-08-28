<?php
$sOutputFile = 'email_1.txt';
include_once('simple_html_dom.php');

$sTargetUrl = 'https://github.com/luciankahn/queers-without-hacks';

$sTargetUrl .= '?page=';
$oHtml = new simple_html_dom();

$iNum = 1;

while(url_exists($sTargetUrl . $iNum))
{
    $oHtml->load_file($sTargetUrl . $iNum);

    foreach($oHtml->find('span[class=css-truncate css-truncate-target] a') as $oProfile)
    {
        $rProfile = file_get_contents('https://github.com' . $oProfile->href);

        if(preg_match_all('/[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+.[a-zA-Z]{2,4}/', $rProfile, $aMatches)) {
            foreach ($aMatches[0] as $sEmail) {
                file_put_contents($sOutputFile, trim($sEmail) . PHP_EOL, FILE_APPEND);
            }
        }
    }
    $iNum++;
    sleep(5); // Github doesn't like too many request in a short time
}

    /* Remove duplicates */
    $aEmails = file($sOutputFile);
    $aEmails = array_unique($aEmails);
    file_put_contents($sOutputFile, implode('', $aEmails));

 echo 'Done!<br /> Total email got: ' . $iNum;

function url_exists($sUrl)
{
    return file_get_contents($sUrl);
}
