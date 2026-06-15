def handler(event, context):
    print("Escalating pending approvals")
    return {"status":"done"}