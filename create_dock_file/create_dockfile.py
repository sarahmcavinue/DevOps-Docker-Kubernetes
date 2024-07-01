import docker
from docker.errors import BuildError, APIError, ContainerError
import os
from pathlib import Path
import time

# Create a client object for Docker
client = docker.from_env()

def create_docker_file(path_py_prog, version_py, script_name):
    try:   
        # Create a Dockerfile
        with open("Dockerfile", "w") as dockerfile:
           dockerfile.write("FROM python:" + version_py + "\n")
           dockerfile.write("ADD " + path_py_prog + " /" + "\n")
           dockerfile.write("COPY requirements.txt /" + "\n")  # Copy requirements.txt
           dockerfile.write("RUN pip install -r requirements.txt" + "\n")  # Install dependencies
           dockerfile.write("CMD python /" + script_name + "\n")
           dockerfile.write("ENV PYTHONIOENCODING=utf-8\n")
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except Exception as e:
        print(f"Error creating Dockerfile: {e}")
    


def build_docker_image(image_name):
    try:
        _, build_logs = client.images.build(path=".", tag=image_name)
        for line in build_logs:
            if 'stream' in line:
                print(line['stream'].strip())
    except docker.errors.BuildError as build_error:
        print(f"Build failed: {build_error}")
    except docker.errors.APIError as api_error:
        print(f"Error in API call: {api_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def run_docker_cont(image_name):
    try:
        container = client.containers.run(
            image_name,
            detach=True,
            stdin_open=True,
            volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}}
        )
        print("Container ID:", container.id)
       

             # Pause the container
        print("Pausing the container...")
        container.pause()
        print("Container is paused.")

        # Wait for 5 seconds
        time.sleep(5)

        # Unpause the container
        print("Unpausing the container...")
        container.unpause()
        print("Container is unpaused.")

         # Fetch and print the logs properly
        log_output = container.logs(stream=True)
        for log in log_output:
            print(log.decode('utf-8').strip())

    except docker.errors.ContainerError as container_error: 
        print(f"Error in container: {container_error}")
    except Exception as e:
        print(f"Error running container: {e}")

if __name__ == "__main__":
    path_py_prog = input("Enter the path to the python program: ")
    script_name = os.path.basename(path_py_prog)  # Extracts the script name from the path
    choice = input("Enter the name of the image 1) python version 2.7, 2) python version 3.13 ")
    if choice == "1":
        version_py = "python:2.7"
    elif choice == "2":
        version_py = "python:3.13"
    else:
        print("Invalid choice")
        exit()
    

    image_name = input("Enter the name of the image: ")

    create_docker_file(path_py_prog, version_py, script_name)
    build_docker_image(image_name)
    run_docker_cont(image_name)
