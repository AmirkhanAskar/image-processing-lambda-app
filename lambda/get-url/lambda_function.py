import boto3
import json

s3 = boto3.client('s3')
INPUT_BUCKET = 'imgproc-input-cc-2025-new'

def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    
    # CORS preflight
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

    try:
        params = event.get("queryStringParameters") or {}
        filename = params.get("filename")

        if not filename:
            raise ValueError("Missing 'filename' parameter")

        url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': INPUT_BUCKET, 'Key': filename},
            ExpiresIn=120,
            HttpMethod='PUT'
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"upload_url": url})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }
