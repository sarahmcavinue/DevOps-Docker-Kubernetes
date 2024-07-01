# DevOps-Docker-Kubernetes
# Docker: docker_folder

### Overview

This repository contains various scripts and configurations for managing and automating DevOps tasks using Docker, Kubernetes, AWS, and Ansible. Each folder is organized by technology and contains necessary scripts, configurations, and instructions to set up and manage resources efficiently.

### Dependencies:

    Python 3.7
    Docker Python SDK
    Docker
    Docker Compose
    os module (used in Part 2)

### Setup:

1. Create a Python virtual environment in each directory containing the Dockerfile and Python script.
2. Install necessary packages using pip, including the Docker Python SDK.

### Running Docker Interactively:

To run the Dockerfile interactively, use the command:

```bash

sh

docker run -it -v /var/run/docker.sock:/var/run/docker.sock [IMAGE_NAME]:[TAG]

```


This mounts the Docker daemon socket, allowing the container to communicate with the Docker daemon on the Amazon-Linux host.

### Downgrading urllib3:

The urllib3 version was incompatible with the system environment, so it was downgraded using:

```bash
sh

python3 -m pip install "urllib3<2.0"
```

### Interactive Menu:

The program outputs an interactive menu using the Docker Python SDK with options to:

    List all containers.
    List all stopped containers.
    Select an image to create and run a new container.
    Execute a command in a selected container.
    View port mappings of a selected container.
    Stop and remove all containers.
    Save an image to a tar file.

### Files: menu.py, requirements.txt, dockerfile

### Dockerfile Creation and Execution:

The 'create_dockfile.py' script generates a Dockerfile to run a Python script (example.py), which outputs text in the terminal.

### Directory: 'my_files'
### Files: create_dockfile.py, requirements.txt, example.py

# Docker Compose for Pre-Defined Scenario:

A multi-container Docker Compose setup for a complex web application including databases, Redis cache, and a Flask application.

### Directory: dock_comp

### Files: Docker-compose.yml, Requirements.txt, env_file

### Example:
Modified from juggernaut's example, adding and modifying containers for a 7-container setup including Flask, Nginx, PostgreSQL, Redis, BusyBox, and Alpine.
Running Docker Compose:

Images and containers are pulled and run as specified in the docker-compose.yml. The docker ps command confirms successful container deployment.

# Kubernetes: kubernetes_folder

### Dependencies:

    Kubernetes cluster setup using kubectl, kubeadm, and kubelet.
    Kubernetes Python SDK installed via pip.

### Kubernetes Interactive Menu:

A Python script providing an interactive menu to manage Kubernetes resources using the Kubernetes Python SDK.

### Directory: kubernetes

### Files: load-balancer-service.yaml, My_kube.py, pods.yaml

### Kubernetes Menu Options:

    List all pods.
    Describe a pod.
    Create a deployment.
    Scale a deployment.
    Execute a command on a pod.
    Create a rolling update.
    Delete a deployment.
    Create pods on every worker node.

### Load Balancing Service and Multiple Pods:

Functions to apply YAML configurations for deploying a load-balancing service and multiple pods.

### Functions Used:

    apply_yaml(): Applies YAML files for deployments and services.
    list_pods(): Outputs a list of pods.
    list_services(): Lists running services.
    create_kube_resources(): Combines functions to create resources and outputs their names.

# AWS Resources: folder_aws_resource_functions

### Files containing functions to create, delete, and modify AWS resources:

    autoscale.py
    awsmanager.py
    cwcontroller.py
    ebsmanager.py
    lambhandler.py
    newuser.py
    rdscontroller.py
    S3controller.py
    registeruser.py
    main.py (menu to interact with the AWS resources)

### The AWSManager class initializes and provides a menu for EC2 management. It includes functions to list EC2 instances by their status, start and stop specific instances, and launch new instances with user-selected OS and AMI. It uses waiter methods to ensure the instances reach the desired state before proceeding.
EBSController:

### The EBSController class manages Elastic Block Store (EBS) volumes. Functions include listing volumes, creating volumes in specified Availability Zones, attaching and detaching volumes to/from instances, modifying volume sizes, listing snapshots, and creating volumes from snapshots. It provides a menu to access these functions, ensuring efficient volume management.
S3Manager:

### The S3Manager class handles operations related to Amazon S3. It includes functions to list all S3 buckets and objects within them, upload objects to a specified bucket, download objects from a bucket, and delete buckets. The class ensures smooth interaction with S3 resources.
CWController:

### The CWController class manages CloudWatch metrics and alarms. It includes functions to display metrics for selected EC2 instances and set alarms that trigger actions based on specified conditions, such as stopping an instance when disk write bytes exceed a threshold.
Autoscaling:

### The Autoscaling class interacts with an autoscaling group configured in the AWS Console. It includes functions to scale up the group when CPU utilization exceeds 90% and scale down when it drops below 30%. This ensures dynamic resource management based on workload.
RDSController:

### The RDSController class manages Amazon RDS instances. It provides functions to list, create, and delete RDS instances using predefined subnets and availability zones for a Multi-AZ deployment. It includes a menu to access these functions and utilizes waiter methods to ensure instance availability.
Lambda:

### The Lambda class handles AWS Lambda functions and related SNS notifications. It includes functions to list, create, and delete Lambda functions, and to send SNS notifications when CPU usage crosses defined thresholds. This enables automated response to system performance metrics.
AnsibleManager:

### The AnsibleManager class automates EC2 instance creation and management using Ansible. It prompts the user to input the number of instances to launch and the name of the Ansible group. The class then validates the input, creates EC2 instances with specified parameters, waits for the instances to be running, retrieves their public IP addresses, and updates a groups_ip.txt file with instance IPs and group names. This file is then used to execute an Ansible playbook for further configuration.
Ansible Playbooks

    playbook.yaml: Appends content from groups_ip.txt to /etc/ansible/hosts using the blockinfile module.
    play2.yaml: Prompts the user to choose a group name from /etc/ansible/hosts, installs Apache2 on those instances, and verifies that the server is running. This playbook ensures Apache2 is installed, running, and enabled on boot for the selected group of hosts.

Example Run


```bash
sh

ansible-playbook apache_install.yaml
```
