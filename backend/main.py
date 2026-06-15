import os
import json
import uuid
import boto3
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client("s3")
sqs = boto3.client("sqs")

QUEUE_URL = os.environ.get("SQS_QUEUE_URL")
S3_BUCKET = os.environ.get("S3_BUCKET")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    uploadedBy: str = Form(...)
):
    document_id = str(uuid.uuid4())
    s3_key = f"documents/{document_id}-{file.filename}"

    s3.upload_fileobj(file.file, S3_BUCKET, s3_key)

    message = {
        "documentId": document_id,
        "documentName": file.filename,
        "uploadedBy": uploadedBy,
        "s3Bucket": S3_BUCKET,
        "s3Key": s3_key,
        "action": "submitted"
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    return {
        "message": "Document uploaded and submitted for approval",
        "documentId": document_id,
        "fileName": file.filename,
        "s3Key": s3_key
    }
