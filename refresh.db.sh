#!/bin/bash
mysql -uroot -p<< eof
drop database if exists odl_app_backend;
CREATE DATABASE odl_app_backend DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
eof
python ./manage.py syncdb