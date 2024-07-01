
from kubernetes import client, config, stream
from kubernetes.client.rest import ApiException
import subprocess


# Initialize Kubernetes config
config.load_kube_config()

api = client.CoreV1Api()
apps_api = client.AppsV1Api()


#this function is integrated with the main menu to list all the pods in all namespaces
def list_pod_names_and_namespaces():
    try:
        # List all pods across all namespaces
        pods = api.list_pod_for_all_namespaces(watch=False)
        for i, pod in enumerate(pods.items):
            print(f"{i}. {pod.metadata.name} in {pod.metadata.namespace}")
            return pods.items
    except ApiException as e:
        print(f"Exception when accessing Kubernetes API: {e}")
        return []

#this function is integrated with option 2 and option 8 in the main menu to list all namespaces

def list_namespaces():
    try:
        namespaces = api.list_namespace()
        for i, ns in enumerate(namespaces.items):
            print(f"{i}: Namespace: {ns.metadata.name}")
        return namespaces.items
    except ApiException as e:
        print(f"Exception when listing namespaces: {e}")
        return []


#this function is integrated with option 2 in the main menu to list all pods and include an index

def list_all_pods(namespace):
    try:
        pods = api.list_namespaced_pod(namespace)
        for i, pod in enumerate(pods.items):
            print(f"{i}: Pod Name: {pod.metadata.name}")
        return pods.items
    except ApiException as e:
        print(f"Exception when listing pods in {namespace}: {e}")
        return []


#this function is integrated with option 4 scale deployment the main menu to list all the deployments in namespaces
def list_all_deployments():
    deployment_list = []
    try:
        deployments = apps_api.list_deployment_for_all_namespaces()
        print("Available Deployments in All Namespaces:")
        for i, deployment in enumerate(deployments.items):
            deployment_info = { "namespace": deployment.metadata.namespace, "name": deployment.metadata.name }
            deployment_list.append(deployment_info)
            print(f"{i}: Deployment Name: {deployment.metadata.name} in Namespace: {deployment.metadata.namespace}")
        return deployment_list
        
    except ApiException as e:
        print(f"Exception when listing all deployments: {e}")
        return []


#option 1; list all pods in all namespaces with their details
def list_pods():
    try:
        pods = api.list_pod_for_all_namespaces(watch=False)
        print("Listing all pods in all namespaces:")
        for i, pod in enumerate(pods.items):
            print(f"Pod name: {pod.metadata.name}")
            print(f"Pod namespace: {pod.metadata.namespace}")
            print("--------------------------------------------------")
    except ApiException as e:
        print(f"Exception when listing pods: {e}")

#option 2; describe a pod in a namespace
def describe_pod():
    print("Listing all pods in all namespaces:")
    #calling function to namespaces 
    namespaces = list_namespaces()

    try:
        #namespace index to select the namespace
        ns_index = int(input("Enter the index of the namespace: "))
        #slected index of the namespace
        selected_namespace = namespaces[ns_index].metadata.name

        print(f"\nListing all pods in namespace: {selected_namespace}")
        #calling function to list all pods in the selected namespace
        pods = list_all_pods(selected_namespace)

        pod_index = int(input("Enter the index of the pod: "))
        selected_pod_name = pods[pod_index].metadata.name

        pod = api.read_namespaced_pod(name=selected_pod_name, namespace=selected_namespace)
        print(f"\nPod name: {pod.metadata.name}")
        print(f"Pod namespace: {pod.metadata.namespace}")
        print(f"Pod status: {pod.status.phase}")
        print(f"Pod IP: {pod.status.pod_ip}")
        print(f"Pod host IP: {pod.status.host_ip}")
        print(f"Pod start time: {pod.status.start_time}")
        print(f"Pod container images: {pod.spec.containers[0].image}")
        print(f"Pod container ports: {pod.spec.containers[0].ports}")
        print("--------------------------------------------------")



    except ApiException as e:
        print(f"Exception when describing pod: {e}")
    except IndexError:
        print("Invalid index selected.")
    except ValueError:
        print("Invalid input, please enter a number.")
   
    
    
    

