### bring up mysql container
```
docker run -d -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql
```

### install python requirements
```
pip install -r requirements.txt
```
### import customer data to MySQL container (download source csv to this directory)
```
python customer-csv-mysql.py filename.csv
```

## Setup Grafana

I've included the dashboard.json so you can see the templating directly in an applied example.  Otherwise you can add this to any dashboard (yes, even with the database being on your local host).

Once the mysql queries extract the data, they are available as a list item variable for your Elasticsearch queries. Note that the special `All` values automatically default to a data set as suited to a particular datasource. ie.  `'item1', 'item2', 'item3'` for **MySQL** queries and `('item1' OR 'item2' OR 'item3')` for **Elastic/Lucene** queries.

#### Datasource
Once your mysql container is up and populated with the customer data, you can set up the datasource in Grafana.  Note that since this datasource is actually local, it will still work in a local-browser Granfa views on your laptop, it will not work as a datasource for anyone else.  Unless of course they happen to have the customer populated MySQL container running locally as well.

click `Add Datasource`

```
Name:     customer_sql_POC
Default:  unchecked
Type:     MySQL
Host:     localhost:3306
Database: customers
User:     root
Password: root
```

#### Variables
From the main dashboard, click the settings gear and select `Templating`

We will create three new variables for use in the dashboards

for each, click `+ New`

leave fields blank unless otherwise noted.

```
name:        customer
type:        Query
datasource:  customer_sql_POC
refresh:     On Dashboard Load
query:       select customer_name from customer_devices
sort:        Alphabetical (asc)
Include All: checked

name:        device
type:        Query
datasource:  customer_sql_POC
refresh:     On Dashboard Load
query:       select device_type from customer_devices where customer_name in ($customer)
sort:        Alphabetical (asc)
Include All: checked

name:        mac_address
type:        Query
datasource:  customer_sql_POC
refresh:     On Dashboard Load
query:       select mac_address from customer_devices where customer_name in ($customer) and device_type in ($device)
sort:        Alphabetical (asc)
Include All: checked

```

Now you will have three variables you can use anywhere in your Dashboard: in queries, in graph titles, text areas, etc etc.

-  `$customer`  
-  `$device`
-  `$mac_address`
