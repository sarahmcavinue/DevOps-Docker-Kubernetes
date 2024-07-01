

class EBSManager:
    def __init__(self, ec2_resource, ec2_client):
        #ec2 constructer, assigns ec2 resource to AWSManager
        self.ec2 = ec2_resource
        self.ec2_client = ec2_client
        

    def list_volumes(self):
       try:
           # List all existing volumes
           count = 0
           # Iterate over all volumes
           for volume in self.ec2.volumes.all():
             print("********************************************************************************")

             print("\nLIST OF EBS VOLUMES:")
             # Print the volume ID, state, size, zone, and type
             print("Volume ID: ", volume.volume_id)
             print("Volume State: ", volume.state)
             print("Volume size: ", str(volume.size)+"GB")
             print("Volume zone: ", volume.availability_zone)
             print("Volume type: ", volume.volume_type)
             
             # Get the volume attachments
             attach_data = volume.attachments
             # Check if the volume has any attachments
             for attachment in attach_data:
               print("\nList of volume attachments: ")
               print("EC2 instance ID:", attachment["InstanceId"])
               print("Time of attachment: ", attachment["AttachTime"])
               print("Device: ", attachment["Device"])

               print("******************************************************************************")

               count+=1
           if count == 0:
            print("\nNo EBS detected.")
       except Exception as e:
            print(f"\nAn error occurred: {e}")



    def create_volume(self):

        try:
           ec2 = self.ec2
        
           while True:
                   print("\nSelect Availability Zone:")
                   print("1. eu-weast-1a")
                   print("2. eu-waest-1b")
                   print("3. eu-west-1c")

                   choice = input("\nEnter your choice of availability zone: ")
                   if choice == "1":
                        availability_zone =  "eu-west-1a"
                   elif choice == "2":
                        availability_zone = "eu-west-1b"
                   elif choice == "3":
                       availability_zone = "eu-west-1b"
                       break

                   if choice in ["1", "2", "3"]:
                          
                          size_gb = int(input("\nEnter the size in GB for the new volume: \n1. 10 GB, \n2. 20 GB\n"))
                          if size_gb == 1:
                            size_gb = 10
                          elif size_gb == 2:
                            size_gb = 20
                          else:
                            print("\nInvalid choice. Please select a valid size.")
                            continue
                              
                              # Create the volume
                          new_volume = ec2.create_volume(Size=size_gb, AvailabilityZone=availability_zone)
                          print(f"\nCreated volume with ID: {new_volume.id}")
                          break
                   else:
                      print("\nInvalid option")
        except ValueError:
               print("Invalid input. Please enter a number.")

    #funnction called in attach_ebs_volume
    def print_unattached_volumes(self, availability_zone):
        try:
            # List unattached volumes in the selected availability zone
            print(f"\nUnattached volumes in {availability_zone}:")
            for volume in self.ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]):
               if volume.availability_zone == availability_zone:
                print(f"Volume ID: {volume.id}, Size: {volume.size} GB")
                return
        except:
            print("\nAn error occurred while listing unattached volumes. Check that there are unattached volumes in the selected availability zone.")



    def attach_ebs_volume(self):
      try:
         
         while True:
           print("\nSelect Availability Zone you want to attach instance:")
           print("\n1. eu-west-1a \n2. eu-west-1b \n3. eu-west-1c")

           choice = input("Enter your choice of availability zone: ")
           availability_zone = {"1": "eu-west-1a", "2": "eu-west-1b", "3": "eu-west-1c"}.get(choice)

           if not availability_zone:
                print("Invalid choice. Please select a valid availability zone.")
                return

        
              # Create an empty list to hold instances that can have volumes attached
           available_instances = []
            # Iterate over all instances
           for instance in self.ec2.instances.all():
              # Check if the instance is running or stopped
             if instance.state['Name'] in ('running', 'stopped') and instance.placement['AvailabilityZone'] == availability_zone:
                block_device_mappings = instance.block_device_mappings
                 # Check if the instance has only one block device and if it is the root device
                 #Using the root device name, we can check if the instance has only one block device
                 #and if it is the root device.
                 #If the instance has only one root device, we can attach a volume to it.
                if len(block_device_mappings) == 1 and block_device_mappings[0]['DeviceName'] == instance.root_device_name:
                   #append the instance with only root block device
                   available_instances.append(instance.id)

            # Check if any available instances were found
           if available_instances:
                print(f"Instances available for volume attachment in {availability_zone}:")
                for instance_id in available_instances:
                   print(instance_id)
           else:
                print(f"No available instances for volume attachment in {availability_zone}.")
                return
             
                

           select_instance_id = input(f"Enter the instance id you want to attach ebs volume to:  ")

           print("List of available volumes to attach: ")
           self.print_unattached_volumes(availability_zone)
        

           select_volume_id = input("Enter the volume ID you wish to attach: ").strip()

           device_choices = {
            "1": "/dev/sdf", "2": "/dev/sdg", "3": "/dev/sdh",
            "4": "/dev/sdi", "5": "/dev/sdj", "q": "quit"
        }

            
           while True:
                print("\nSelect device to attach (note that there is no option to attach to root as all instances already have volumes attached to the root):")
                print("1. Attach to /dev/sdf")
                print("2. Attach to /dev/sdg")
                print("3. Attach to /dev/sdh")
                print("4. Attach to /dev/sdi")
                print("5. Attach to /dev/sdj")
                print("Q. Quit")
    
                choice = input("\nEnter your choice: ").lower()  # Convert to lowercase for case-insensitivity
                device = device_choices.get(choice)

                if device == "quit":
                    return
                elif device:
                
                   try:
                       # Get the EC2 instance object using the instance ID
                       selected_instance = self.ec2.Instance(select_instance_id)
                       selected_instance.attach_volume(VolumeId=select_volume_id, Device=device)
                       print(f"Attached volume {select_volume_id} to instance {select_instance_id} as device {device}")
                       break
                   except Exception as e:
                    print(f"An error occurred attaching the volume: {e}")
                    break
      except ValueError:
               print("Invalid input. Please enter a number.")

               return



    def detach_ebs_volume(self):
      ec2 = self.ec2
      

      while True:
        print("\nSelect Availability Zone you want to detach instance:")
        print("\n1. eu-west-1a \n2. eu-west-1b \n3. eu-west-1c")


        choice = input("Enter your choice of availability zone: ")
        availability_zone = {"1": "eu-west-1a", "2": "eu-west-1b", "3": "eu-west-1c"}.get(choice)

        if not availability_zone:
            print("Invalid choice. Please select a valid availability zone.")
            if choice == "q":
                return
            print("Invalid choice. Please select a valid availability zone.")
            continue

        # Create an empty list to hold instances that can have volumes attached
        # This dictionary will hold the instance IDs with their respective device names
        # where more than one device is attached.
        instances_with_multiple_devices = {}
        
        try:
            # Iterate over all instances with the specified availability zone, and that are running or stopped instances
            for instance in ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']},
                {'Name': 'availability-zone', 'Values': [availability_zone]}]):
                    # Get the block device mappings
                    block_device_mappings = instance.block_device_mappings
                    # Check if the instance has more than one block device
                    if len(block_device_mappings) > 1:
                        # Extract the device names and their corresponding volume IDs
                        device_info = [{'DeviceName': device['DeviceName'], 'VolumeId': device['Ebs']['VolumeId']} 
                                       for device in block_device_mappings if 'Ebs' in device]
                        # Store the device info in the dictionary with the instance ID as the key
                        instances_with_multiple_devices[instance.id] = device_info
                        break
                   
            # Check if any available instances were found
            if instances_with_multiple_devices:
               # Output the instance IDs with their respective device names
                print(f"Instances available for volume attachment in {availability_zone}:")
                print(instances_with_multiple_devices)

            instance_id_detach = input("Enter the instance ID you want to detach volume from: ").strip()
            device_detach = input("Enter the device name to detach (do not select root device /dev/sda1): ").strip()
            vol_id_detach = input("Enter the volume ID you want to detach: ").strip()
            # Get the volume object
            volume = ec2.Volume(vol_id_detach)

            # Detach the volume
            volume.detach_from_instance(Device=device_detach, InstanceId=instance_id_detach)
            print(f"Detaching volume {vol_id_detach} from instance {instance_id_detach} as device {device_detach}")
        except Exception as e:
                    print(f"Error detaching volume: {str(e)}")
                    break

                    

    def modify_ebs_volume(self):
       
     try:  
       
       self.list_volumes()
       vol_id_mod = input("\nEnter the volume ID you want to modify: ").strip()

       for volume in self.ec2.volumes.all():
                 if volume.id == vol_id_mod:
                    if volume.attachments:
                        instance_id = volume.attachments[0]['InstanceId']
                        instance = self.ec2.Instance(instance_id)
                        # Check the state of the instance
                        if instance.state['Name'] == 'running':
                            print(f"Instance {instance_id} is running. Stopping now...")
                            instance.stop()  # Stop the instance
                            instance.wait_until_stopped()  # Wait for the instance to stop
                            print(f"Instance {instance_id} has been stopped.")
                        else:
                            print(f"Instance {instance_id} is not running. Current state: {instance.state['Name']}")
                        
                        print(f"Volume {volume.id} is currently {volume.size} GiB, attached to instance {instance_id} as device {volume.attachments[0]['Device']}.")
                    else:
                        print(f"Volume {volume.id} is not attached to any instance.")
                    continue
                 print("Please choose a new size for your volume from the following options:")
                 while True:
                   print("1. 20 GiB")
                   print("2. 50 GiB")
                   print("3. 100 GiB")

                   choice = input("Enter your choice: ")
                   if choice == "1":
                            new_size = 20
                   elif choice == "2":
                            new_size = 50
                   elif choice == "3":
                            new_size = 100
                   else:
                            print("Invalid choice. Please select a valid size.")
                            continue
                   

                   response = self.ec2_client.modify_volume(VolumeId=vol_id_mod, Size=new_size)
                  
                   print(f"Modified volume {volume.id} to size {new_size} GiB.")
                   return response
          
     except ValueError:
               print("Invalid input. Please enter a number.")
     except Exception as e:
             print(f"An error occurred: {str(e)}")
        
    def list_snapshots(self):
       try:
         snapshots = self.ec2.snapshots.filter(OwnerIds=['self'])
         for snapshot in snapshots:
            print(f"\nSnapshot ID: {snapshot.id}, Volume ID: {snapshot.volume_id}, State: {snapshot.state}")
       except Exception as e:
            print(f"An error occurred: {e}")

    def create_snapshot(self):
      try:
          self.list_volumes()
          volume_id = input("\nEnter the volume ID you want to create a snapshot of: ").strip()
          volume = self.ec2.Volume(volume_id)
          description = input("Enter a description for the snapshot: ")
          snapshot = volume.create_snapshot(Description=description)
          print(f"Creating snapshot {snapshot.id}")
          print("Please wait...")
          # Wait for the snapshot to be completed
          waiter = self.ec2_client.get_waiter('snapshot_completed')
          waiter.wait(SnapshotIds=[snapshot.id])
          print(f"Snapshot {snapshot.id} is now available.")
      except Exception as e:
        print(f"An error occurred: {e}")
    
    def create_volume_from_snapshot(self):
       try:
          ec2 = self.ec2
          self.list_snapshots()
          
          snapshot_id = input("\nEnter the snapshot ID you want to create a volume from: ").strip()
          #retrieve information about the snapshot and the AZ it is located in
          print("\nSelect Availability Zone you want to detach instance:")
          print("\n1. eu-west-1a \n2. eu-west-1b \n3. eu-west-1c")

          while True:
                choice = input("\nEnter your choice of availability zone: ")
                availability_zone = {"1": "eu-west-1a", "2": "eu-west-1b", "3": "eu-west-1c"}.get(choice)


                volume = ec2.create_volume(SnapshotId=snapshot_id, 
                AvailabilityZone=availability_zone )
                print(f"\nCreated volume {volume.id} from snapshot {snapshot_id} in the availability zone {availability_zone}")
          
       except Exception as e:
            print(f"An error occurred: {e}")
          

    def ebs_menu(self):
       while True:
             print("\nEBS Management Menu:")
             print("1. List of EBS Volumes")
             print("2. Create an EBS Volume")
             print("3. Choose and attach an EBS Volume to a selected EC2 instance")
             print("4. Detach a selected EBS Volume from a selected EC2 instance")
             print("5. Modify a selected EBS Volume")
             print("6. List all Snapshots")
             print("7. Create a Snapshot")
             print("8. Create a Volume from a Snapshot")
             print("b. Back to main menu")
             print("9. Quit")

             choice = input("Enter your choice: ")
             if choice == '1':
              self.list_volumes()

             elif choice == '2':
              self.create_volume()

             elif choice == '3':
                self.attach_ebs_volume()

             elif choice == '4':
                self.detach_ebs_volume()

             elif choice == '5':
                self.modify_ebs_volume()

             elif choice == '6':
                self.list_snapshots()
             
             elif choice == '7':
                self.create_snapshot()

             elif choice == '8':
                self.create_volume_from_snapshot()

             elif choice == 'b':
                break

             elif choice == '9':
              break
             
             else:
              print("Invalid choice. Please enter a valid option.")


