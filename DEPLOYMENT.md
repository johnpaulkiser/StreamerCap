

shipping deployment checklist:
[ ] debug = false





Set up ec2 instance
set up rds postgres

make python virtual environment
download repo from git
install dependencies in venv

change add host to /etc/hosts
add ec2 ip to allowed hosts in settings.py

install apache2
install wsgi for apache2
make new apache config streamercap.conf in /etc/apache2/sitesavailable

enable site `sudo a2ensite streamercap.conf`

restart apache2 deamon -> service apache2 restart






