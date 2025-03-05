from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Cliente, Factura, LineaFactura
from config import settings
import os
from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Facturación")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response
class ClienteBase(BaseModel):
    nombre: str
    nif: str
    direccion: str
    codigo_postal: str
    ciudad: str
    pais: str
    email: str
    telefono: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True

# Routes
@app.post("/clientes/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    try:
        db.commit()
        db.refresh(db_cliente)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el cliente")
    return db_cliente

@app.get("/clientes/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@app.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.post("/facturas/{cliente_id}")
def generar_factura(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Aquí iría la lógica para generar el PDF de la factura
    # usando la plantilla y los datos del cliente
    
    # Por ahora, solo creamos un registro de factura
    nueva_factura = Factura(
        cliente_id=cliente_id,
        numero_factura=f"F-{datetime.now().strftime('%Y%m%d')}-{cliente_id}",
        fecha_emision=datetime.now(),
        base_imponible=0.0,  # Estos valores deberían venir del request
        iva=0.0,
        total=0.0
    )
    
    db.add(nueva_factura)
    db.commit()
    
    return {"message": "Factura generada correctamente", "factura_id": nueva_factura.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 