#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
  apt-get update -y
  apt upgrade -y
  apt install -y php apache2 mariadb-server php-mysqli php-gd libapache2-mod-php git
  
  mkdir /var/www
  mkdir /var/www/html
  cd /var/www/html
  git clone https://github.com/digininja/DVWA.git
  cd /var/www/html/DVWA/config
  cp config.inc.php.dist config.inc.php

  cat << EOF > /var/www/html/DVWA/config/scripts.sql
create database dvwa;
create user dvwa@localhost identified by 'p@ssw0rd';
grant all on dvwa.* to dvwa@localhost;
flush privileges;
EOF
  mysql --execute 'tee session.out; source /var/www/html/DVWA/config/scripts.sql;'
  echo "Hello from user-data!"