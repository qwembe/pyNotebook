#!/bin/bash

docker container run \
        --name sql-maria \
        -e MYSQL_ROOT_PASSWORD=12345 \
        -e MYSQL_USER=username \
        -e MYSQL_PASSWORD=12345 \
        -e MYSQL_DATABASE=dbname \
        -p 3306:3306 \
        -d mariadb:10.4