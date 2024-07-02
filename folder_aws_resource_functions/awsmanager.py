


class AWSManager:
    def __init__(self, ec2_resource, ec2_client):
        #ec2 constructer, assigns ec2 resource to AWSManager
        self.ec2 = ec2_resource
        self.ec2_client = ec2_client

    def manage_ec2(self):
       while True:
            print("\nAWS EC2 Menu:")
            print("1. List all instances in a Running List and Other List")
            print("2. Select and start an instance")
            print("3. Select and stop an instance")
            print("4. Launch either a Windows or Linux instance")
            print("5. Select and Terminate instance")
            print("B. Back")
            print("Q. Quit")
            choice = input("Enter your choice: ").strip().lower()
            if choice == '1':
                self.list_ec2_instances()
            elif choice == '2':
                self.start_ec2_instance()
            elif choice == '3':
                self.stop_ec2_instance()
            elif choice == '4':
                self.launch_ec2_instance()
            elif choice == '5':
                self.terminate_ec2_instance()
            elif choice == 'b':
                break
            elif choice == 'q':
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")


    
    def list_ec2_instances(self):
        try:
           running_instances = []
           other_instances = []

           for instance in self.ec2.instances.all():
                if instance.state['Name'] == 'running':
                   running_instances.append(instance)
                else:
                  other_instances.append(instance)

           print("Running EC2 Instances:")
           for instance in running_instances:
               instance_id = instance.id
               state = instance.state['Name']
               ami_id = instance.image_id
               instance_type = instance.instance_type
               region = instance.placement['AvailabilityZone'][:-1]
               launch_time = instance.launch_time
               print("\n***************************************************************************************************")
               print("\nRUNNING EC2 INSTANCES:")
               print(f"Instance ID: {instance_id}, State: {state}, AMI ID: {ami_id}, Instance Type: {instance_type}, Region: {region}, Launch Time: {launch_time}")
              


           print("OTHER EC2 INSTANCES:")
           for instance in other_instances:
               instance_id = instance.id
               state = instance.state['Name']
               ami_id = instance.image_id
               instance_type = instance.instance_type
               region = instance.placement['AvailabilityZone'][:-1]
               launch_time = instance.launch_time
               print(f"\nInstance ID: {instance_id}, State: {state}, AMI ID: {ami_id}, Instance Type: {instance_type}, Region: {region}, Launch Time: {launch_time}")
               print("\n***************************************************************************************************")
           print("END OF LIST")
        except Exception as e:
           print(f"Error listing EC2 instances: {e}")



    def start_ec2_instance(self):
      try:
          print("List of instances to choose from: ")
          self.list_ec2_instances()
          instance_id = input("Enter the EC2 instance ID to start: ").strip()
          instance = self.ec2.Instance(instance_id)

          # Check if the instance exists
          if instance.state['Name'] == 'running':
            print(f"Instance {instance_id} is already running.")
          else:
            instance.start()
            print(f"Instance {instance_id} starting")
            print("Please wait...")
            #using the waiter to wait for the instance to start
            waiter = self.ec2_client.get_waiter('instance_running')
            #waiter waits for the instance to start
            waiter.wait(InstanceIds=[instance_id])
            print(f"\nInstance {instance_id} is now running.")
      except Exception as e:
          print(f"Error starting instance {instance_id}: {e}")

    
    def stop_ec2_instance(self):
        try:
            print("List of instances to choose from: ")
            self.list_ec2_instances()
            instance_id = input("Enter the EC2 instance ID to stop: ").strip()
            instance = self.ec2.Instance(instance_id)
            # Check if the instance exists
            if instance.state['Name'] == 'stopped':
                print(f"Instance {instance_id} is already stopped.")
            else:
                instance.stop()
                print(f"Stopping instance {instance_id}")
        except Exception as e:
            print(f"Error stopping instance {instance_id}: {e}")


    def launch_ec2_instance(self):
        try:
            while True:
                print("Select the instance OS you wish to launch")
                print("1. Windows")
                print("2. Linux")
                choice = input("Enter your choice: ")
                if choice == '1':
                      instances = self.ec2.create_instances(
                          ImageId = 'ami-04c320a393da4b1ba',
                          MinCount = 1,
                          MaxCount = 1,
                          InstanceType = 't2.micro',
                          KeyName = 'key_pair',
                          SubnetId = 'subnet-xxxxxxx',
                         
                      )
                      print("Instance launching. Please wait...")
                      waiter = self.ec2_client.get_waiter('instance_running')
                      #waiter waits for the instance to start
                      waiter.wait(InstanceIds=[instances[0].id])
                      print(f"\nInstance {instances[0].id} is now running.")
                      print("Windows instance was sucessfully launched:", instances[0].id)
                      break
                    
                elif choice == '2':
                    instances = self.ec2.create_instances(
                        ImageId = 'ami-0694d931cee176e7d',
                        MinCount = 1,
                        MaxCount = 1,
                        InstanceType = 't2.micro',
                        KeyName = 'key_pair',
                        SubnetId = 'subnet-xxxxxxx',
                    )
                    print("Instance launching. Please wait...")
                    #using the waiter to wait for the instance to start
                    waiter = self.ec2_client.get_waiter('instance_running')
                    waiter.wait(InstanceIds=[instances[0].id])
                    print(f"\nInstance {instances[0].id} is now running.")
                    print("Linux instance was successfully launched:", instances[0].id)
                    break
                
                else:
                   print("Invalid choice. Please enter 1 or 2 to select instance.")
        except Exception as e:
            print(f"Error starting instance: {e}")


    def terminate_ec2_instance(self):
       try:
           print("\nList of instances to choose from: ")
           self.list_ec2_instances()
           instance_id = input("Enter the EC2 instance ID to terminate: ").strip()
           instance = self.ec2.Instance(instance_id)
           # Check if the instance is already terminated
           if instance.state['Name'] == 'terminated':
                print(f"Instance {instance_id} is already terminated.")

           elif instance.state['Name'] == 'running':
                instance.stop()
                instance.terminate()
                print(f"Stopping and terminating running instance {instance_id}")
           else:
                instance.terminate()
                print(f"Terminating instance {instance_id}")

       except Exception as e:
              print(f"Error terminating instance {instance_id}: {e}")
       
    ###############   Function created to call in other classes:      
       

    def ec2_instances(self):
        try:
            for instance in self.ec2.instances.all():
                print(f"\nInstance ID: {instance.id}")
        except Exception as e:
            print(f"Error listing EC2 instances: {e}")
          
    def stop_with_instance_id(self, instance_id):
        try:
            instance = self.ec2.Instance(instance_id)
            instance.stop()
            print(f"\nStopping instance {instance_id}")
        except Exception as e:
            print(f"\nError stopping instance {instance_id}: {e}")
              
              
