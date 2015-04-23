## project_name: odl_app_backend
**ODL bootcamp 2015**

for a web app to controller mininet and call odl rest api.

#### how to deploy：
	apt-get update
	apt-get install libjpeg-dev libfreetype6-dev libssl-dev
	apt-get install python2.7 python2.7-dev python-pip libmysqlclient-dev -y
	apt-get install mysql-server -y
  pip install -r requirements.txt

#### refresh db
  sh refresh.db.sh
#### run
  python manage.py runserver
  
