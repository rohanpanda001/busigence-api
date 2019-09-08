
## git clone

Clone the repo

## pip install -r requirements.txt 

Install all the dependencies

## mysql -u root

Start mysql server 

## Set up Database

CREATE DATABASE busigence;

## Load Data into tables
LOAD DATA LOCAL INFILE './customers.csv' 
INTO TABLE customers 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE './orders.csv' 
INTO TABLE orders 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

## python app.py

Open another terminal
Run it on localhost
 
 
