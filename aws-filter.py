import os
import boto3
import time
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use the JsonFormatter from python-json-logger
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(json_indent=2)  # Set the json_indent parameter
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
AWS_ACCESS_KEY=os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.environ.get('AWS_SECRET_KEY')
SLEEP_INTERVAL=os.environ.get('SLEEP_INTERVAL')


def awscallback():
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name='us-east-1'
        )

        response = ec2.describe_instances(
            Filters=[
                {'Name': 'instance-state-code', 'Values': ['16']},
                {'Name': 'tag:k8s.io/role/master', 'Values': ['1']}
            ]
        )

        instances = [instance for reservation in response.get('Reservations', []) for instance in reservation.get('Instances', [])]

        for instance in instances:
            instance_id = instance['InstanceId']
            instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'Unnamed')
            instance_launch_time = instance.get('LaunchTime').strftime('%Y-%m-%d %H:%M:%S')
            instance_ip_address = instance.get('PublicIpAddress', 'N/A')
            runtime_seconds = int((time.time() - instance['LaunchTime'].timestamp()))

            log_data = {
                "Log Level": "INFO",
                "Instance ID": instance_id,
                "Instance Name": instance_name,
                "Instance IP": instance_ip_address,
                "Launch Time": instance_launch_time,
                "Runtime (seconds)": runtime_seconds
            }

            logger.info("Aws Output", extra=log_data)

    except Exception as e:
        log_data = {
            "Log Level": "ERROR",
            "Error Message": str(e)
        } 
        logger.error("Error in awscallback", extra=log_data, exc_info=True)

while True:
    awscallback()
    time.sleep(int(SLEEP_INTERVAL))