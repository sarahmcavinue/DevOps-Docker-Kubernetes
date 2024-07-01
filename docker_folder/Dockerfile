# Start with a base image that includes Python
FROM python:3.7.16-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
#require pip docker in requirement.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container at /app
COPY . /app

# The script to run when the container starts
CMD ["python", "menu.py"]
