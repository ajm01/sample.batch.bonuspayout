# Install the PostgreSQL Operator

## Create a namespace to contain both the PostgreSQL Operator and the application that will make use of it:

```shell
odo project create jbatch-demo
```

## Access your Openshift Console and install the Dev4Devs PostgreSQL Operator from the Operator Hub:

PostgreSQL Operator as shown in OperatorHub

NOTE: Install operator into the "jbatch-demo" namespace created above

## Create a database using odo via the Dev4Devs PostgreSQL Database Operator: 

>What is odo?

> odo is a CLI tool for creating applications on OpenShift and Kubernetes. odo allows developers to concentrate on creating applications without the need to administer a cluster itself. Creating deployment configurations, build configurations, service routes and other OpenShift or Kubernetes elements are all automated by odo.
>
> Before proceeding, please [install the latest odo CLI](https://odo.dev/docs/installing-odo/) 

We can use the default configurations of the PostgreSQL Operator to start a Postgres database from it. But since our app uses few specific configuration values, lets make sure they are properly populated in the databse service we start.

First, login into your cluster using the oc login command.

Attach odo to the current project/namespace
```shell
> odo set project jbatch-demo
```

Store the YAML of the service in a file:

```shell
> odo service create postgresql-operator.v0.1.1/Database --dry-run > db.yaml
```
Now, in the db.yaml file, modify the following values (these values already exist, we simply need to change them) under the spec: section of the YAML file:

```yaml
  databaseName: "sampledb"
  databasePassword: "samplepwd"
  databaseUser: "sampleuser"
```
Now, using odo, create the database from above YAML file:

```shell
> odo service create --from-file db.yaml
```

This action will create a database instance pod in the service-binding-demo namespace. The bonuspayout application will be configured to use this database.

# Configure the PostgreSQL Server

With this postgreSQL Server install it is neccessary to set a specific configation value, `max_prepared_transactions`

Access the postgre container shell:
 - ```oc rsh [postgre pod name]```
 - or, access the terminal via the Admin Console

Access the the psql cli:
```shell
> psql
```
Issue ALTER command to update the max_prepared_transactions env setting
```shell
psql# ALTER SYSTEM SET max_prepared_transactions TO 30;
```

exit psql and then restart the postgreSQL server:
```shell
pg_ctl restart -D /var/lib/pgsql/data/userdata
```

# Add DB connection information to the application

### Obtain the DB host IP address
You will be creating a kubernetes secret to contain the db connection information that will be made available to the application at startup time in the form of env vars. The two pieces of data that remain to be obtained is the postgresql server address and port. To find the address issue:

```shell
> oc get all
```
you will see a section of the results containing IP addresses for th evarious pods in your current namespace:

```
NAME                                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/postgresql                    ClusterIP   172.30.186.121   <none>        5432/TCP            3d2h
service/postgresql-operator-metrics   ClusterIP   172.30.182.150   <none>        8383/TCP,8686/TCP   3d8h
service/sampledatabase                ClusterIP   172.30.227.122   <none>        5432/TCP            3d8h
```
Make note of the IP address associated with the sampledatabase service - this is the IP address of the postgresSQL server.

The postgresSQL server port is the well known value `5432`

### Create a kubernestes secret containing the db connection information:
Before you can create a kubernetes secret you must translate all connection data into base64 encoding. There are 5 pieces of data to be converted:
- db hostname
- db port
- db username
- db user password
- db name

To convert into base64 encoding execute the following shell command for each piece of data:
```shell
echo -n '<value here>' | base64
```

and copy the resulting values into the following yaml 
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: bp-database-secret
data:
  POSTGRES_USER: <base64 value here>
  POSTGRES_PASSWORD: <base64 value here>
  POSTGRES_DB: <base64 value here>
  POSTGRES_HOSTNAME: <base64 value here>
  POSTGRES_PORT: <base64 value here>
```

Copy this yaml document and use it to create a secret via the Admin Console

or, from the command line:
```shell
kubectl apply -f ./dbsecret.yaml
```

# Run the Job

The batch job yaml file has been configured to reference the secret which makes the values avaialble to the pod environment that runs the batch job. In this manner the batch container will be able to connect to the database.

### Submit the Job itself:
```shell
kubectl create -f ./batchjob.yaml
```

This will pull the latest image containing the bonuspayout app and the script that will start the server, submit the job and then stop the server. The Job itself will run the script.
