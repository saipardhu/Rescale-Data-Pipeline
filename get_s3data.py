import boto3
import os
import pandas as pd
import logging
import datetime

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('sample-spot-prices')
p_dir = '/home/ec2-user/sample_dp/' #Parent directory
d_dir = p_dir + 'data/'  #data directory
add_dir = p_dir + 'added_data/'
log_dir = p_dir + 'logs/'

#Getting the date to use it for log filename
date_object = str(datetime.datetime.now())
ts = date_object.split(".")[0]
ts = ts.split(" ")
ts = ts[0]+"-"+ts[1]



#Create the directories if not exists
if not os.path.exists(p_dir):
	os.mkdir(p_dir)

if not os.path.exists(d_dir):
    os.mkdir(d_dir)

if not os.path.exists(add_dir):
    os.mkdir(add_dir)
	
if not os.path.exists(log_dir):
    os.mkdir(log_dir)



#Read the bucket and download all the csv files
for object in my_bucket.objects.all():
    if(object.key.endswith('.csv') and (not os.path.exists(d_dir+"/"+object.key) or (not os.path.exists(d_dir+"/"+object.key)))):
        logging.basicConfig(filename=log_dir+"log-"+ts+".log",format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        path, filename = os.path.split(object.key)
        logging.warning("Downloading the file {0}\n".format(object.key))
        my_bucket.download_file(object.key, d_dir+"/"+filename)
        data=pd.read_csv(d_dir+"/"+filename) 
        acc_id = filename.split("_")[2] #Get the account id from the filename
        region = filename.split("_")[3].split(".")[0] #Get the region from the filename
        data['Account_id']=acc_id #Creating the column for accountid
        data['Region']=region #Creating the column for region
        colnames=['Account_id','ProductDescription','InstanceType','AvailabilityZone','SpotPrice','Timestamp','Region'] #Reorder the columns in the order of the table column order
        data.reindex(columns=colnames)
        data.to_csv(d_dir+"/"+filename,encoding='utf-8',index=False) #writing the cleaned data to csv
        logging.warning("\nImport Success\n")
        
