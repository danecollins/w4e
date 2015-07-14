#!/bin/bash -l

source ~/env/w4e/bin/activate
source ~/dropbox/osx/env_vars/w4e_vars

DATE=`date +%Y-%m-%d`
backup_file=/Users/dane/dropbox/dacxl/TrackPlaces/backups/heroku_w4e.$DATE

pg_dump --dbname=$HPG_PROD_DBNAME --host=$HPG_PROD_HOST --username=$HPG_PROD_UNAME -F c -f $backup_file

