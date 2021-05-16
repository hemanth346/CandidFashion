from __future__ import absolute_import
import json, os, io
import cv2
from pathlib import Path
import boto3
from botocore.client import BaseClient

import torch

# import torchvision.transforms as T
# from torchvision.transforms import Compose
import torch.nn.functional as F
from pathlib import Path

from utils import setup_logger, image2b64

logger = setup_logger(__name__)

CLASSES = ['tops_or_shirt', 'toursers_or_skirts', 'dress']


def fetch_apparel(image, mask):
    apparels = {}
    for ax in range(mask.shape[-1]):
        m = mask[:,:,ax]
        roi = cv2.bitwise_and(image, image, mask=m)
        if m.any(): # add only if class is present
            title = CLASSES[ax]
            roi[roi < 1] = 255 # make background white
            roi = image2b64(roi)# encode image
            apparels[title] = roi
    return apparels 


def detect_apparel(image, model_name='best_model.pt', classes=CLASSES):

    if 'PRODUCTION' in os.environ:
        logger.info(f"=> Loading {model_name} from S3")
        s3: BaseClient = boto3.client('s3')
        obj = s3.get_object(Bucket=os.environ['S3_BUCKET'], Key=(model_name))
        bytestream = io.BytesIO(obj['Body'].read())
        model = torch.jit.load(bytestream)
    else:
        logger.info(f"=> Loading {model_name} from Local")
        model = torch.jit.load(str((Path('models') / model_name)))

    trans: Compose = T.Compose([
        T.Resize(480, 720),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    img_tensor = trans(image).unsqueeze(0)
    predicted_segment_mask = model.predict(img_tensor).squeeze() # will be multiple axis images
    return predicted_segment_mask
    # tops_or_shirt_mask,  toursers_or_skirts_mask, dress_mask= [mask for mask in predicted_mask]
