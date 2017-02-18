<?php
@set_time_limit(0);
@ini_set('memory_limit', '528M');

$sOutputFile = 'log_email_github.txt';
require 'vendor/autoload.php';
require 'vendor/swiftmailer/swiftmailer/lib/swift_required.php';
require 'simple_html_dom.php';


/***** TODO: Replace these following values in Yaml config file and use Symfony package to read it easily *****/
$sTargetUrl = 'https://github.com/opensource-socialnetwork/opensource-socialnetwork/stargazers';
$sTargetUrl .= '?page=';

/** Gmail Email account **/
$sName = 'Pierre';
$sEmail = 'myemail@gmail.com';
$sEmailPwd = 'mypwd';

$oHtml = new simple_html_dom;

$iNum = 1;

while(url_exists($sTargetUrl . $iNum))
{
    $oHtml->load_file($sTargetUrl . $iNum);

    foreach($oHtml->find('span[class=css-truncate css-truncate-target] a') as $oProfile)
    {
       $oHtml->load_file('https://github.com' . $oProfile->href);

       if ($oHtml->find('a[class=email]',0) && trim(explode('@', $oHtml->find('a[class=email]', 0)->innertext)[1])
           != 'buddyexpress.net' && trim($oHtml->find('a[class=email]',0)->innertext) != 'me@koen.pt')
       {
           if($oName = $oHtml->find('title', 0)) {
               $aName = explode(' ', $oName->innertext);
               $sName = str_replace(array('(', ')'), '', ucfirst($aName[1]));
        } else {
            $sName = '';
        }

        $sBody = file_get_contents('Emails/msg_ph7cms_github_to_send.txt');
        $sBody = str_replace('[name]', (!empty($sName) ? $sName : 'there') . '!', $sBody);
        $sBody = str_replace('[end_name]', (!empty($sName) ? ' ' . $sName : ''), $sBody);
        $sBody = str_replace('[day]', get_day(), $sBody);
        $sEmail = trim($oHtml->find('a[class=email]',0)->innertext);
                                                    // 587
        $oTransport = Swift_SmtpTransport::newInstance('smtp.gmail.com', 465, 'ssl')->setUsername($sEmail)->setPassword($sEmailPwd);
        $oMailer = Swift_Mailer::newInstance($oTransport);
        $oMessage = Swift_Message::newInstance('I need your help... ;)')->setFrom(array($sEmail => $sName))->setTo(array($sEmail))->setBody($sBody, 'text/html');
        $oMailer->send($oMessage);

        // Set log
       file_put_contents($sOutputFile, $sEmail . ' - ' . $sName . PHP_EOL . $sBody . PHP_EOL . PHP_EOL . PHP_EOL, FILE_APPEND);

   }
    }
    $iNum++;
    sleep(5); // Github doesn't like too many request in a short time
}

    /* Remove duplicates */
    $aEmails = file($sOutputFile);
    $aEmails = array_unique($aEmails);
    file_put_contents($sOutputFile, implode('', $aEmails));

 echo 'Done!';

function url_exists($sUrl)
{
    return file_get_contents($sUrl);
    /*
    $headers = @get_headers($sUrl);
    return (strpos($headers[0],'200')===true);
    * */
}

function get_day()
{
    switch (date('D'))
    {
        case 'Mon':
            $sDay = 'Monday';
        break;

        case 'Tue':
            $sDay = 'Tuesday';
        break;

        case 'Wed':
            $sDay = 'Wednesday';
        break;

        case 'Thu':
            $sDay = 'Thursday';
        break;

        case 'Fri':
            $sDay = 'Friday';
        break;

        case 'Sat':
            $sDay = 'Saturday';
        break;

        case 'Sun':
            $sDay = 'Sunday';
        break;

        default:
            $sDay = 'day';
    }
    return $sDay;
}
