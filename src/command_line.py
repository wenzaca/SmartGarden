#!/usr/bin/env python3

import os
import argparse
import boto3

if os.path.isdir('log') is False:
    os.mkdir('log')


def download_certificate(profile_name, s3_bucket, region):
    session = boto3.session.Session(profile_name=profile_name)
    s3 = session.client('s3', region_name=region)
    if os.path.isdir('./certs') is False:
        os.mkdir('./certs')
        s3.download_file(s3_bucket, 'rootca.pem', './certs/rootca.pem')
        s3.download_file(s3_bucket, 'certificate.pem.crt', './certs/certificate.pem.crt')
        s3.download_file(s3_bucket, 'private.pem.key', './certs/private.pem.key')


def main():
    parser = argparse.ArgumentParser("smart_garden", description="WebServer stater point for Smart Garden")
    parser.add_argument("--s3-bucket", '-b', help="The S3 Bucket where the certificates were uploaded", type=str,
                        required=True, metavar='bucket/name/and/folder')
    parser.add_argument("--profile_name", '-u', help="The Credential User", type=str, required=False,
                        default='default', metavar='default')
    parser.add_argument("--aws_region", '-r', help="The Bucket and the AWS IoT Region", type=str, required=False,
                        default='us-east-1', metavar='us-east-1')
    parser.add_argument("--port", '-p', help="The port that you want this server to run", type=int, required=False,
                        default=80, metavar='80')
    args = parser.parse_args()
    download_certificate(args.profile_name, args.s3_bucket, args.aws_region)
    from src.flaskapp import app

    app.run(host='127.0.0.1', port=args.port, use_reloader=False, debug=False)



