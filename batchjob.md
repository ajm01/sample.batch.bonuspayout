## Installation and Configuration of the minikube environment
<b>Please Note:</b> The guide only works with minikube configured with kubernetes 1.19.x or lower. odo link cannot link services successfully in a Kubernetes 1.20.x or higher environment as of this writing.

It is recommended tothat users of this guide obtain a suitable system for running minikube with kubernetes. In practice this should be a 4 core system minimum. Before proceeding to the sample application, please follow the instructions for establishing a minikube environment:

### Install and start docker 
Please follow instructions [here](https://docs.docker.com/engine/install/) for your OS distribution.

### Install and start and configure minikube

#### <u>Install minikube</u>
Follow minikube installation instructions [here](https://minikube.sigs.k8s.io/docs/start/) for your operating system target.

#### <u>Start minikube</u>
If running as root, minikube will complain that docker should not be run as root as a matter of practice and will abort start up. To proceed, minikube will need to be started in a manner which will override this protection:
```shell
> minikube start --force --driver=docker --kubernetes-version=v1.19.8
```

If you are a non-root user, start minikube as normal (will utilize docker by default):
```shell
> minikube start --kubernetes-version=v1.19.8
```
#### <u>Configure minikube</u>
ingress config:<br>
The application requires an ingress addon to allow for routes to be created easily. Configure minikube for ingress by adding ingress as a minikube addon:
```shell
> minikube addons enable ingress
```
Note: It is possible that you may face the dockerhub pull rate limit if you do not have a pull secret for your personal free docker hub account in place. During ingress initialization two of the job pods used by ingress may fail to initialize due to pull rate limits. If this happens, and ingress fails to enable, you will have to add a secret for the pulls for the following service accounts:

- ingress-nginx-admission
- ingress-nginx

to add a pull secret for these service accounts: <br>
- switch to the kube-system context:
```shell
> kubectl config set-context --current --namespace=kube-system
```
- create a pull secret:
```shell
> kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```
~~~
        where:
          - <your-registry-server> is the DockerHub Registry FQDN. (https://index.docker.io/v1/)
          - <your-name> is your Docker username.
          - <your-pword> is your Docker password.
          - <your-email> is your Docker email.
~~~

- add this new cred ('regcred' in the example above) to the default service account in minikube:
```shell
> kubectl patch serviceaccount ingress-nginx-admission -p '{"imagePullSecrets": [{"name": "regcred"}]}'
> kubectl patch serviceaccount ingress-nginx -p '{"imagePullSecrets": [{"name": "regcred"}]}'
```

 Default Service Account Pull Secret patch:<br>
 Much like the ingress service accounts, the default service account will need to be patched with a pull secret configured for your personal docker account. 

 - switch to th edefault context:
 ```shell
 > kubectl config set-context --current --namespace=default
```

 - create the same docker-registry secret configured for your docker , now for the default minikube context:
 ```shell
 > kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
 ```


~~~
        where:
          - <your-registry-server> is the DockerHub Registry FQDN. (https://index.docker.io/v1/)
          - <your-name> is your Docker username.
          - <your-pword> is your Docker password.
          - <your-email> is your Docker email.
~~~

- Add this new cred ('regcred' in the example above) to the default service account in minikube:
```shell
> kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "regcred"}]}'
```
Kubernetes Dashboard graphical UI config:<br>
 It is helpful to make use of the basic kubernetes dashboard UI to interact with the various kubernetes entities in a graphical way. Please refer to the directions [here](https://minikube.sigs.k8s.io/docs/handbook/dashboard/) for enabling and starting the dashboard. Please note, this require the installation of and access to a desktop environment in order to make use of the dashboard. (GNOME + xrdb for example)

Operator Lifecycle Manager (OLM) config:
Enabling OLM on your minikube instance simplifies installation and upgrades of Operators available from [OperatorHub](https://operatorhub.io). Enable OLM with below command:
```shell
> minikube addons enable olm
```

### Install odo
Please follow odo installation instructions [here](https://odo.dev/docs/installing-odo/) for your OS distribution.

## What is odo?

odo is a CLI tool for creating applications and interacting with OpenShift and Kubernetes (minikube). odo allows developers to concentrate on creating applications without the need to administer a cluster itself. Creating deployment configurations, build configurations, service routes and other OpenShift or Kubernetes elements are all automated by odo.
In this doc, we are using odo to simply create a database service in our minikube cluster.

### Cluster Admin

The cluster admin needs to install 2 Operators into the cluster:

* Service Binding Operator
* A Backing Service Operator

A Backing Service Operator that is "bind-able," in other
words a Backing Service Operator that exposes binding information in secrets, config maps, status, and/or spec
attributes. The Backing Service Operator may represent a database or other services required by
applications. We'll use Dev4Devs PostgreSQL Operator found in the OperatorHub to
demonstrate a sample use case.

#### Install the Service Binding Operator

Below `kubectl` command will make the Service Binding Operator available in all namespaces on your minikube:
```shell
> kubectl create -f https://operatorhub.io/install/service-binding-operator.yaml
```
#### Install the DB operator

Below `kubectl` command will make the PostgreSQL Operator available in `my-postgresql-operator-dev4devs-com` namespace of your minikube cluster:
```shell
> kubectl create -f https://operatorhub.io/install/postgresql-operator-dev4devs-com.yaml
```
**NOTE**: This Operator will be installed in the "my-postgresql-operator-dev4devs-com" namespace and will be usable from this namespace only.
#### <i>Create a database to be used by the sample application</i>
Since the PostgreSQL Operator we installed in above step is available only in `my-postgresql-operator-dev4devs-com` namespace, let's first make sure that odo uses this namespace to perform any tasks:
```shell
> odo project set my-postgresql-operator-dev4devs-com
```

We can use the default configurations of the PostgreSQL Operator to start a Postgres database from it. But since our app uses few specific configuration values, lets make sure they are properly populated in the databse service we start.

First, store the YAML of the service in a file:
```shell
> odo service create postgresql-operator.v0.1.1/Database --dry-run > db.yaml
```
Now, in the `db.yaml` file, modify the following values (these values already exist, we simply need to change them) under `spec:` section of the YAML file:
```yaml
  databaseName: "sampledb"
  databasePassword: "samplepwd"
  databaseUser: "sampleuser"
```

Now, using odo, create the database from above YAML file:
```shell
> odo service create --from-file db.yaml
```
This action will create a database instance pod in the `my-postgresql-operator-dev4devs-com` namespace.

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
