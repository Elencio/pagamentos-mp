import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import pagamento, webhook, auth  # Import the auth router
from .seed import run_seed
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

run_seed()

def create_admin():
    from sqlalchemy.orm import Session
    from .database import SessionLocal
    from . import models
    from .auth import get_password_hash
    
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123") 
            admin_user = models.User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash(admin_password),
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created")
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

create_admin()

app = FastAPI(title="API de Pagamentos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["auth"])  
app.include_router(pagamento.router, prefix="/api", tags=["pagamentos"])
app.include_router(webhook.router, prefix="/api", tags=["webhook"])

@app.get("/")
def root():
    return {"message": "API de Pagamentos funcionando!"}