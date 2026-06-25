from fastapi import FastAPI, UploadFile, File, Depends
from sqlmodel import Session
import database, models
import storage_client

app = FastAPI(title="ExtractIQ API")

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.post("/test-upload/")
def test_upload(file: UploadFile = File(...), session: Session = Depends(database.get_session)):
    # 1. Read the uploaded file
    file_bytes = file.file.read()
    filename = file.filename
    
    # 2. Upload to Supabase Storage
    public_url = storage_client.upload_to_storage(file_bytes, filename) # <--- CHANGED THIS
    
    # 3. Save record to Neon Postgres
    db_doc = models.Document(
        filename=filename,
        s3_url=public_url, # We still call it s3_url in the DB to avoid changing the schema
        status="PENDING"
    )
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)
    
    return {
        "message": "Successfully connected to Supabase and Neon!",
        "document_id": db_doc.id,
        "filename": db_doc.filename,
        "public_url": db_doc.s3_url, # Now it's a direct link!
        "status": db_doc.status
    }

@app.get("/documents/")
def get_documents(session: Session = Depends(database.get_session)):
    docs = session.query(models.Document).all()
    return docs