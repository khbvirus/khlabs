#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
  yum -y update
  yum install -y httpd24 php72 mysql57-server php72-mysqlnd
  cat /etc/system-release
  service httpd start
  chkconfig httpd on
  chkconfig --list httpd
  echo "Hello from user-data!"