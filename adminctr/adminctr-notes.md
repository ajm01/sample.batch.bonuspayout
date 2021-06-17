# Setup for Admin Center

1. Build the admin center image using the dockerfile in this dir
2. apply the admin center yaml file - will deploy the admin center image and establish a service
3. enable ingress in minikube
4. apply the ingress yaml in this directory to open an ingress to the new service
5. access the admin center via the defined url: https://adminctr.local/adminCenter/
6. if on openshift: declare a route via yaml and apply