import boto3
from dateutil import parser
from datetime import datetime, timezone, timedelta
from config import DAYS_OLD, REGION

def delete_old_versions(bucket_name, days_old=DAYS_OLD):
    s3 = boto3.client('s3', region_name=REGION)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)

    print(f"\n🔍 Looking for object versions older than {days_old} days in '{bucket_name}'...")
    paginator = s3.get_paginator('list_object_versions')

    deleted = 0
    for page in paginator.paginate(Bucket=bucket_name):
        versions = page.get('Versions', []) + page.get('DeleteMarkers', [])
        for version in versions:
            last_modified = version['LastModified']
            if last_modified < cutoff:
                print(f"🗑 Deleting: {version['Key']} (Version: {version['VersionId']})")
                s3.delete_object(Bucket=bucket_name, Key=version['Key'], VersionId=version['VersionId'])
                deleted += 1

    print(f"✅ Deleted {deleted} old object versions.\n")

def delete_incomplete_uploads(bucket_name, days_old=DAYS_OLD):
    s3 = boto3.client('s3', region_name=REGION)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)

    print(f"\n🔍 Checking for incomplete multipart uploads older than {days_old} days...")
    uploads = s3.list_multipart_uploads(Bucket=bucket_name).get('Uploads', [])

    deleted = 0
    for upload in uploads:
        if upload['Initiated'] < cutoff:
            print(f"🗑 Aborting upload: {upload['Key']} (UploadId: {upload['UploadId']})")
            s3.abort_multipart_upload(Bucket=bucket_name, Key=upload['Key'], UploadId=upload['UploadId'])
            deleted += 1

    print(f"✅ Aborted {deleted} multipart uploads.\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AWS S3 Cleaner")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("--days", type=int, default=DAYS_OLD, help="Number of days to consider old")
    parser.add_argument("--versions", action="store_true", help="Delete old object versions")
    parser.add_argument("--uploads", action="store_true", help="Delete incomplete multipart uploads")

    args = parser.parse_args()

    if args.versions:
        delete_old_versions(args.bucket, args.days)
    if args.uploads:
        delete_incomplete_uploads(args.bucket, args.days)

    if not args.versions and not args.uploads:
        print("❗️Please specify at least one operation: --versions or --uploads")
