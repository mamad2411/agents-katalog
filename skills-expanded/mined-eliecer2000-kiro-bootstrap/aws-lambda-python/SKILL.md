---
name: aws-lambda-python
description: AWS Lambda development with Python. Use when writing Lambda handlers, packaging with layers, using boto3/Powertools, structured logging or optimizing Python Lambda performance.
---

# AWS Lambda Python

Skill para desarrollo de funciones Lambda en Python: handlers, empaquetado, layers, AWS SDK (boto3), Powertools, logging estructurado, manejo de errores, testing y mejores prácticas de rendimiento.

## Principios fundamentales

- Un handler, una responsabilidad. Evitar Lambdas monolíticos.
- Separar lógica de negocio del handler. El handler solo parsea el evento, invoca la lógica y formatea la respuesta.
- Usar AWS Lambda Powertools para Python en todo proyecto: logging, tracing, metrics, validation, idempotency.
- Tipado estricto con type hints y validación con Pydantic o Powertools Parser.
- Inicializar clientes AWS fuera del handler (reutilización en warm starts).

## Estructura de proyecto recomendada

```
functions/
├── mi_funcion/
│   ├── __init__.py
│   ├── handler.py          # Entry point del Lambda
│   ├── service.py          # Lógica de negocio
│   ├── repository.py       # Acceso a datos (DynamoDB, S3, etc.)
│   ├── models.py           # Pydantic models / dataclasses
│   └── exceptions.py       # Excepciones custom
├── shared/
│   ├── __init__.py
│   ├── middleware.py        # Middleware compartido
│   └── constants.py
├── tests/
│   ├── unit/
│   │   ├── test_service.py
│   │   └── test_handler.py
│   └── integration/
│       └── test_api.py
├── requirements.txt
└── pyproject.toml
```

## Handler con Powertools (patrón recomendado)

```python
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.validation import validate

logger = Logger()
tracer = Tracer()
metrics = Metrics()
app = APIGatewayHttpResolver()

# Clientes AWS inicializados fuera del handler (warm start reuse)
import boto3
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

@app.get("/items")
@tracer.capture_method
def list_items():
    items = table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={":pk": "ITEMS"},
    )
    return {"items": items.get("Items", [])}

@app.post("/items")
@tracer.capture_method
def create_item():
    body = app.current_event.json_body
    # Validar con Pydantic
    item = ItemCreate(**body)
    table.put_item(Item=item.to_dynamo())
    metrics.add_metric(name="ItemCreated", unit=MetricUnit.Count, value=1)
    return {"id": item.id}, 201

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
```

## Validación con Pydantic

```python
from pydantic import BaseModel, Field, validator
from uuid import uuid4
from datetime import datetime

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(..., pattern=r"^[a-z-]+$")

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()

    def to_dynamo(self) -> dict:
        return {
            "PK": "ITEMS",
            "SK": f"ITEM#{uuid4()}",
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "category": self.category,
            "createdAt": datetime.utcnow().isoformat(),
        }
```

## Manejo de errores

```python
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    NotFoundError,
    InternalServerError,
)

class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code

@app.exception_handler(AppError)
def handle_app_error(ex: AppError):
    logger.warning(f"App error: {ex.code} - {ex.message}")
    return (
        {"error": {"code": ex.code, "message": ex.message}},
        ex.status_code,
    )

@app.exception_handler(Exception)
def handle_unexpected_error(ex: Exception):
    logger.exception("Unexpected error")
    return (
        {"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}},
        500,
    )
```

## Idempotencia con Powertools

```python
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer,
    idempotent_function,
    IdempotencyConfig,
)

persistence = DynamoDBPersistenceLayer(table_name=os.environ["IDEMPOTENCY_TABLE"])
config = IdempotencyConfig(expires_after_seconds=3600)

@idempotent_function(
    data_keyword_argument="order",
    persistence_store=persistence,
    config=config,
)
def process_order(order: dict) -> dict:
    # Esta función solo se ejecuta una vez por order_id
    result = payment_service.charge(order)
    return {"status": "processed", "transaction_id": result.id}
```

