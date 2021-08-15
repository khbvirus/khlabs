#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
  apt-get update -y
  apt upgrade -y
  apt install -y php apache2 mariadb-server php-mysqli php-gd libapache2-mod-php git awscli jq
  
  mkdir /var/www
  mkdir /var/www/html
  cd /var/www/html
  git clone https://github.com/digininja/DVWA.git
  cd /var/www/html/DVWA/config
  # cp config.inc.php.dist config.inc.php

  cat << "EOF" > /var/www/html/DVWA/config/config.inc.php.origin
<?php

# If you are having problems connecting to the MySQL database and all of the variables below are correct
# try changing the 'db_server' variable from localhost to 127.0.0.1. Fixes a problem due to sockets.
#   Thanks to @digininja for the fix.

# Database management system to use
$DBMS = 'MySQL';
#$DBMS = 'PGSQL'; // Currently disabled

# Database variables
#   WARNING: The database specified under db_database WILL BE ENTIRELY DELETED during setup.
#   Please use a database dedicated to DVWA.
#
# If you are using MariaDB then you cannot use root, you must use create a dedicated DVWA user.
#   See README.md for more information on this.
$_DVWA = array();
$_DVWA[ 'db_server' ]   = '127.0.0.1';
$_DVWA[ 'db_database' ] = 'dvwa';
$_DVWA[ 'db_user' ]     = 'dvwa';
$_DVWA[ 'db_password' ] = '##db_secret##';
$_DVWA[ 'db_port'] = '3306';

# ReCAPTCHA settings
#   Used for the 'Insecure CAPTCHA' module
#   You'll need to generate your own keys at: https://www.google.com/recaptcha/admin
$_DVWA[ 'recaptcha_public_key' ]  = '';
$_DVWA[ 'recaptcha_private_key' ] = '';

# Default security level
#   Default value for the security level with each session.
#   The default is 'impossible'. You may wish to set this to either 'low', 'medium', 'high' or impossible'.
$_DVWA[ 'default_security_level' ] = 'low';

# Default PHPIDS status
#   PHPIDS status with each session.
#   The default is 'disabled'. You can set this to be either 'enabled' or 'disabled'.
$_DVWA[ 'default_phpids_level' ] = 'disabled';

# Verbose PHPIDS messages
#   Enabling this will show why the WAF blocked the request on the blocked request.
#   The default is 'disabled'. You can set this to be either 'true' or 'false'.
$_DVWA[ 'default_phpids_verbose' ] = 'false';

# Default locale
#   Default locale for the help page shown with each session.
#   The default is 'en'. You may wish to set this to either 'en' or 'zh'.
$_DVWA[ 'default_locale' ] = 'en';

?>
EOF

  # aws secretsmanager get-secret-value --secret-id dvwa-db-admin-credentials/admin-password --version-stage AWSCURRENT
  db_secret=$(aws secretsmanager get-secret-value --secret-id dvwa-db-admin-credentials/admin-password --version-stage AWSCURRENT --region eu-west-1 | jq .SecretString | grep -Po "(?<=password\\\\\":\\\\\").*(?=\\\\\",\\\\\"username)")
  echo $db_secret
  cat << EOF > /var/www/html/DVWA/config/scripts.sql
create database dvwa;
create user dvwa@localhost identified by '##db_secret##';
grant all on dvwa.* to dvwa@localhost;
flush privileges;
EOF
  sed "s/##db_secret##/$db_secret/g" /var/www/html/DVWA/config/scripts.sql >> /var/www/html/DVWA/config/scripts_final.sql
  sed "s/##db_secret##/$db_secret/g" /var/www/html/DVWA/config/config.inc.php.origin >> /var/www/html/DVWA/config/config.inc.php
  mysql --execute 'tee session.out; source /var/www/html/DVWA/config/scripts_final.sql;'

  chmod 757 /var/www/html/DVWA/hackable/uploads
  chmod 757 /var/www/html/DVWA/config
  chmod 646 /var/www/html/DVWA/external/phpids/0.6/lib/IDS/tmp/phpids_log.txt

  sed -i "s/allow_url_include = Off/allow_url_include = On/g" /etc/php/7.4/apache2/php.ini
  systemctl restart apache2

  echo "Hello from user-data!"