#option 3; create a deployment in a namespace with nginx or busybox image
def create_deployment():
    namespaces = api.list_namespace()
    for ns in namespaces.items:
       print("Namespaces available: ")
       print(ns.metadata.name)

    namespace = input("Enter namespace for the deployment: ")
    name = input("Enter deployment name: ")
    image = input("Enter image: 1) nginx:1.22.1 or 2) busybox:1.34.1): ")
    if image == "1":
        image = "nginx:1.22.1"
    elif image == "2":
        image = "busybox:1.34.1"
    replicas = 2  # Default number of replicas

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector={'matchLabels': {'app': name}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={'app': name}),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(name=name, image=image)
                ])
            )
        )
    )

    try:
        apps_api.create_namespaced_deployment(namespace=namespace, body=deployment)
        print(f"Deployment {name} created.")
    except ApiException as e:
        print(f"Exception when creating deployment: {e}")

#option 4; scale a deployment in a namespace
def scale_deployment():
    
    deployments = list_all_deployments()
    if not deployments:
        print("No deployments found, exiting.")
        return

    try:

        index = int(input("Enter the index of the deployment you want to scale: "))
        if index < 0 or index >= len(deployments):
            raise ValueError("Invalid index")

        selected_deployment = deployments[index]
        namespace = selected_deployment["namespace"]
        deployment_name = selected_deployment["name"]

        replicas = int(input("Enter number of replicas (1-5): "))

        scale = client.V1Scale(
            spec=client.V1ScaleSpec(replicas=replicas)
        )
        apps_api.patch_namespaced_deployment_scale(name=deployment_name, namespace=namespace, body=scale)
        print(f"Deployment {deployment_name} in namespace {namespace} scaled to {replicas} replicas.")
    except ApiException as e:
        print(f"Exception when scaling deployment: {e}")

#option 5; execute a command in a pod
def execute_command_in_pod():
    try:
        # List all pods in all namespaces
        pods = api.list_pod_for_all_namespaces(watch=False)
        print("Pods available:")
        for i, pod in enumerate(pods.items):
            print(f"{i}. {pod.metadata.name} in {pod.metadata.namespace}")

        # User input for selecting a pod
        pod_index = int(input("Enter the number of the pod to execute command: "))
        selected_pod = pods.items[pod_index]

        # User input for command
        command = input("Enter the command to execute (e.g., 'ls /'): ").split()
        namespace = selected_pod.metadata.namespace
        pod_name = selected_pod.metadata.name

        # Executing command in the selected pod
        resp = stream.stream(api.connect_get_namespaced_pod_exec,
                             pod_name,
                             namespace,
                             command=command,
                             stderr=True, stdin=False,
                             stdout=True, tty=False)
        print(f"Command output: {resp}")
    except ApiException as e:
        print(f"Exception when accessing Kubernetes API: {e}")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except IndexError as ie:
        print(f"Selected pod index is out of range: {ie}")

#option 6; perform a rolling update on a deployment in a namespace
def rolling_update_deployment():
    
    deployments = list_all_deployments()
    if not deployments:
        print("No deployments found, exiting.")
        return

    try:
        index = int(input("Enter the index of the deployment you want to update: "))
        if index < 0 or index >= len(deployments):
            raise ValueError("Invalid index")
        

        selected_deployment = deployments[index]
        namespace = selected_deployment["namespace"]
        deployment_name = selected_deployment["name"]

        print("Select the image to update:")
        print("1) Nginx 1.22.3")
        print("2) BusyBox 1.34.1")
        image_choice = input("Enter your choice (1 or 2): ")

        if image_choice == "1":
            image = "nginx:1.25.3"
        elif image_choice == "2":
            image = "busybox:1.36.1"
        else:
            print("Invalid choice, exiting.")
            return


        # Get the deployment
        deployment = apps_api.read_namespaced_deployment(name=deployment_name, namespace=namespace)

        # Update the image of the deployment
        deployment.spec.template.spec.containers[0].image = image

        # Perform the rolling update
        apps_api.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

        # Re-fetch the deployment to confirm the update
        updated_deployment = apps_api.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        running_image = updated_deployment.spec.template.spec.containers[0].image

        print(f"Deployment {deployment_name} updated.")
        print(f"Running image: {running_image}")


    except ApiException as e:
        print(f"Exception when updating deployment: {e}")

#option 7; delete a deployment in a namespace
def delete_deployment():
    deployments = list_all_deployments()
    if not deployments:
        print("No deployments found, exiting.")
        return
    try:


        index = int(input("Enter the index of the deployment you want to delete: "))
        if index < 0 or index >= len(deployments):
            raise ValueError("Invalid index")
        selected_deployment = deployments[index]
        namespace = selected_deployment["namespace"]
        deployment_name = selected_deployment["name"]

        apps_api.delete_namespaced_deployment(name=deployment_name, namespace=namespace)
        print(f"Deployment {deployment_name} deleted.")
    except ApiException as e:
        print(f"Exception when deleting deployment: {e}")


