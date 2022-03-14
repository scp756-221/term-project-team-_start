NAMESPACE=_start_ns
CLUSTER_NAME=_start_cluster
EKS_CONTEXT=_start_context

K8S_VERSION=1.21
REGION=us-west-2
NODE_TYPE=t3.medium
NODE_GROUP=worker-nodes
NODE_NUM=2
NODE_MIN=2
NODE_MAX=2

start: 
	showcontext
	eksctl create cluster --name $(CLUSTER_NAME) --version $(K8S_VERSION) --region $(REGION) --nodegroup-name $(NODE_GROUP) --node-type $(NODE_TYPE) --nodes $(NODE_NUM) --nodes-min $(NODE_MIN) --nodes-max $(NODE_MAX) --managed | tee ~/logs/eks-start.log
	kubectl config rename-context `kubectl config current-context` $(EKS_CONTEXT) | tee -a ~/logs/eks-start.log

stop:
	eksctl delete cluster --name $(CLUSTER_NAME) --region $(REGION) | tee ~/logs/eks-stop.log
	kubectl config delete-context $(EKS_CONTEXT) | tee -a ~/logs/eks-stop.log

up:
	eksctl create nodegroup --cluster $(CLUSTER_NAME) --region $(REGION) --name $(NODE_GROUP) --node-type $(NODE_TYPE) --nodes $(NODE_NUM) --nodes-min $(NODE_MIN) --nodes-max $(NODE_MAX) --managed | tee ~/logs/eks-start.log

down:
	eksctl delete nodegroup --cluster $(CLUSTER_NAME) --region $(REGION) --name $(NODE_GROUP) | tee ~/logs/eks-down.log

ls:
	showcontext lsnc

lsnc:
	lscl
	eksctl get nodegroup --cluster $(CLUSTER_NAME) --region $(REGION)

lscl:
	eksctl get cluster --region $(REGION) -v 0

status:
	showcontext
	eksctl get cluster --region $(REGION) | tee ~/logs/eks-status.log
	eksctl get nodegroup --cluster $(CLUSTER_NAME) --region $(REGION) | tee -a ~/logs/eks-status.log

cd:
	kubectl config use-context $(EKS_CONTEXT)

showcontext:
	kubectl config get-contexts