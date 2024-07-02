# Description: This file contains the LambdaHandler class which is used to send email notifications to the user when the CPU utilization is low or high.


class LambdaHandler:
    def __init__(self, lambda_client):
        self.lambda_client = lambda_client

        
    def manage_lambda(self):
        while True:
            print("\nAWS Lambda Menu:")
            print("1. List Lambda functions")
            print("2. Create Lambda function")
            print("3. Delete Lambda function")
            print("B. Back")
            print("Q. Quit")
            choice = input("Enter your choice: ").strip().lower()
            if choice == '1':
                self.list_lambda_functions()
            elif choice == '2':
                self.create_lambda_function()
            elif choice == '3':
                self.delete_lambda_function()
            elif choice == 'b':
                return
            elif choice == 'q':
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")

    def list_lambda_functions(self):
        try:
            response = self.lambda_client.list_functions()
            for function in response['Functions']:
                print(f"Function Name: {function['FunctionName']}, ARN: {function['FunctionArn']}")
        except Exception as e:
            print(f"Error listing Lambda functions: {e}")


    def create_lambda_function(self):
        try:
            print("Creating Lambda function...")
            # Create a Lambda function
            self.lambda_client.create_function(
                FunctionName='cpu_low_email_message',
                Runtime='python3.11',
                Role='arn:aws:iam::xxxxxxx:role/lambda',
                Handler='lambdahandler.cpu_low_email_message',
                Code={
                    'S3Bucket': 'sarahmcavinue2023',
                    'S3Key': 'lambdahandler.zip',
                },
                Description='This function sends an email to notify the user of low CPU utilization.',
            )

            self.lambda_client.create_function(
                FunctionName='cpu_high_email_message',
                Runtime='python3.11',
                Role='arn:aws:iam::xxxxx:role/lambda',
                Handler='lambdahandler.cpu_high_email_message',
                Code={
                    'S3Bucket': 'sarahmcavinue2023',
                    'S3Key': 'lambdahandler.zip',
                },
                Description='This function sends an email to notify the user of low CPU utilization.',
            )
            
             
            print("Lambda function created successfully.")
            
        except Exception as e:
            print(f"Error creating Lambda function: {e}")


    def delete_lambda_function(self):
        try:
            print("List of functions to choose to delete: ")

            response = self.lambda_client.list_functions()
            for function in response['Functions']:
                print(f"Function Name: {function['FunctionName']}, ARN: {function['FunctionArn']}")
            FunctionName = input("Enter the FunctionName of the function you want to delete: ")
            print("Deleting Lambda function...")
            self.lambda_client.delete_function(
                FunctionName=FunctionName
            )
            print("Lambda function deleted successfully.")
        except Exception as e:
            print(f"Error deleting Lambda function: {e}")


    def CPU_low_email_message(self):
    # Email details
        SENDER = "xxxxxxx@mycit.ie"
        RECIPIENT =  "xxxxxxx@mycit.ie"
        AWS_REGION = "eu-west-1"
        SUBJECT = "Low CPU Utilization Notification"
        BODY_TEXT = "The CPU utilization has fallen below 30%."

    # Send email
        response = self.lambda_client.send_email(
        Destination={'ToAddresses': [RECIPIENT]},
        Message={
            'Body': {'Text': {'Data': BODY_TEXT}},
            'Subject': {'Data': SUBJECT},
        },
        Source=SENDER )
        print(response)


    def CPU_high_email_message(self):
    #Topic created in the AWS console to send SNS when it exceed 90% CPU usage
    # Email details
        SENDER = "xxxxxxx@mycit.ie"
        RECIPIENT =  "xxxxxxxx@mycit.ie"
        AWS_REGION = "eu-west-1"
        SUBJECT = "High CPU Utilization Notification"
        BODY_TEXT = "The CPU utilization has increased to above 90%."

    # Send email
        response = self.lambda_client.send_email(
        Destination={'ToAddresses': [RECIPIENT]},
        Message={
            'Body': {'Text': {'Data': BODY_TEXT}},
            'Subject': {'Data': SUBJECT},
        },
        Source=SENDER )
        print(response)
        
