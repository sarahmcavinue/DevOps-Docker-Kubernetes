import boto3
import os

class S3Controller:
    """
    Amazon S3 Controller

    This class manages S3 operations including listing buckets and objects, uploading, downloading, and deleting objects and buckets.
    """

    def __init__(self, s3resource):
        self.s3 = s3resource

    def list_buckets(self):
        # List all buckets
        for bucket in self.s3.buckets.all():
            print("\nBucket Name:", bucket.name)
            print("Creation Date:", bucket.creation_date)
            print("*************************************************\n")

    def list_objects(self):
        try:
            for bucket in self.s3.buckets.all():
                print("\n", bucket.name)
                print("*************************************************\n")

            bucket_name = input("Enter the bucket name you wish to list objects from: ").strip()
            bucket = self.s3.Bucket(bucket_name)
            # List all objects in the selected bucket
            for obj in bucket.objects.all():
                print("\nObject Key:", obj.key)
                print("Last Modified:", obj.last_modified)
                print("Size:", obj.size)
                print("*************************************************\n")
        except self.s3.meta.client.exceptions.NoSuchBucket:
            print(f"Bucket {bucket_name} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def upload_object(self):
        try:
            for bucket in self.s3.buckets.all():
                print("\n", bucket.name)
                print("*************************************************\n")
            bucket_name = input("Enter the bucket name you wish to upload your object to: ").strip()
            object_name = input("Enter the name of the object you wish to upload: ").strip()
            file_name = input("Enter the path of the file you wish to upload: ").strip()
            
            if not object_name:
                object_name = file_name

            self.s3.Bucket(bucket_name).upload_file(file_name, object_name)
            print(f"Uploaded {file_name} to {bucket_name}")
        except FileNotFoundError:
            print(f"File {file_name} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def bucket_exists(self, bucket_name):
        # Check if the bucket exists
        for bucket in self.s3.buckets.all():
            if bucket.name == bucket_name:
                return True
        return False
    
    def object_exists(self, bucket_name, object_name):
        # Check if the object exists
        for obj in self.s3.Bucket(bucket_name).objects.all():
            if obj.key == object_name:
                return True
        return False

    def download_object(self):
        try:
            for bucket in self.s3.buckets.all():
                print("\n", bucket.name)
                print("*************************************************\n")

            bucket_name = input("Enter the bucket name you wish to download your object from: ").strip()

            if not self.bucket_exists(bucket_name):
                print(f"Bucket '{bucket_name}' does not exist.")
                return

            for obj in self.s3.Bucket(bucket_name).objects.all():
                print("\n", obj.key)
                print("*************************************************\n")

            object_key_name = input("Enter the name of the object you wish to download: ").strip()
            if not self.object_exists(bucket_name, object_key_name):
                print(f"Object '{object_key_name}' does not exist in bucket '{bucket_name}'.")
                return

            file_name_path_to_store = input("Enter the path of the file you wish to download to: ").strip()
            self.s3.Bucket(bucket_name).download_file(object_key_name, file_name_path_to_store)
            print(f"Downloaded {object_key_name} from {bucket_name} to {file_name_path_to_store}")
        except FileNotFoundError:
            print(f"File {file_name_path_to_store} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_bucket(self):
        try:
            for bucket in self.s3.buckets.all():
                print("\n List of Buckets: ", bucket.name)
                print("*************************************************\n")

            bucket_name = input("Enter the bucket name you wish to delete: ").strip()

            if not self.bucket_exists(bucket_name):
                print(f"Bucket '{bucket_name}' does not exist.")
                return

            objects_to_display = self.s3.Bucket(bucket_name).objects.all()
            print("List of objects in the bucket: ")
            for obj in objects_to_display:
                print(obj.key)

            confirmation = input("Are you sure you want to delete all objects and the bucket? (yes/no): ")
            if confirmation.lower() == 'yes':
                for obj in objects_to_display:
                    print(f"Deleting object {obj.key}...")
                    self.s3.Object(bucket_name, obj.key).delete()

                self.s3.Bucket(bucket_name).delete()
                print(f"Bucket {bucket_name} deleted.")
        except self.s3.meta.client.exceptions.NoSuchBucket:
            print(f"Bucket {bucket_name} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def s3_menu(self):
        while True:
            print("\nAWS S3 Bucket Operations Menu")
            print("1. List all buckets")
            print("2. List all objects in a bucket")
            print("3. Upload an object to a bucket")
            print("4. Download an object from a bucket to a selected file path")
            print("5. Delete a bucket")
            print("6. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.list_buckets()
            elif choice == "2":
                self.list_objects()
            elif choice == "3":
                self.upload_object()
            elif choice == "4":
                self.download_object()
            elif choice == "5":
                self.delete_bucket()
            elif choice == "6":
                print("Exiting the menu.")
                break
            else:
                print("Invalid choice. Please try again.")

