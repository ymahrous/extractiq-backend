from models import User, Document, Extraction
from auth import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

TEST_ENGINE = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=TEST_ENGINE)

def test_signup(client):
    response = client.post("/api/v1/auth/signup", json={
        "username": "testuser@edocai.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_login_success(client):
    with TestingSessionLocal() as session:
        user = User(
            username="login@test.com",
            hashed_password=get_password_hash("password123")
        )
        session.add(user)
        session.commit()
        
    response = client.post("/api/v1/auth/login", json={
        "username": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "login@test.com",
        "password": "wrongpassword" # Assuming your backend validates input and returns 422
    })
    assert response.status_code == 401 # Changed from 401 to 422

def test_signup_duplicate_email(client):
    client.post("/api/v1/auth/signup", json={
        "username": "dup@test.com",
        "password": "password123"
    })
    
    response = client.post("/api/v1/auth/signup", json={
        "username": "dup@test.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_delete_account_removes_related_data(client, monkeypatch):
    monkeypatch.setattr("storage_client.delete_from_storage", lambda filename: None)

    with TestingSessionLocal() as session:
        user = User(
            username="delete-account@test.com",
            hashed_password=get_password_hash("password123"),
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        document = Document(
            filename="account-delete.pdf",
            s3_url="https://example.com/account-delete.pdf",
            status="COMPLETED",
            owner_id=user.id,
        )
        session.add(document)
        session.commit()
        session.refresh(document)

        extraction = Extraction(
            document_id=document.id,
            extracted_data={"invoice_number": "456"},
            confidence_score=0.98,
        )
        session.add(extraction)
        session.commit()

    token_response = client.post("/api/v1/auth/login", json={
        "username": "delete-account@test.com",
        "password": "password123",
    })
    token = token_response.json()["access_token"]

    response = client.delete(
        "/api/v1/auth/delete",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    with TestingSessionLocal() as session:
        assert session.exec(select(User).where(User.id == user.id)).first() is None
        assert session.exec(select(Document).where(Document.id == document.id)).first() is None
        assert session.exec(select(Extraction).where(Extraction.document_id == document.id)).first() is None