from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    Size,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as aws_lambda,
    aws_logs as logs,
    aws_s3 as s3,
    CfnOutput,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_s3_notifications as s3n,
    
    
)
import uuid
import time



bucketname="ffmpeg-bucket-"+str(uuid.uuid4()).split("-")[0]+str(time.time())

class ServerlessFfmpegStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ffmpegbucket = s3.Bucket(
            self, id=bucketname+"-id1", bucket_name=bucketname,
            enforce_ssl=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            auto_delete_objects=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            lifecycle_rules=[{"expiration":Duration.days(1)}]
        )

        #----------------------------------GENERATE IMAGE-----------------------------------------------------
        ffmpeg_lambda_function_name="ffmpeg_lambda_function"

        ffmpeg_lambda_role=iam.Role(
            self,
            id="ffmpeg_lambda_role",
            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com")
        )

        ffmpeg_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        ffmpeg_lambda_function=aws_lambda.DockerImageFunction(self,ffmpeg_lambda_function_name,
        architecture=aws_lambda.Architecture.ARM_64,
        timeout=Duration.seconds(300),
        log_retention=logs.RetentionDays.ONE_WEEK,
        environment={
        "NUMBA_CACHE_DIR":"/tmp/cache1",
        "BUCKET":bucketname,
        "STAGE":"",
        },
        ephemeral_storage_size=Size.mebibytes(2048),
        memory_size=4000,
        retry_attempts=0,
        role=ffmpeg_lambda_role,
        code=aws_lambda.DockerImageCode.from_image_asset("./ffmpeg_lambda"),
        )

        ffmpegbucket.grant_read_write(ffmpeg_lambda_function)


        ffmpegbucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(ffmpeg_lambda_function))


