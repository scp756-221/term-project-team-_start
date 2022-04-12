[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7031369&assignment_repo_type=AssignmentRepo)
# Term project for Team _start

## Preperation

### 1. Install dependencies

- kubectl: [Link](https://kubernetes.io/docs/tasks/tools/)
- aws: [Link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- eksctl: [Link](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)
- helm: [Link](https://helm.sh/docs/helm/helm_install/)
- istioctl: [Link](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/)

### 2. Instantiate the template files

Fill in the required values in the template variable file

Copy the file `cluster/tpl-vars-blank.txt` to `cluster/tpl-vars.txt`
and fill in all the required values in `tpl-vars.txt`.  

Instantiate the templates

Once you have filled in all the details, run

~~~
$ make -f k8s-tpl.mak templates
~~~

This will check that all the programs you will need have been
installed and are in the search path.  If any program is missing,
install it before proceeding.

The script will then generate makefiles personalized to the data that
you entered in `clusters/tpl-vars.txt`.

**Note:** This is the *only* time you will call `k8s-tpl.mak`
directly. This creates all the non-templated files, such as
`k8s.mak`.  You will use the non-templated makefiles in all the
remaining steps.

## Deploy Services

### 1. Create the DynamoDB tables

~~~
$ aws cloudformation create-stack --stack-name DynamoDB --template-body file://<Path-to-Repository>/term-project-team-_start/cluster/cloudformationdynamodb.json
~~~

### 2. Ensure AWS DynamoDB is accessible/running

Regardless of where your cluster will run, it uses AWS DynamoDB
for its backend database. Check that you have the necessary tables
installed by running

~~~
$ make -f k8s.mak dynamodb-init
$ aws dynamodb list-tables
~~~

The resulting output should include tables `User` and `Music`.

### 3. Start the cluster

Depending on the vendor you use, start using the provided make file.

~~~
$ make -f <VENDOR>.mak start
~~~

`<VENDOR>` can be `mk` (Minikube), `az` (Azure), `eks` (Amazon), or `gcp` (Google).

### 4. Create namespace

EKS cluster context name is **aws756**. Use the context-name for `kubectl` to create namespace:

~~~
$ kubectl config use-context aws756
$ kubectl create ns c756ns
$ kubectl config set-context aws756 --namespace=c756ns
~~~

### 5. Building docker images and pushing to github container registry

Build images for the database service, three micro services, and the loader

~~~
$ make -f k8s.mak cri
~~~

Once complete, go to github, under *packages* make the images public

## 6. Monitoring

Three tools will be used to monitor the distributed application and microservices: Grafana, Prometheus and Kiali

### 7. Provision and Deploy

First, copy your GitHub Repository token to `cluster/ghcr.io-token.txt`.

Install istio, prometheus, kiali, and their dependencies; and deploy the microservices by running

~~~
$ make -f k8s.mak provision
~~~

### 8. Grafana

Get Grafana URL, run:

~~~
$ make -f k8s.mak grafana-url
~~~

Click the url and login with:
  User: 'admin'
  Password: 'prom-operator'

After signon, in Grafana home screen, aavigate to the dashboard by hovering on the “Dashboards” icon on the left.
Select “Browse” from the menu. This will bring up a list of dashboards. Click on c756 transactions.

### 9. Prometheus

Get Prometheus URL, run:

~~~
$ make -f k8s.mak prometheus-url
~~~

### 10. Kiali
Get Kiali URL, run:

~~~
$ make -f k8s.mak kiali
$ make -f k8s.mak kiali-url
~~~

### 11. Load testing the services
Use Gatling for simulating high traffic for various services. The supported service_name values are: 'User', 'Music', 'Playlist', 'All'.

~~~
$ ./gatling.sh <number_of_users> <pause_between_runs> <service_name>
~~~

For instance, to run all services for 100 users every 10ms:

~~~
$ ./gatling.sh 100 10 All
~~~

To stop all running Gatling jobs:

~~~
$ ./tools/kill-gatling.sh
~~~