#option 8; create pods on every worker node
def create_pods_on_each_node():
    try:
        # List all nodes in the cluster
        nodes = api.list_node()
        # Filter out master nodes
        worker_nodes = [node for node in nodes.items if 'node-role.kubernetes.io/master' not in node.metadata.labels]

        # List all namespaces and select one
        namespaces = list_namespaces()
        ns_index = int(input("Enter the index of the namespace: "))
        selected_namespace = namespaces[ns_index].metadata.name

        # Image selection
        image = input("Enter image for the pod 1) alpine:3.19 or 2)redis: 7 ")
        if image == "1":
            image = "alpine:3.19"
        elif image == "2":
            image = "redis:7"
        else:
            print("Invalid image selection, exiting.")
            return

        # Base name for the pods
        pod_base_name = input("Enter base name for the pods: ")

        # Create a pod on each worker node
        for i, node in enumerate(worker_nodes):
            pod_name = f"{pod_base_name}-{i}"
            pod_body = client.V1Pod(
                api_version="v1",
                kind="Pod",
                metadata=client.V1ObjectMeta(name=pod_name),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(name=pod_name, image=image)],
                    node_name=node.metadata.name  # Schedule Pod on this specific node
                )
            )
            api.create_namespaced_pod(namespace=selected_namespace, body=pod_body)
            print(f"Pod {pod_name} created on node {node.metadata.name}")

    except client.rest.ApiException as e:
        print(f"Exception when creating pods: {e}")






#this is integrated with the main menu to list all the images in all namespaces for option 8.
def list_images(namespace):
    # Fetch all pods in the specified namespace
    pods = api.list_namespaced_pod(namespace)

    # Extract the images
    images = []
    for pod in pods.items:
        for container in pod.spec.containers:
            images.append(container.image)

    # Remove duplicates and return the list
    return list(set(images))



#************************************PART 2 ***************************************



#running the command to apply the yaml file
def apply_yaml(yaml_file):
    try:
        subprocess.run(["kubectl", "apply", "-f", yaml_file], check=True)
        print(f"Successfully applied {yaml_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error applying {yaml_file}: {e}")

#List of pods to output the new pods
def list_of_pods_without_index(namespace):
    pods = []

    try:
        pod_list = api.list_namespaced_pod(namespace=namespace).items
        for pod in pod_list:
            pods.append(pod.metadata.name)
    except Exception as e:
        print(f"Error listing pods: {e}")

    return pods

#List of services to output the new load balancer service
def list_services(namespace):
    config.load_kube_config()  # Load Kubernetes configuration
    services = []

    try:
        svc_list = api.list_namespaced_service(namespace=namespace).items
        for svc in svc_list:
            # Only include services with a type of LoadBalancer
            services.append(svc.metadata.name)
    except Exception as e:
        print(f"Error listing services: {e}")

    return services

def create_kube_resources():
    # Apply the pod deployment YAML
    apply_yaml("pods.yaml")

    print("Creating pods...")

    # List and print the names of new pods; this list_all_pods function was created earlier in the code
    new_pods = list_of_pods_without_index("default")
    print("Pods created:")
    for pod_name in new_pods:
        print(pod_name)

    # Apply the LoadBalancer service YAML
    apply_yaml("loadbalancer-service.yaml")

    # List and print the names of new services
    new_services = list_services("default")
    print("Services created:")
    for svc_name in new_services:
        print(svc_name)

#main menu to display the options
def main_menu():
    actions = {
        "1": list_pods,
        "2": describe_pod,
        "3": create_deployment,
        "4": scale_deployment,
        "5": execute_command_in_pod,
        "6": rolling_update_deployment,
        "7": delete_deployment,
        "8": create_pods_on_each_node,
        "9": create_kube_resources,

    }
    
    while True:
        print("\nKubernetes Management Menu:")
        print("1. List all pods")
        print("2. Describe a pod")
        print("3. Create a deployment")
        print("4. Scale a deployment")
        print("5. Execute command in a pod")
        print("6. Create a rolling update")
        print("7. Delete a deployment")
        print("8. Create pods on every worker node")
        print("9. Create pods and services")
        print("10. Exit")
        choice = input("Enter your choice: ")

        if choice == "10":
            print("Exiting the program.")
            break
        elif choice in actions:
            try:
               actions[choice]()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice. Please enter a number between 1-10.")

if __name__ == "__main__":
    main_menu()
