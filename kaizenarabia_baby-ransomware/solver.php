<?php 

$cipher = mcrypt_module_open('twofish','','ecb','');
$counter = 0;
while(1){
    $key = "keykey".$counter;
    $key = str_pad($key,  16, "1");
    $iv = hex2bin('00000000000000000000000000000000');
    $encrypted = hex2bin("61D1D33C8FCF28D6E3FF8ED3AB1D006D");
    $decrypted = mcrypt_decrypt('twofish', $key, $encrypted, 'ecb', $iv);
    if (strpos($decrypted, 'bank') !== false){
          printf("KEY : %s Decrypted text: %s (%s)\n",$key,$decrypted,bin2hex($decrypted));
          break;
    }

    $counter += 1;
}

?>
