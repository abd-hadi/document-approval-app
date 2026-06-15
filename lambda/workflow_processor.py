import json
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DocumentApprovals")

def handler(event, context):
    for record in event.get("Records", []):
        body = json.loads(record["body"])
        document_id = body.get("documentId")

        table.put_item(
            Item={
                "documentId": document_id,
                "status": "SUBMITTED",
                "action": body.get("action", "submitted"),
                "processedAt": datetime.now(timezone.utc).isoformat()
            }
        )

        print(f"Saved document approval record: {document_id}")

    return {"status": "processed"}
