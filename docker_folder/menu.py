#!/usr/bin/python3
import docker
from docker.errors import BuildError, ImageNotFound, APIError, NotFound

# Create a client object for Docker
client = docker.from_env()

# Create a menu function
def menu():
    while True:
        print("\nDocker Management Menu")
        print("1. List containers")
        print("2. List all stopped containers")
        print("3. Select an image to create a container from and run it")
        print("4. Select a container to execute a command in")
        print("5. View the port mappings for a container")
        print("6. Stop and remove all containers")
        print("7. Select image to save to tar file")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            list_containers()
        elif choice == "2":
            list_stopped_containers()
        elif choice == "3":
            run_container()
        elif choice == "4":
            execute_command()
        elif choice == "5":
            view_port_mappings()
        elif choice == "6":
            stop_remove_containers()
        elif choice == "7":
            save_image()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# List containers
def list_containers():
    try:
        print("Listing all containers:")
        for container in client.containers.list(all=True):
            print(container.id)
    except Exception as e:
        print(f"Error: {e}")
# Create a function to list stopped containers
def list_stopped_containers():
    try:
        print("Listing all stopped containers:")
        for container in client.containers.list(all=True):
            if container.status == "exited":
                print(container.id)
    except APIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Error: {e}")




def execute_command():
    try:
        # List containers
        print("Listing all containers:")
        containers = client.containers.list(all=True)
         # Display the containers and their indices
        for index, container in enumerate(containers):
            print(f"Index: {index} | Container IDs: {container.short_id} | Names: {container.name}")

        # Request user to select a container by index
        container_index = int(input("Enter the index of the container you wish to use: "))

        # Check if the index is valid
        if container_index < 0 or container_index >= len(containers):
            print("Invalid index. Exiting.")
            return

        # Get the selected container
        container = containers[container_index]

        # Request user to enter a command
        command = input("Enter the command you wish to execute: ")

        # Execute command in container
        exec_instance = container.exec_run(command)

        # Display output and exit code
        print("Exit code:", exec_instance.exit_code)
        print("Output:\n", exec_instance.output.decode())
    except ImageNotFound as e:
        print(f"Image not found error: {e}")
    except APIError as api_error:
        print(f"Docker API error: {api_error}")
    except ValueError as val_error:
        print(f"Value error: {val_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    

# Create a function to run a container from an image either on the system or a new image and detach it from the terminal
def run_container():
    try:
        # Get existing images from the user's system
        existing_images = client.images.list()
        print("Existing images on your system:")
        for index, image in enumerate(existing_images):
            # Get the tags for the image if any or set it to "No Tag" if none exists
            image_tags = image.tags[0] if image.tags else "No Tag"
            # display the image details to the user with index number for selection
            print(f"{index}: Image ID: {image.id.split(':')[1][:12]} | Tags: {image_tags}")

        # Request user if they want to use an existing image or pull a new one
        choice = input("\nDo you want to use an existing image (E) or pull a new one (P)? [E/P]: ").strip().lower()
        if choice not in ['e', 'p']:
            raise ValueError("Invalid choice. Please enter 'E' for existing or 'P' for pull.")

        if choice == 'e':
            # User chooses from existing images
            index = int(input("Enter the index of the image you want to use: "))
            if index < 0 or index >= len(existing_images):
                raise ValueError("Invalid index")
            image = existing_images[index]
        else:
            # User prompted to choose to pull a new image
            image_name = input("Enter the index of the new image to pull: 1.) nginx, 2.) redis, 3.) mysql, 4.)python, 5.)ubuntu\n")
            if image_name == "1":
                image_name = "nginx"
            elif image_name == "2":
                image_name = "redis"
            elif image_name == "3":
                image_name = "mysql"
            elif image_name == "4":
                image_name = "python"
            elif image_name == "5":
                image_name = "ubuntu"

            # Pull the image
            image = client.images.pull(image_name)
            print(f"Pulled image: {image.tags[0] if image.tags else image.id.split(':')[1][:12]}")

        name = input("Enter a name for the container: ")

        # Run the container and detach it from the terminal and mount the docker socket to the container 
        container = client.containers.run(image, detach=True, name=name, tty=True, stdin_open=True, volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}})
        print(f"Container started: {container.short_id}")

    except APIError as api_error:
        print(f"Docker API Error: {api_error}")
    except ValueError as val_error:
        print(f"Error: {val_error}")
    except Exception as e:
        print(f"Unexpected Error: {e}")



# Create a function to view port mappings for a container
def view_port_mappings():
    try:
        # List containers
        print("Listing all containers:")
        containers = client.containers.list(all=True)
        # Display the containers and their indices
        for index, container in enumerate(containers):
            print(f"Index: {index} | Container IDs: {container.short_id} | Names: {container.name}")

        # Request user to select a container by index
        container_index = int(input("Enter the index of the container you wish to use: "))

        # Check if the index is valid
        if container_index < 0 or container_index >= len(containers):
            print("Invalid index. Exiting.")
            return

        # Get the selected container
        container = containers[container_index]

        # Display the port mappings
        print("Port mappings: ", container.ports)
    except APIError as api_error:
        print(f"Docker API error: {api_error}")
    except ValueError as val_error:
        print(f"Value error: {val_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    

# Stop and remove all containers
def stop_remove_containers():
    try:
        # Stop all containers
        for container in client.containers.list(all=True):
            container.stop()
            print(f"Stopped container: {container.id}")

        # Remove all containers
        client.containers.prune()
        print("All containers stopped and removed.")
    except APIError as api_error:
        print(f"Docker API error: {api_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
   

# Save an image to a tar file
def save_image():
    try:
        
        # List all images and their indices
        images = client.images.list()
        print("Available images:")
        for index, image in enumerate(images):
            print(f"{index}: Image ID - {image.id}")

        # Select image by index
        index = int(input("Enter the index of the image you wish to use: "))
        if index < 0 or index >= len(images):
            raise ValueError("Invalid index")
         
         # Get image ID from the selected image
        image_id = images[index].id

        # Ask user to enter a name for the tar file
        tar_name = input("Enter a name for the tar file: ")

        # Save the image to a tar file
        image = client.images.get(image_id)
        with open(tar_name, 'wb') as file:
            for chunk in image.save(named=True):
                file.write(chunk)
        print("Image saved to tar file:", tar_name)
    except ImageNotFound as e:
        print(f"Image not found error: {e}")
    except APIError as api_error:
        print(f"Docker API error: {api_error}")
    except ValueError as val_error:
        print(f"Value error: {val_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
# Start the menu
if __name__ == "__main__":
    menu()
