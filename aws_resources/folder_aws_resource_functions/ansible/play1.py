

import os
import sys
import boto3


class AnsibleManager:

    def __init__(self, ec2, ec2_client):
        #ec2 constructer, assigns ec2 resource to AWSManager
        self.ec2 =  ec2
        self.ec2_client = ec2_client
    


    def main(self):
       
       ip_addresses = []
       try:
           count_instance = int(input("Enter the number of instances between 1-5 to launch: "))
           group_name = input("Enter the name of the ansible group: ").strip()
        
           # Validate the number of instances
           if count_instance < 1 or count_instance > 5:
            print("Invalid number of instances. Please enter a number between 1-5")
            return

           # Create the instance
           instances = self.ec2.create_instances(
                    ImageId = 'ami-0694d931cee176e7d',
                    MinCount = count_instance,
                    MaxCount = count_instance,
                    InstanceType = 't2.micro',
                    KeyName = 'key_pair',
                    SecurityGroupIds = ['sg-xxxxxxxxxxxx'],
                    SubnetId = 'subnet-xxxxxxxxxx'
                    )
           print("Instance launching ...")
           print("Please wait ...")
            # Waiter used to wait for the instance to be running
           waiters = self.ec2_client.get_waiter('instance_running')
           waiters.wait(InstanceIds=[instance.id for instance in instances])
            
            # Wait for the instance to be running before getting the public IP
           print("Getting public IP addresses...")
           for instance in instances:
                instance.wait_until_running()
                # Reload the instance attributes to get the public IP address
                instance.reload()
                if instance.public_ip_address:
                    ip_addresses.append(instance.public_ip_address)
                    print(f"Public IP address: {instance.public_ip_address}")
                else:
                    print("Public IP address not assigned yet. Please wait...")
                    

                
           # Write the group name and IP addresses to a file
           print("\nCreating groups_ip.txt file...")
           with open('groups_ip.txt', 'w') as file:
                 file.write(f"[{group_name}]\n")
                 for ip_address in ip_addresses:
                     file.write(f"{ip_address}\n")

           # Set the file permissions to 600             
           os.chmod('groups_ip.txt', 0o600)
           # Write the group name and IP addresses to a groups_ip.txt file
           print("Writing group name and IP addresses to file...")

           print("Ansible group created successfully")
           print("Running ansible playbook...")
           os.system("ansible-playbook -i groups_ip.txt playbook.yaml")
        
       except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    ec2 = boto3.resource('ec2',  region_name='eu-west-1')
    ec2_client = boto3.client('ec2', region_name='eu-west-1')
    new_ansible = AnsibleManager(ec2, ec2_client)
    new_ansible.main()

    
