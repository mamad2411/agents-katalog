# AGENTS.md - AI Agent Guidelines for CRM Project

## Project Overview

This is a CRM (Customer Relationship Management) system built with Python/Flask for managing customers, sales, invoices, accounts, and inventory. The application is written primarily in Spanish and targets Argentine businesses (includes AFIP electronic invoicing integration).

**Tech Stack:**
- **Backend:** Python 3.x, Flask, SQLAlchemy
- **Database:** MySQL
- **Frontend:** Jinja2 templates, Bootstrap 5, jQuery, HTMX, SweetAlert2
- **Key Integrations:** AFIP (Argentine tax authority) for electronic invoicing

## Build/Run/Test Commands

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate         # Windows
source venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python index.py               # Development server on http://localhost:5000

# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_clientes.py

# Run a single test function
pytest tests/test_clientes.py::test_create_cliente

# Run tests with verbose output
pytest -v tests/

# Run tests with print output visible
pytest -s tests/
```

## Project Structure

```
CRM/
├── index.py              # Flask app entry point and configuration
├── models/               # SQLAlchemy ORM models (one file per domain)
├── routes/               # Flask blueprints (route handlers)
├── services/             # Business logic layer
├── utils/                # Configuration, database, helpers, decorators
├── templates/            # Jinja2 HTML templates
│   └── partials/         # Reusable template components
├── static/               # CSS, JS, images, vendor libraries
├── scripts/              # Utility/migration scripts
├── cert_fe/              # Electronic invoicing certificates (gitignored)
└── SQL/                  # Database scripts (gitignored)
```

## Code Style Guidelines

### Language
- **Code comments and documentation:** Spanish
- **Variable/function names:** Spanish (snake_case)
- **User-facing strings:** Spanish

### Python Style
- Follow PEP 8 conventions
- 4-space indentation
- No type hints (not used in this codebase)
- Use `Decimal` for all monetary calculations (never float)

### Import Order
1. Standard library imports
2. Third-party imports (Flask, SQLAlchemy, etc.)
3. Local imports (models, services, utils)

```python
# Example import structure
from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
from sqlalchemy import text, func, and_
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

from models.clientes import Clientes
from services.clientes import save_cliente
from utils.db import db
from utils.utils import check_session
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files | snake_case (Spanish) | `ventas.py`, `clientes.py` |
| Classes/Models | PascalCase (Spanish) | `Clientes`, `Factura`, `Articulo` |
| Functions | snake_case (Spanish) | `save_cliente()`, `get_abc_operaciones()` |
| Variables | snake_case (Spanish) | `idcliente`, `tipo_comprobante`, `total_neto` |
| Blueprints | `bp_` prefix | `bp_clientes`, `bp_ventas` |
| Foreign keys | `id` + entity | `idcliente`, `idlista`, `idsucursal` |
| Boolean vars | `es_` or `con_` prefix | `es_compuesto`, `con_colores` |
| Database tables | lowercase plural | `clientes`, `articulos`, `facturav` |

### Route/Blueprint Pattern

```python
from flask import Blueprint, render_template, request, jsonify, session, g
from utils.utils import check_session
from utils.msg_alertas import alertas_mensajes

bp_clientes = Blueprint('clientes', __name__, template_folder='../templates/clientes')

@bp_clientes.route('/clientes/<id>', methods=['GET', 'POST'])
@check_session              # Required: session validation
@alertas_mensajes           # Optional: alert messages decorator
def clientes(id):
    # Route logic here
    return render_template('clientes.html', 
        data=data,
        alertas=g.alertas,
        cantidadAlertas=g.cantidadAlertas,
        mensajes=g.mensajes,
        cantidadMensajes=g.cantidadMensajes)
```

### Model Pattern

```python
from utils.db import db

class Clientes(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), nullable=False)
    documento = db.Column(db.String(13), nullable=False)
    # Use db.Numeric(20,6) for monetary values
    total = db.Column(db.Numeric(20,6), default=0)
    
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento
```

### Service Pattern

```python
from models.clientes import Clientes
from utils.db import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def save_cliente(nombre, documento):
    """Creates a new customer and returns the ID."""
    cliente = Clientes(nombre, documento)
    db.session.add(cliente)
    db.session.commit()
    return cliente.id

def get_data_with_stored_procedure(param1, param2):
    """Call stored procedures using text() and named parameters."""
    result = db.session.execute(
        text("CALL procedure_name(:param1, :param2)"),
        {'param1': param1, 'param2': param2}
    ).fetchall()
    return result
```

### Error Handling

Always use try-except with rollback for database operations:

```python
from sqlalchemy.exc import SQLAlchemyError

def save_entity(data):
    try:
        entity = Entity(**data)
        db.session.add(entity)
        db.session.commit()
        return entity.id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error SQL: {e}")
        raise Exception(f"Error SQL: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        raise Exception(f"Error: {e}")
```

### API Response Pattern

```python
# Success response
return jsonify({'success': True, 'message': 'Operación exitosa', 'data': {...}})

# Error response
return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
```

### Session Variables

Common session keys used throughout the application:
- `session['user_id']` - Current user ID
- `session['id_empresa']` - Current company ID (defaults to 1)
- `session['id_sucursal']` - Current branch ID
- `session['idPuntoVenta']` - Current point of sale
- `session['tipo_iva']` - Tax type (IVA category)
- `session['owner']` - Owner name
- `session['company']` - Company name

### Environment Variables

Required environment variables (in `.env` file):
- `SQLALCHEMY_DATABASE_URI` - MySQL connection string
- `MY_SECRET_KEY` - Flask secret key
- `LOGO_PATH` - Company logo path
- `INVOICES_FOLDER` - Invoice storage path
- `COMPANY_FOLDER` - Company-specific folder
- `FLASK_ENV` - Environment (development/production)

## Important Notes

1. **Monetary values:** Always use `Decimal` type, never `float`
2. **Database commits:** Always wrap in try-except with rollback on failure
3. **Session checks:** Use `@check_session` decorator on all authenticated routes
4. **Templates:** Pass alert/message variables (`g.alertas`, `g.mensajes`, etc.)
5. **Stored procedures:** Use `text()` with named parameters for safety
6. **File uploads:** Max 16MB, allowed extensions: png, jpg, jpeg, gif, webp, svg
