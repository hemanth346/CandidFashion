from __future__ import absolute_import

import os
import bz2
import urllib.request
import boto3
from botocore.client import BaseClient
import credentials
from utils import setup_logger

# Names
BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', credentials.AWS_BUCKET_NAME)

# S3 Connection
S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', credentials.AWS_ACCESS_KEY),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', credentials.AWS_SECRET_ACCESS_KEY)
)

logger = setup_logger(__name__)


def download_models(S3_CLIENT=S3_CLIENT):
    s3: BaseClient = S3_CLIENT
    models = ['best_model.pt']
    for model in models:
        model_path = f'./models/{model}'
        if not os.path.exists(model_path):
            logger.info(f'=> Downloading {model} from S3 Bucket')
            s3.download_file(os.environ['S3_BUCKET'], model, model_path)
