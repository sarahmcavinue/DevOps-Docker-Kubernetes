import cwcontroller



class Autoscale:


    def __init__(self, auto_resource, cw_resource):
        self.autoscale = auto_resource
        self.cw = cw_resource
       
       



#An autoscaling group was created in the AWS console
#This function is used to create a scaling policy
#The scaling policy is used to scale the number of instances in response to a changing load
#The type of scaling policy that was chosen to be simple scaling
#The simple scaling policy enables the system to scale the number of instances in response to a changing load
#Lambda function was created in the AWS console to send SNS when it exceed 90% CPU usage

    def autoscale_scale_up(self):
          
         # Auto Scaling Group name
          auto_scaling_group_name = 'autoscale_grp'

            
        # Create a simple scaling policy
          response = self.autoscale.put_scaling_policy(
          AutoScalingGroupName=auto_scaling_group_name,
          PolicyName='ScaleUpPolicy',
          PolicyType='SimpleScaling',
          AdjustmentType='ChangeInCapacity',
          ScalingAdjustment=1,  # One instance to add
          Cooldown=200 )  # Cooldown period in 200 seconds

          # Extract the Policy ARN
          policy_arn = response['PolicyARN']

          print(f"Created Scaling Policy: {policy_arn}")
          #Topic created in the AWS console to send SNS when it exceed 90% CPU usage
          sns_topic_arn = 'arn:aws:sns:eu-west-1:xxxxx:high_use_90'
          
  
          


          #Using CloudWatch to monitor the scaling policy
          # Create an alarm to monitor CPU utilization
          response = self.cw.put_metric_alarm(
          AlarmName='HighCPUUtilization',
          MetricName='CPUUtilization',
          Namespace='AWS/EC2',
          Statistic='Average',
          Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': auto_scaling_group_name
              },
          ],
          # CPU utilization greater than 90%
          # The alarm will be triggered if the CPU utilization is greater than 90% for 60 seconds
          #Using the period of 60 seconds
          Period=60,
          Threshold=90,
          #Using the greater than threshold
          ComparisonOperator='GreaterThanThreshold',
          #Using the evaluation period of 1
          EvaluationPeriods=1,
          AlarmActions=[sns_topic_arn, policy_arn],
          Unit='Percent'
                    )
         
          print("Created CloudWatch alarm for high CPU utilization: ")
          print("Email sent to notify user of high CPU utilization: ")
          
    

    def autoscale_scale_down(self):
        #Scaling down the number of instances terminates the instance
        #The instance is terminated when the CPU utilization is less than 30% for 60 seconds

        # Auto Scaling Group name
        auto_scaling_group_name = 'autoscale_grp'
        #notify_low_cpu via email with Topic created in the AWS console
        sns_topic_arn = 'arn:aws:sns:eu-west-1:xxxxxx:CPU-low.fifo'
        
            
        

             # Create a simple scaling policy
        response = self.autoscale.put_scaling_policy(
              AutoScalingGroupName=auto_scaling_group_name,
              PolicyName='ScaleDownPolicy',
              PolicyType='SimpleScaling',
              AdjustmentType='ChangeInCapacity',
              ScalingAdjustment=-1,  # One instance to remove
              Cooldown=200 )  # Cooldown period in 200 seconds
        
           # Extract the Policy ARN
        policy_arn = response['PolicyARN']
        print(f"Created Scale Down Scaling Policy: {policy_arn}")

           # Create an alarm to monitor low CPU utilization
        response = self.cw.put_metric_alarm(
          AlarmName='LowCPUUtilization',
          MetricName='CPUUtilization',
          Namespace='AWS/EC2',
          Statistic='Average',
          Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': auto_scaling_group_name
            },
             ],
          Period=60,
          # CPU utilization less than 30%
          Threshold=30,
          ComparisonOperator='LessThanThreshold',
          EvaluationPeriods=1,
          #sns_topic_arn is used to send email to notify user of low CPU utilization
          AlarmActions=[policy_arn, sns_topic_arn],
          Unit='Percent'
           )
        print("Created CloudWatch alarm for low CPU utilization")
        print("Email sent to notify user of low CPU utilization ")
         
        

    def menu(self):
     while True:
        print("\nAWS Autoscale Menu")
        print("1. Set Autoscaling Policy to scale up with email notification")
        print("2. Set Autoscaling Policy to scale down with email notification")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
             self.autoscale_scale_up()
            
            
        elif choice == '2':
             self.autoscale_scale_down()
             
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")


        

