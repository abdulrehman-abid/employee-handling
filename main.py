from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API WORKING", "setup": "COMPLETE"}

@app.get("/health")
def health():
    return {"status": "ok"}