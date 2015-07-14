#!/bin/bash -l

cd ~/src/w4e
echo -n "*** W4E daily script ***" >> ~/daily.log
date >> ~/daily.log
source ~/env/w4e/bin/activate

scripts/backup_prod.sh
curl http://watch4.events/checkin/9YZNCBAR/ > /dev/null

echo dropping database
dropdb w4e_prod >> ~/daily.log 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: could not drop database" 
    echo "ERROR: could not drop database" >> ~/daily.log
fi

echo pulling data from heroku
heroku pg:pull DATABASE w4e_prod --app w4e >> ~/daily.log 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: heroku pull failed"
    echo "ERROR: heroku pull failed" >> ~/daily.log
    exit 1
fi

echo "INFO: heroku pull completed" >> ~/daily.log
export DATABASE_URL=postgres:///w4e_prod
scripts/dbsummary.py >> ~/daily.log 2>&1

echo -n "*** end W4E daily script **************************************" >> ~/daily.log


