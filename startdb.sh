#!/bin/bash


source conf.sh

docker container run \
        --name sql-maria \
        -e MYSQL_ROOT_PASSWORD=$Password \
        -e MYSQL_USER=$UserName \
        -e MYSQL_PASSWORD=$Password \
        -e MYSQL_DATABASE=$DatabaseName \
        -p 3306:$Port \
        -d mariadb:10.4

hash -r 2>/dev/null