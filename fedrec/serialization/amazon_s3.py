from abc import ABC, abstractmethod
import os
import yaml
import boto3
import pandas as pd
import torch
import botocore

class AbstractDatabaseManager(ABC):
    

    def __init__(self):

        pass

    
    @abstractmethod
    def download(self):
        raise NotImplementedError("Database interface not defined.")

    @abstractmethod
    def upload(self):
        raise NotImplementedError("Database interface not defined.")

    @abstractmethod
    def update(self):
        raise NotImplementedError("Database interface not defined.")

    @abstractmethod
    def delete(self):
        raise NotImplementedError("Database interface not defined.")





"""
    TODO: Make the whole FL service independent of local system. All the io operations should be done via S3 only.
"""

class S3Interface(AbstractDatabaseManager):

  
    def __init__(self,
                region=None,
                aws_access_key=None,
                aws_secret_access_key=None,
                storage=None,
                bucket=None
                ):
        
        self.region = region
        self.storage = storage
        self.s3 = boto3.resource(
                service_name='s3',
                region_name=region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_access_key
        )

        
        self.bucket_name = bucket
        self.bucket = None
        self.current_buckets = None
        try:
            self.bucket = self.s3.Bucket(bucket)
            self.current_buckets = [bucket.name for bucket in self.s3.buckets.all()]
        
        except Exception as e:
            print(e)
        
        print(self.current_buckets)
        pass



    
    def listAllBuckets(self):
        if self.current_buckets == None:
            raise Exception("Info not available.")

        for b in self.current_buckets:
            print(b)
  


    def download(self, file_key: str):
        """

        """
        #condition to check if s3 is connected
        if self.current_buckets == None : 
            raise Exception("Error connecting to database.")
        
        #Extract Group of device and model we need to fetch
        
        filePath = self.storage + file_key
        
        self.bucket.download_file(
            Key=file_key, Filename=filePath
        )

        return filePath



    def upload(self, file_path: str, file_key: str):
        if self.current_buckets == None:
            raise Exception("Error connecting to database.")
        

        self.bucket.upload_file(Filename=file_path, Key=file_key)
        #os.remove(file_path) 


  
    def update(self,file_path:str, file_key:str):
        if self.current_buckets == None:
            raise Exception("Error connecting to database.")

        self.upload(file_path, file_key)


    def delete(self, file_key: str):
        if self.current_buckets == None:
            raise Exception("Error connecting to database.")
        

        self.s3.Object(self.bucket_name, file_key).delete()

    def list_all_files(self, dir_name: str) -> list :

        """
            dir_name should end in '/'
        """

        obj_summary = self.bucket.objects.filter(Prefix=dir_name)
        keys = []
        for obj in obj_summary :
            key = str(obj.key).replace(dir_name, '')
            if key != '':
                keys.append(key)
        
        return keys

    def check_file_exists(self, file_key:str) -> bool :

        try:
            self.s3.Object(self.bucket_name, file_key).load()
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 404 :
                return False
            else :
                raise


    def create_empty_dir(self, dir_name: str) :

        if self.bucket == None:
            raise Exception("Error connecting to datbase.")
        
        self.bucket.upload_file(Filename='/path/to/any/file', Key=dir_name)


    def empty_dir(self, dir_name: str):

        if self.bucket == None:
            raise Exception("Error connecting to database.")
        
        keys = self.list_all_files(dir_name)
        for key in keys:
            self.delete(dir_name + key)