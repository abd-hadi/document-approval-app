import os
import json
import uuid
import boto3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqs = boto3.client("sqs")
QUEUE_URL = os.environ.get("SQS_QUEUE_URL")

class DocumentRequest(BaseModel):
    documentName: str
    uploadedBy: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/documents")
def upload_document(request: DocumentRequest):
    document_id = str(uuid.uuid4())

    message = {
        "documentId": document_id,
        "documentName": request.documentName,
        "uploadedBy": request.uploadedBy,
        "action": "submitted"
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    return {
        "message": "Document submitted for approval",
        "documentId": document_id
    }
