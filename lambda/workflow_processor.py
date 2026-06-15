def handler(event, context):
    for record in event.get("Records", []):
        print("Processing:", record["body"])
    return {"status":"processed"}