# serverlss-ffmpeg


:warning: **FOR EDUCATIONAL PURPOSES ONLY** :warning:

Docker images, code, buildspecs, and guidance provided as proof of concept only and for educational purposes only.



In this repo we have a quick demonstration of deploying a container with FFMPEG installed to AWS Lambda.

The FFMPEG command is simple, it takes in an input video and converts it to a WebM while keeping the same codecs for audio and video. You may modify this to fit your testing needs by modifying the command in `serverless_ffmpeg/ffmepg_lambda/main.py`.


This will deploy a bucket to your AWS account, a Lambda function, and set the function to be triggered each time a file is uploaded to the bucket. Once triggered, it downloads the file to the function, performs the conversion, and then re-uploads it with a new name to the bucket. 


# Deployment

1) Ensure you have `aws-cdk`, `python3`, and an AWS account with appropriate credentials.
2) `cd` into `serverless_ffmpeg`
3) `python3 -m venv .venv`
4) `source .venv activate`
5) `pip3 install -r requirements.txt`
6) `cdk deploy`


# Use

Upload a file to the S3 bucket. Monitor the function. Check the output file once complete!

Note that this will incur charges in your AWS account. It's for demonstration purposes only, please don't use this in a production environment.