## Empaquetado y layers

### requirements.txt
```
aws-lambda-powertools[all]>=2.0.0
pydantic>=2.0.0
boto3-stubs[dynamodb]
```

### Layer compartido (con CDK)
```python
# En CDK stack
powertools_layer = lambda_.LayerVersion.from_layer_version_arn(
    self, "PowertoolsLayer",
    f"arn:aws:lambda:{region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:51"
)
```

### Docker para dependencias nativas
```dockerfile
FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY functions/ ${LAMBDA_TASK_ROOT}/
CMD ["handler.handler"]
```

## Testing

### Unit test con pytest
```python
import pytest
from unittest.mock import patch, MagicMock
from functions.mi_funcion.service import ItemService

@pytest.fixture
def mock_table():
    with patch("functions.mi_funcion.repository.table") as mock:
        yield mock

def test_create_item_success(mock_table):
    mock_table.put_item.return_value = {}
    service = ItemService(mock_table)
    result = service.create({"name": "Test", "price": 9.99, "category": "test"})
    assert result["name"] == "Test"
    mock_table.put_item.assert_called_once()

def test_create_item_invalid_price(mock_table):
    service = ItemService(mock_table)
    with pytest.raises(ValueError, match="price must be positive"):
        service.create({"name": "Test", "price": -1, "category": "test"})
```

### Test de handler con evento API Gateway
```python
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2

def test_handler_list_items(mock_table):
    mock_table.query.return_value = {"Items": [{"name": "Item1"}]}
    event = APIGatewayProxyEventV2({
        "requestContext": {"http": {"method": "GET", "path": "/items"}},
        "rawPath": "/items",
    })
    response = handler(event._data, MagicMock())
    assert response["statusCode"] == 200
```

## Rendimiento

- Inicializar clientes boto3 fuera del handler (global scope).
- Usar `boto3.resource` para operaciones de alto nivel, `boto3.client` para bajo nivel.
- Memory: empezar con 256MB, medir con Powertools Tracer y ajustar.
- Timeout: 2x el p99 observado, mínimo 10s para APIs, hasta 900s para procesamiento batch.
- Evitar imports innecesarios en el handler (cada import añade cold start).
- Usar Provisioned Concurrency solo si p99 cold start es inaceptable.

## Variables de entorno recomendadas

```
POWERTOOLS_SERVICE_NAME=mi-servicio
POWERTOOLS_LOG_LEVEL=INFO
POWERTOOLS_METRICS_NAMESPACE=MiApp
TABLE_NAME=mi-tabla
STAGE=dev
```

## Anti-patrones a evitar

- ❌ Lógica de negocio directamente en el handler.
- ❌ `import boto3` dentro del handler (re-crea cliente en cada invocación).
- ❌ `print()` en lugar de logger estructurado.
- ❌ Capturar `Exception` sin re-raise o logging.
- ❌ No usar type hints.
- ❌ requirements.txt sin versiones pinneadas.
- ❌ Hardcodear nombres de tablas, buckets o ARNs.
- ❌ No tener tests unitarios para la lógica de negocio.
- ❌ Lambda con más de 512MB sin justificación medida.
- ❌ Timeout de 15 minutos "por si acaso".

## Checklist de revisión Lambda Python

- [ ] Handler delgado, lógica en service/repository.
- [ ] Powertools configurado (Logger, Tracer, Metrics).
- [ ] Validación de input con Pydantic o Powertools Parser.
- [ ] Manejo de errores con respuestas consistentes.
- [ ] Clientes AWS inicializados fuera del handler.
- [ ] Variables de entorno para configuración (no hardcoded).
- [ ] Tests unitarios con pytest y mocks.
- [ ] requirements.txt con versiones pinneadas.
- [ ] Memory y timeout configurados según mediciones.
- [ ] Idempotencia implementada donde aplica.
