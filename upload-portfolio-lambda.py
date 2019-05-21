import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:450629874875:Portfolio_Deployments')

    location = {
        "bucketName": 'portfoliobuild.anirudhpillutla.info',
        "objectKey": 'portfoliobuild.zip'
    }
    try:
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "BuildArtifact":
                    location = artifact["location"]["s3Location"]
        print ("Building Portfolio from " + str(location))


        s3 = boto3.resource('s3')
        portfolio_bucket = s3.Bucket('portfolio.anirudhpillutla.info')
        build_bucket = s3.Bucket(location["bucketName"])

        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj(location["objectKey"],portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print ("Job Done")
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio Deployed Successfully")

        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
        else:
            codepipeline.boto3.client('codepipeline')
            codepipeline.put_job_failure_result(jobId=job["id"])

    except:
        topic.publish(Subject="Portfolio Deployment Failed", Message="Portfolio Deployment Unsuccessful")
        raise

    return "Inside Lambda Function"
