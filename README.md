# Jenkisn CI-CD Project

A brief description of your project.
we have a Python applicaion that is checking the  AWS instances base on tage we define on the EC2.
The Python application is compile to a multistage dockerfile.
When you update any part of the code on development branch  all the code will be automaticly merg to main branch.
the pipline will deploy a new continer with the application. 

# Usage
You mose have the python, requirements.txt &Jenkinsfile on the same folder in order to the application to work.
You will need to change in the Dockerfile the environment variables of AWS_ACCESS_KEY & AWS_SECRET_KEY to your  AWS key.
You will need to change the region name in the python base on the region you use in AWS.
