from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/documents")
def upload_document():
    return {"message":"Upload endpoint placeholder"}