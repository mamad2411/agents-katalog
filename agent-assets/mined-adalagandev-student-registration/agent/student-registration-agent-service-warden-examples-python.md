# Service Rules — Python Examples

**Framework basis:** Python 3.11+, FastAPI 0.100+, Pydantic v2, SQLAlchemy 2.x.
The rules themselves are framework-agnostic — these examples only show one
concrete stack.
**Translation hints:** Django → view = boundary, service module = logic,
`transaction.atomic()` = unit of work; Flask → blueprint = boundary;
plain scripts → argparse layer = boundary.
**Version-sensitive:** Pydantic v2 shown (`model_validate`, `ConfigDict`) —
v1 uses `parse_obj`/`Config`. SQLAlchemy 2.x `Session.begin()` shown — 1.x
autocommit patterns differ.

## Rule 1 — One capability per service
Violation:
```python
class OrderService:
    def place_order(...): ...
    def send_order_email(...): ...      # notification capability
    def render_invoice_pdf(...): ...    # document capability
```
Correct:
```python
class OrderService:                     # orders only
    def place_order(...): ...
class NotificationService: ...
class InvoiceService: ...
```

## Rule 2 — Inject dependencies
Violation:
```python
class OrderService:
    def __init__(self):
        self.repo = OrderRepository(engine)   # self-instantiated, concrete
```
Correct:
```python
class OrderService:
    def __init__(self, repo: OrderRepositoryPort, clock: Clock):
        self._repo, self._clock = repo, clock
# FastAPI wiring: Depends(get_order_service) at the router, never inside
```

## Rule 3 — No transport/persistence in logic
Violation:
```python
def place_order(self, request: Request):          # HTTP in the service
    data = await request.json()
    self.session.execute(text("INSERT ..."))      # raw SQL in the service
```
Correct:
```python
def place_order(self, cmd: PlaceOrder) -> Order:  # domain in, domain out
    ...
    self._repo.add(order)                          # port hides persistence
```

## Rule 4 — DTOs at the boundary
Violation:
```python
def place_order(self, body: OrderRequest):   # Pydantic request model
    self._repo.add(body)                     # flows straight to storage
```
Correct:
```python
# router:
cmd = PlaceOrder(customer_id=body.customer_id, lines=body.to_lines())
order = service.place_order(cmd)             # domain dataclass inside
return OrderResponse.model_validate(order)   # mapped back at the edge
```

## Rule 5 — Service method = transaction boundary
Violation:
```python
def place_order(self, cmd):
    self._repo.add(order); self._session.commit()       # commit #1
    self._stock.reserve(order); self._session.commit()  # half-committed risk
```
Correct:
```python
def place_order(self, cmd):
    with self._uow.begin():          # one unit of work
        self._repo.add(order)
        self._stock.reserve(order)   # both or neither
```

## Rule 6 — Domain exceptions only
Violation:
```python
raise HTTPException(status_code=409, detail="no stock")  # HTTP in service
```
Correct:
```python
raise InsufficientStockError(sku, requested, available)
# boundary handler maps it to 409 (exception-warden's territory)
```

## Rule 7 — Invariants in service, syntax at edge
Violation:
```python
def place_order(self, cmd):
    if not re.match(EMAIL_RE, cmd.email): ...   # format check re-done here
    # ...but nobody checks the customer exists
```
Correct:
```python
def place_order(self, cmd):                     # Pydantic validated shape
    customer = self._customers.get(cmd.customer_id)
    if customer is None:
        raise CustomerNotFoundError(cmd.customer_id)
    if not customer.may_order():
        raise CustomerSuspendedError(customer.id)
```

## Rule 8 — Stateless services
Violation:
```python
class CartService:
    def load(self, user_id): self.cart = ...   # shared across requests
    def checkout(self): use(self.cart)         # race in ASGI concurrency
```
Correct:
```python
class CartService:
    def checkout(self, user_id: UserId) -> Receipt:
        cart = self._repo.for_user(user_id)    # state via params/storage
```

## Rule 9 — Isolate side effects and time
Violation:
```python
if order.created_at < datetime.now() - TTL:    # needs freezegun to test
```
Correct:
```python
def __init__(self, ..., now: Callable[[], datetime]): ...
if order.created_at < self._now() - TTL:       # test passes a fake now
```

## Rule 10 — CQS; orchestrate, don't accumulate
Violation:
```python
def get_order(self, oid):
    order = self._repo.get(oid)
    order.last_viewed = self._now()            # query mutates state
    self._repo.save(order)
    return order
```
Correct:
```python
def get_order(self, oid) -> Order: return self._repo.get(oid)   # query
def record_view(self, oid) -> None: ...                          # command
```
