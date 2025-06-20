import boto3
import json
import io
from PIL import Image


s3 = boto3.client('s3')

INPUT_BUCKET = 'imgproc-input-cc-2025-new'
OUTPUT_BUCKET = 'imgproc-output-cc-2025-new'

def lambda_handler(event, context):

    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps("CORS OK")
        }


    params = event.get('queryStringParameters') or {}
    key = params.get('key')
    filter_type = params.get('filter', 'greyscale')

    if not key:
        return {"statusCode": 400, "body": "Missing 'key' parameter"}

    try:
        # Get original image
        obj = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
        img = Image.open(obj['Body'])

        # Apply filter
        if filter_type == 'resize':
            img = img.resize((100, 100))

        elif filter_type == 'greyscale':
            img = img.convert('L')

        elif filter_type == 'rotate':
            img = img.rotate(90)

        elif filter_type == 'flip':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        elif filter_type == 'crop':
            w, h = img.size
            img = img.crop((10, 10, w - 10, h - 10))

        elif filter_type == 'format':
            output_format = 'PNG'
        else:  # default to compression
            output_format = img.format or 'JPEG'

        # Save result to buffer
        buffer = io.BytesIO()
        if filter_type == 'format':
            key_out = key.rsplit('.', 1)[0] + '.png'
            img.save(buffer, format='PNG')
        elif filter_type == 'compress':
            key_out = key.rsplit('.', 1)[0] + '_compressed.jpg'
            img.save(buffer, format=output_format, quality=30)
        else:
            key_out = key.rsplit('.', 1)[0] + f'_{filter_type}.jpg'
            img.save(buffer, format='JPEG')

        buffer.seek(0)

        # Upload to output bucket
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=key_out, Body=buffer)

        return {
            "statusCode": 200,
            "body": json.dumps({"output_key": key_out}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}",
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }
