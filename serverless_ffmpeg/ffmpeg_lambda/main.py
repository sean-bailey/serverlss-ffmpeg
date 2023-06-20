import boto3
import os
import subprocess
import tempfile
import time
import uuid

s3_client = boto3.client('s3')

def handler(event, context):
    # get bucket name and file key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    download_path = os.path.join(tempfile.gettempdir(), key)

    print(download_path)

    # download file
    s3_client.download_file(bucket, key, download_path)

    #Get the extension
    basename, extension = os.path.splitext(download_path)
    basename=basename+str(time.time())+str(uuid.uuid4()).replace("-","").replace("_","")
    starttime=time.time()
    # process the file with ffmpeg
    output_path = f"{basename}.webm"
    print(output_path)


    

    #-f mpegts -c:v copy -af aresample=async=1:first_pts=0
    subprocess.check_output(['ffmpeg','-y', '-i', download_path, '-c','copy', output_path])
    endtime=time.time()
    timedelta=endtime-starttime
    print(timedelta)
    # upload the processed file
    s3_client.upload_file(output_path, bucket, f'{basename}.webm')
