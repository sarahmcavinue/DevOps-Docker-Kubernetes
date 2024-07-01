from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from awsmanager import AWSManager
import boto3



class CWController:
    def __init__(self, cw_client, ec2_resource):
        #ec2 constructer, assigns ec2 resource to CWController
        self.cw = cw_client
        self.ec2 = ec2_resource
       
       

     # Function to display metrics for a selected EC2 instance
    def display_metrics(self):
        
        print("Instances to choose from select running instances only:")
        AWSManager.list_ec2_instances(self)
        print("********************")
          
        instance_id = input("Enter the EC2 instance ID from the running list: ").strip()
        #List of metrics to choose from
        metrics = ["DiskReadOps", "CPUCreditsUsage"]
        for metric in metrics:
        
         try:
            
             response = self.cw.get_metric_statistics(
             Namespace="AWS/EC2",
             #Metric name to be displayed
             MetricName=metric,
             Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
             # Get data for last 30 minutes
             StartTime=datetime.utcnow() - timedelta(minutes=30),
             #end time is now
             EndTime=datetime.utcnow(),
             #Frequency of the period points in the range; time in seconds; 1800 seconds equals 30 minutes; every 30 min there is a data point
             Period=1800,
             #Average the data over last 30 minutes
             Statistics=['Average']
             )
             if response['Datapoints']:
               averarge = response['Datapoints'][0]['Average']
               print(f"{metric} for {instance_id}: Average = {averarge}")
             else:
                print(f"No data for {metric} for {instance_id}")

         except ClientError as e:
            print(f"Error getting metrics: {e}")



       # Function to set an alarm
    def set_alarm(self):
        try:
            print("List of instances to choose from: ")
            #List all instances
            print("Instances to choose from select running instances only:")
            AWSManager.list_ec2_instances(self)
            print("********************")
            
            instance_id = input("Enter the EC2 instance ID: ").strip()
            # Alarm action (ARN of the stop action)
            stop_action = f'arn:aws:automate:eu-west-1:ec2:stop'



             #set alarm
            self.cw.put_metric_alarm(
            AlarmName="HighDiskWriteBytes",
            MetricName="DiskWriteBytes",
            Namespace="AWS/EC2",
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            Statistic="Sum",
            #Threshold is 9,000 bytes
            Threshold=9000,
            Period=300,
            EvaluationPeriods=1,
            #Greater than or equal to threshold
            ComparisonOperator="GreaterThanOrEqualToThreshold",
            AlarmActions=[stop_action],
            Unit='Bytes')
            print("Alarm set successfully.")

            print("Instance stopped successfully.")
        except ClientError as e:
          print(f"Error setting alarm: {e}")



#Please note that the four optional functions are located in autoscaling.py and lambdahandler.py
#The autoscaling.py file contains two autoscaling policy functions
#The lambdahandler.py file contains two email functions
    
    def menu(self):
        while True:
           print("\nAWS Management Menu")
           print("1. Display EC2 Metrics for a selected instance displaying the average DiskReadOps and CPUCreditUsage over the last 30 minutes")
           print("2. Set EC2 Alarm for a selected instance to stop the instance if the DiskWriteBytes is greater than or equal to 9,000 bytes")
           print("3. Exit")
           choice = input("Enter your choice (1-3): ")

           if choice == '1':
                self.display_metrics()
               
           elif choice == '2':
                self.set_alarm()
           elif choice == '3':
                print("Exiting the program.")
                break
           else:
                print("Invalid choice. Please enter a number between 1 and 7.")
          
