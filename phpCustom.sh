#!/bin/bash
set -e

# PHP Custom setup script
# Jared Loosli
# avantidevelopment.com
#
# Inspired by 
# Stephen Wood
# www.heystephenwood.com
# 
# Usage: $ sudo ./phpCustom.sh
#
# Net install:
#   $ curl https://raw.githubusercontent.com/jloosli/mybin/master/phpCustom.sh | sudo sh

# Must be run as root
if [[ `whoami` != "root" ]]
then
  echo "This install must be run as root or with sudo."
  exit
fi

# Add packages/mods that need to be installed here
apt-get install -y php5-curl
cat - > /etc/php5/fpm/conf.d/10-custom.ini <<PHP5CONF
; 10-custom.ini 
; PHP custom settings
; By Jared Loosli http://avantidevelopment.com 
 
; Set Path
include_path = ".:/usr/share/php:/var/www/cakephp/lib:/usr/bin"
post_max_size = 2G
upload_max_filesize = 2G

PHP5CONF

service php5-fpm restart

echo 'Installation complete. Enjoy!'