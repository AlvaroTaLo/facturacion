# Sistema de Facturación

Este es un sistema de facturación desarrollado con Python, utilizando FastAPI para el backend y PostgreSQL como base de datos.

## Requisitos

- Python 3.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd facturacion
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
   - Crear una base de datos PostgreSQL llamada `facturacion`
   - Modificar el archivo `.env` con las credenciales correctas de la base de datos

5. Crear las carpetas necesarias:
```bash
mkdir templates
mkdir generated_pdfs
```

## Uso

1. Iniciar el servidor:
```bash
python main.py
```

2. La API estará disponible en `http://localhost:8000`

3. Documentación de la API:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Endpoints principales

- `POST /clientes/`: Crear un nuevo cliente
- `GET /clientes/`: Listar todos los clientes
- `GET /clientes/{cliente_id}`: Obtener detalles de un cliente
- `POST /facturas/{cliente_id}`: Generar una nueva factura para un cliente

## Estructura del proyecto

```
facturacion/
├── main.py           # Archivo principal de la aplicación
├── models.py         # Modelos de la base de datos
├── config.py         # Configuraciones
├── pdf_generator.py  # Generador de PDFs
├── requirements.txt  # Dependencias
├── .env             # Variables de entorno
├── templates/       # Plantillas para facturas
└── generated_pdfs/  # PDFs generados
```

## Configuración

Modifica el archivo `.env` con tus configuraciones:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/facturacion
SECRET_KEY=your-secret-key-here
TEMPLATES_DIR=templates
PDF_OUTPUT_DIR=generated_pdfs
```

## Notas

- Asegúrate de cambiar la SECRET_KEY en producción
- Los PDFs generados se guardan en la carpeta `generated_pdfs`
- Las plantillas de facturas deben colocarse en la carpeta `templates` 