
## Table of contents

Folder:

-Passwords
-Resource
-AWSMAnager EC2
-EBSManager
-CWController
-Autoscale
-RDS
-LambdaHandler

Ansible Folder:
-playbook.yaml
-playbook2.yaml
-Python file

******************************************************************************************************
Login credentials:
password.txt

All three usernames in the password.txt have valid IAM credentials for you to use for testing purposes.
You will need to enter the username ans password. The are:

izzy password1
dan password2
hazel password3

*******************************************************************************************************
Resources:

All the following boto3 Resources and Clients are initalized:
-EC2 resource
-EBS resource
-Cloudwatch resource
-Autoscale
-RDS resource 
-Lambda resources


**********************************************************************************************************

AWSManager:

class initalized

Function 1.
manage_ec2()
Menu function for EC2

Function 3:
list_ec2_instances()
This function creates two lists; one for running instances and one for other instances.
Lists are displyed with the attributes and their values.

Function 4:
start_ec2_instance()
Outputs a list of instances.
Prompts user selection to input instance ID.
Starts the selected instance.
Waiter method to wait and confirm instance is running.

Function 5
stop_ec2_instance():
Prompts user selection to input instance ID.
Stops the selected instance.

Function 6:
launch_ec2_instance():
Prompts user to select to launch either a Windows or Linux OS instance.
Launches the selected instance using the selected AMI.
Waiter method to wait and confirm instance is running.

**********************************************************************************************************
EBSController:

class defined and initalized.

Function 1.
list_volumes()
All volumes are listed.
Attributes and values are printed.

Function 2:
create_volumes()
Prompts user to select Availibility Zone from three options in the same region, to create volume in.
Prompts user to select the size of volume to create from three options.
Creates volume with inputs

Function 3.
attach_ebs_volume()
Prompts user to select Availibility Zone from three options, to attach volume in.
Lists all available instances that are running or stopped state; checks devices that only have root volume attached.
User input selects from the list instance ID.
The attributes and values for the instance Id are outputted.
User selects from choice of devices to attach volume to. Choice includes a number of devices except the root device. 
This makes it easy to attach a volume as all devices except root are available to attach.
Volume is attached.

Function 3.
detach_ebs_volume
Prompts user to select Availibility Zone from three options, to detach volume from.
This provides a list of all available instances: with more than root volumes attached, in the selected availability zone and in a running or stopped state.
Lists all instance ids, thier volumes and attributes including device names to which they have attachments to.
Prompts user selection to select instance to detach the device and volume id.

Function 4.
modify_ebs_volume():
Outputs a list of volumes and prompts user input to select volume id to modify.
Checks if the instance that the volume is attached to is running. 
If it is running it stops the instance and waits for the instance to stop.
Provides choice of volume size to modify volume.
Prompts user input to select choice of size to modify volume to.
Modifies the selected volume to the choice of size.

Function 5:
list_of_snapshots
Provides a list of snapshots with their attributes and values.

Function 6:
create_volume_from_snapshot
Outputs a list of snapshots.
Prompts user selection to input selected snapshot id.
The snapshot object is retrieved with the snapshod id.
Volume id is retrieved from the snapshot.
Availability zone is the same availability zone of the snapshot.
The volume is created with the volume object, snapshot id and availability zone.

Function 7:
ebs_menu:
Menu for all ebs functions.
************************************************************************************************************

class S3Manager



***************************************************************************************************************
CWController
class defined and initalized.

Function 1:
display_metrics()
Outputs running and other instances.
Prompts the user to input the selected instance, specifies to choose from running list.
Prompts user to input selected running instance id.
Displays metrics for the selected EC2 instance.
Metrics displayed are DiskReadOps and CPUCreditsUsage for the past 30 minutes.

Function 2:
set_alarm()
Function displays a list of instances, prompts the user to input an instance id.
Cloudwatch alam is set to detect DiskWriteBytes that are greater than or equal to 9000.
Once triggered the alarm will stop the instance that triggered the alarm.

**********************************************************************************************************
Autoscaling:
class defined and initalized.
Autoscale group was created in the AWS Console.
Topic created in the AWS Console to enable SNS messages triggered by the functions.

Funtion 1:
autoscale_scale_up()
Autoscaling function to scale up once the CPU reaches above 90% CPU utilization.
This function useses an autoscaling group that was created in the AWS console.

Function 2:
autoscale_scale_down()
Autoscaling function to scale down once the CPU reaches below 30% CPU utilization.
This function uses an autoscaling group that was created in the AWS console.


***************************************************************************************************************
RDS:
class defined and initalized.
RDS subnet group created with three different Availability Zones in the same Region to enable creation of the RDS instance.
Three Availability Zones in the same region creates a Multi-AZ deployment.
DB subnet group specified in the functions; this subnet group supports networking and use of Availability Zones when creating a DB instance.
    

Function 1.
manage_rds()
Menu manages RDS functions
Amazon Relational Database Service (Amazon RDS)


Function 2:
list_rds_instances
Outputs a list of RDS instances.

Function 3:
create_rds_instance
Creates an SQL instance using a free tier SQL AMI.
Subnets, availability zones and DB groups are hard coded, they were created in the Console.
Waiter method to wait for the RDS instance to be available before continuing

Function 4:
 delete_rds_instance
 Outputs the a list of DBIdentifer.
 Prompts the user to select the RDS instance to delete.
 Deletes the RDS instance.

**********************************************************************************************************************

Lambda:
class initalized.

SNS Service enabled through the AWS Console.
IAM group policy access to enable access to lambda.
Object access point created in S3 to access the code file.


Function 1:
list_lambda_functions()
Displays list of Lambda functions.

Function 2.
create_lambda_function()
Creates lambda function.

Function 3.
delete_lambda_function()
List of lambda functions outputted.
Prompts user to select and input lambda function to delete.
Deletes function.

Function 4. 
CPU_low_email_message()
Lambda function to send SNS was envoked through the AWS Console and the IAM role was created.
Send an email when CPU usage is below 30%

Function 4:
CPU_high_email_message()
Lambda function to send SNS was envoked through the AWS Console and the IAM role was created.
Send an email when CPU usage is above 90%


*********************************            Ansible       ****************************
Instructions:
-Environmental variable for access key and secret are imported.
-First the groups_ip.txt file was created and is empty.
-SSH credentials was inputted to the remote servers (key_pair) in the group to install Apache2.
-IAM permissions assigned to the Master ubuntu host.


class AnsibleManager:

Python Function:
main()
From the menu the user is prompted to input the number of instances they wish to create. 
The attributes and values using a Linux AMI are used to create the instance.
The function returns a list of the IP addresses of the newly created instances and adds them to the groups_ip.txt.
The user is prompted to input a name for the user group this value is also added to the groups_ip.txt.
The groups_ip.txt file is written to with the IP addresses and group name to the playbook file.
The playbook is invoked.

playbook.yaml 
Appending content from a the group_ips.txt to the host file /etc/ansible/hosts.
Ansible blockinfile module was used to append the block of text to a file.

play2.yaml
User input prompted using vars_prompt to choose a group name from those in /etc/ansible/hosts.
Installs and runs the Apache2 server on that group of instances.
Checks that Apache 2 is running.
