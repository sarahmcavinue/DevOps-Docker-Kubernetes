#sarah mcavinue R00240262
#AWS project
from registeruser import RegisterUser
from newuser import NewUser
from Resource import Resource
from awsmanager import AWSManager
from ebsmanager import EBSManager
from S3controller import S3Controller
from cwcontroller import CWController
from autoscale import Autoscale
from rdscontroller import RDSController
from lambhandler import LambdaHandler



def display_menu(new_aws_user, new_ebs, new_s3, new_cw, new_auto, new_rds, new_lambda):
    while True:
        choice = input('1. EC2 Instance Menu\n2. EBS Storage Menu\n3. S3 Storage Menu\n4. Monitoring Menu\n5. Autoscaling Menu\n6. RDS Menu\n7. Manage Lambda Functions \nEnter your choice (or "q" to quit): ')
        if choice == '1':
            print("EC2 Instance Menu: ")
            print(new_aws_user.manage_ec2())
        elif choice == '2':
            print("EBS Storage Menu: ")
            print(new_ebs.ebs_menu())  # Assuming the method to manage EBS is called manage_ebs
        elif choice == '3':
            # S3 management functionality 
            print("S3 Storage Menu: ")
            print(new_s3.s3_menu())
        elif choice == '4':

            # Monitoring function1
            print(new_cw.menu())
        elif choice == '5':
            # autoscaling function
            print(new_auto.menu())
        elif choice == '6':
            # RDS function
            print(new_rds.manage_rds())
        elif choice == '7':
            # Lambda function
            print(new_lambda.manage_lambda())
        elif choice.lower() == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def main():
    while True:
        choice = input("1. Login\n2. Register\n3. Quit\nEnter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            registered_user = RegisterUser(username, password, None, None)

            # Check if the user exists in the password file
            if registered_user.user_exists("password.txt"):
                print(f"\nLogin successful. Welcome: {registered_user._username}")
                print("Your AWS credentials are on file.")
                print("\nYou can now manage your AWS resources.")

                res = Resource(registered_user._aws_key, registered_user._aws_secret, 'eu-west-1')
                ec2 = res.EC2Resource()
                ec2_client = res.EC2Client()
                s3 = res.S3Resource()
                cw = res.CWClient()
                auto = res.AutoscaleClient()
                rds = res.RDSClient()
                lambda_resource = res.LambdaClient()
                
            
                new_aws_user = AWSManager(ec2, ec2_client)
                new_ebs = EBSManager(ec2, ec2_client)
                new_s3 = S3Controller(s3)
                new_cw = CWController(cw, ec2
                )
                new_rds = RDSController(rds, ec2_client)
                new_lambda = LambdaHandler(lambda_resource)
                new_auto = Autoscale(auto, cw)
                
                
                

                display_menu(new_aws_user, new_ebs, new_s3, new_cw, new_auto, new_rds, new_lambda)
            else:
                print("Invalid entry, start again")

        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            new_user = NewUser(username, password, None, None)

            if not new_user.user_exists("password.txt", username, password, None, None):
                aws_key = input("Enter AWS key: ")
                aws_secret = input("Enter AWS secret: ")
                new_user.set_aws_credentials(aws_key, aws_secret)
                new_user.register_user("password.txt", username, password, aws_key, aws_secret)

                print(f"Registration successful. Welcome: {new_user._username}")

                res = Resource(new_user._aws_key, new_user._aws_secret, 'eu-west-1')
                ec2_resource = res.EC2Resource()
                ec2_client = res.EC2Client()
                new_aws_user = AWSManager(ec2_resource, ec2_client)
                new_ebs = EBSManager(ec2_resource, ec2_client)
                s3_resource = res.S3Resource()
                new_s3 = S3Controller(s3_resource)
                cw_client = res.CWClient()
                new_cw = CWController(cw_client, ec2_resource)
                auto_client = res.AutoscaleClient()
                new_auto = Autoscale(auto_client, cw_client)
                rds_client = res.RDSClient()
                new_rds = RDSController(rds_client, ec2_client)
                lambda_resource = res.LambdaClient()
                new_lambda = LambdaHandler(lambda_resource)
                

                display_menu(new_aws_user, new_ebs, new_s3, new_cw, new_auto, new_rds, new_lambda)
            else:
                print("User already registered. Login")

        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
