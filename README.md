[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7031369&assignment_repo_type=AssignmentRepo)
# Term project for Team _start

### 1. Install dependencies

- istioctl: [Link](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/)
- kubectl: [Link](https://kubernetes.io/docs/tasks/tools/)
- helm: [Link](https://helm.sh/docs/helm/helm_install/)
- aws: [Link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- eksctl: [Link](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)

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

### 3. Start the cluster

Depending on the vendor you use, start using the provided make file.

~~~
$ make -f <VENDOR>.mak start
~~~

`<VENDOR>` can be `mk` (Minikube), `az` (Azure), `eks` (Amazon), or `gcp` (Google).

### 4. Ensure AWS DynamoDB is accessible/running

Regardless of where your cluster will run, it uses AWS DynamoDB
for its backend database. Check that you have the necessary tables
installed by running

~~~
$ aws dynamodb list-tables
~~~

The resulting output should include tables `User` and `Music`.


### To be included

gatling-music.sh requires 'USERS' and 'PAUSE' to be passed as arguments - to be set as environment variables in the container.