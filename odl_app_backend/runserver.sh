#!/bin/bash
git pull
sudo ./refresh.db.sh
sudo mn -c
sudo python manage.py runserver 192.168.255.7:8000
