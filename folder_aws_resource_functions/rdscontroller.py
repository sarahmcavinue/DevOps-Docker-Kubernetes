import os

class RDSController:
    """
    Amazon Relational Database Service (Amazon RDS) Controller

    This class manages RDS instances including listing, creating, and deleting instances.
    It supports creating a MySQL DB instance with Multi-AZ deployment, subnet groups, and security groups.
    """

    def __init__(self, rds, ec2_client):
        self.rds = rds
        self.ec2_client = ec2_client

    def manage_rds(self):
        while True:
            print("\nAWS RDS Menu:")
            print("1. List RDS instances")
            print("2. Create RDS instance")
            print("3. Delete RDS instance")
            print("4. Quit")
            choice = input("Enter your choice: ").strip().lower()
            if choice == '1':
                self.list_rds_instances()
            elif choice == '2':
                self.create_rds_instance()
            elif choice == '3':
                self.delete_rds_instance()
            elif choice == '4':
                print("Exiting the menu.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def list_rds_instances(self):
        try:
            instances = self.rds.describe_db_instances()
            for instance in instances['DBInstances']:
                print(f"DBInstanceIdentifier: {instance['DBInstanceIdentifier']}, Status: {instance['DBInstanceStatus']}")
        except Exception as e:
            print(f"Error listing RDS instances: {e}")

    def create_rds_instance(self):
        try:
            print("Creating RDS instance...")

            # Use environment variables to store sensitive data
            master_username = os.getenv('MASTER_USERNAME', 'default_username')
            master_password = os.getenv('MASTER_USERPASSWORD', 'default_password')
            vpc_security_group_id = os.getenv('SECURITY_GROUP_ID', 'sg-xxxxxxxxxxxxx')

            # Create a MySQL DB instance
            response = self.rds.create_db_instance(
                DBName='mydb',
                DBInstanceIdentifier='my-db-instance',
                DBInstanceClass='db.t2.small',
                Engine='mysql',
                MasterUsername=master_username,
                MasterUserPassword=master_password,
                AllocatedStorage=20,
                VpcSecurityGroupIds=[
                    vpc_security_group_id,
                ],
                AvailabilityZone='eu-west-1a',
                DBSubnetGroupName='rds_sub_grp',
                PubliclyAccessible=True,
                MultiAZ=False,
            )

            print("RDS instance created successfully.")
            print("Please wait...")
            # Wait for the RDS instance to be available
            waiter = self.rds.get_waiter('db_instance_available')
            waiter.wait(DBInstanceIdentifier='my-db-instance')
            print("RDS instance is now available.")
        except Exception as e:
            print(f"Error creating RDS instance: {e}")

    def delete_rds_instance(self):
        try:
            response = self.rds.describe_db_instances()
            instances = response['DBInstances']
            if not instances:
                print("No RDS instances found.")
                return

            print("List of instances to choose to delete: ")
            for instance in instances:
                print(f"- {instance['DBInstanceIdentifier']}")

            DBInstanceIdentifier = input("Enter the DBInstanceIdentifier of the instance you want to delete: ").strip()
            print("Deleting RDS instance...")
            self.rds.delete_db_instance(
                DBInstanceIdentifier=DBInstanceIdentifier,
                SkipFinalSnapshot=True
            )
            print("RDS instance deleted successfully.")
        except Exception as e:
            print(f"Error deleting RDS instance: {e}")
