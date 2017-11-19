apt-get update
apt-get -y install python3 python3-pip python3-dev
apt-get -y install postgresql postgresql-contrib libpq-dev git
pip3 install --upgrade pip

sudo -i -u postgres

psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE USER lumos WITH PASSWORD 'lumos';
    CREATE DATABASE lumos;
    GRANT ALL PRIVILEGES ON DATABASE lumos TO lumos;
EOSQL

## Load tables

git pull
cd

pip3 install -r requirements.txt

