import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

class Resource:
    def __init__(self, region_name='eu-west-1'):
        self.region = region_name
        self._aws_key = os.getenv('AWS_ACCESS_KEY_ID')
        self._aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        
    def EC2Resource(self):
        # Create and return a Resource for interacting with EC2 instances
        ec2 = boto3.resource(
            "ec2", 
            aws_access_key_id=self._aws_key, 
            aws_secret_access_key=self._aws_secret, 
            region_name=self.region
        )
        return ec2
    
    def EC2Client(self):
        # Create and return a Client for interacting with EC2 instances
        ec2_client = boto3.client(
            "ec2", 
            aws_access_key_id=self._aws_key, 
            aws_secret_access_key=self._aws_secret, 
            region_name=self.region
        )
        return ec2_client

    def S3Resource(self):
        # Create and return a Resource for interacting with S3 instances
        s3 = boto3.resource(
            "s3", 
            aws_access_key_id=self._aws_key, 
            aws_secret_access_key=self._aws_secret, 
            region_name=self.region
        )
        return s3

    def CWClient(self):
        # Create and return a Client for interacting with CloudWatch
        cw = boto3.client(
            'cloudwatch', 
            aws_access_key_id=self._aws_key, 
            aws_secret_access_key=self._aws_secret, 
            region_name=self.region
        )
        return cw
    
    def AutoscaleClient(self):
        # Create and return a Client for interacting with Autoscaling
        autoscale = boto3.client(
            'autoscaling', 
            aws_access_key_id=self._aws_key, 
            aws_secret_access_key=self._aws_secret, 
            region_name=self.region
        )
        return autoscale
    
    def RDSClient(self):
        # Create and return a Client for interacting with RDS
        rds = boto3.client(
            'rds', 
            aws_access_key_id=self._aws_key, 
            aws_secret_access_key=self._aws_secret, 
            region_name=self.region
        )
        return rds
    
    def LambdaClient(self):
        try:
            # Create and return a Client for interacting with Lambda
            lambda_client = boto3.client(
                'lambda', 
                aws_access_key_id=self._aws_key, 
                aws_secret_access_key=self._aws_secret, 
                region_name=self.region
            ) 
            return lambda_client
        except (ClientError, BotoCoreError) as e:
            print(f"An error occurred: {e}")
            return None
