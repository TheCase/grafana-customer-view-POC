#!/usr/bin/env python

import csv
import pymysql.cursors
import sys
import time

from pprint import pprint

if len(sys.argv) < 2:
    print "Usage: {0} <csv_file>".format(sys.argv[0])
    sys.exit(1001)

db_table   = 'customer_devices'
mysql_pass = 'root'
csv_file   =  sys.argv[1]

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=mysql_pass,
                             db='mysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
sql = "CREATE DATABASE IF NOT EXISTS `customers`;"
cursor.execute(sql)
connection.commit()

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=mysql_pass,
                             db='customers',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

sql = "DROP TABLE IF EXISTS `customer_devices`;"
cursor.execute(sql)
connection.commit()

sql = "CREATE TABLE `customer_devices` ( `id` int(11) unsigned NOT NULL AUTO_INCREMENT, \
  `customer_name` text, \
  `mac_address` text, \
  `device_type` text, \
  PRIMARY KEY (`id`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1;"
cursor.execute(sql)
connection.commit()

reader = csv.DictReader(open(csv_file, 'rb'))
csv_data = list()
for line in reader:
  csv_data.append(line)

for row in csv_data:
    if row['Customer Name']:
    #    row['Customer Name'] = "_unassociated_"
        print "importing: {0}, {1}, {2}".format(row['Customer Name'], row['MAC Address'], row['Device Type'])
        sql = "INSERT INTO `customer_devices` (`customer_name`,`mac_address`,`device_type`) VALUES (%s,%s,%s)"
        cursor.execute(sql, (row['Customer Name'].replace(' ','_'), row['MAC Address'], row['Device Type']))
        connection.commit()
connection.close()

print "Import completed."
