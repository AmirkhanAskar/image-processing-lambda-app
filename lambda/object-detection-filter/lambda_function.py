import boto3
import cv2
import json
import numpy as np
import os
import tempfile

s3 = boto3.client('s3')

# CORS headers
cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "*",
    "Content-Type": "application/json"
}

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps("CORS preflight passed")
        }

    # Get the image key from query params
    key = event.get("queryStringParameters", {}).get("key")
    if not key:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'key' in query parameters."}),
            "headers": cors_headers
        }

    input_bucket = "imgproc-input-cc-2025-new"
    output_bucket = "imgproc-output-cc-2025-new"

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.jpg")
        output_path = os.path.join(tmpdir, "output.jpg")

        # Download image from S3
        try:
            s3.download_file(input_bucket, key, input_path)
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to download image: {str(e)}"}),
                "headers": cors_headers
            }

        # Load image using OpenCV
        image = cv2.imread(input_path)
        if image is None:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to load image."}),
                "headers": cors_headers
            }

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detected_objects = []

        # Load Haar cascades
        face_cascade = cv2.CascadeClassifier("/opt/python/cv2/data/haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("/opt/python/cv2/data/haarcascade_eye.xml")
        smile_cascade = cv2.CascadeClassifier("/opt/python/cv2/data/haarcascade_smile.xml")

        # Detect objects
        if not face_cascade.empty():
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            detected_objects += ["face"] * len(faces)

        if not eye_cascade.empty():
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in eyes:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            detected_objects += ["eye"] * len(eyes)

        if not smile_cascade.empty():
            smiles = smile_cascade.detectMultiScale(gray, 1.7, 22)
            for (x, y, w, h) in smiles:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            detected_objects += ["smile"] * len(smiles)

        if not detected_objects:
            detected_objects.append("No objects detected")

        # Save annotated image to output path
        try:
            cv2.imwrite(output_path, image)
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to save output image: {str(e)}"}),
                "headers": cors_headers
            }

        # Upload to output bucket with same key
        try:
            s3.upload_file(output_path, output_bucket, key)
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to upload image to output bucket: {str(e)}"}),
                "headers": cors_headers
            }

        # Return key and detected objects
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({
                "output_key": key,
                "objects": detected_objects
            })
        }
