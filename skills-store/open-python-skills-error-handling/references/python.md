# Python Error Handling

Core Python error handling patterns following the **Let it crash** philosophy.

## Design Philosophy

### Raise Low, Catch High

Exceptions should be raised where errors occur and caught at application boundaries:

```python
# In service layer - just raise
async def get_user(user_id: int) -> User:
    user = await db.users.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user

# In route layer - let it propagate (no try/except needed)
@app.get("/users/{user_id}")
async def get_user_endpoint(user_id: int):
    return await user_service.get_user(user_id)

# At boundary - global handler catches and formats
@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(request, exc):
    return JSONResponse(status_code=404, content={"error": exc.message})
```

### When to Catch Exceptions

Only catch in these specific situations:

| Situation | Reason | Example |
|-----------|--------|---------|
| **Retry** | Transient failures need retry logic | Network timeouts, rate limits |
| **Transform** | Convert to domain exception | Wrap third-party SDK errors |
| **Clean up** | Release resources | File handles, connections |
| **Add context** | Enrich error information | Add request_id, user context |

```python
# GOOD - Catching to transform
try:
    response = await client.get(url)
except httpx.TimeoutException as e:
    raise ExternalServiceError("API timeout") from e

# GOOD - Catching to retry
@retry(stop=stop_after_attempt(3))
async def fetch_data():
    return await unreliable_api.get()

# GOOD - Catching to clean up (prefer context managers)
async with aiofiles.open("data.txt") as f:
    return await f.read()

# BAD - Catching just to log and re-raise
try:
    result = do_something()
except Exception as e:
    logger.error(f"Error: {e}")  # Redundant - global handler logs
    raise
```

## Custom Exception Design

### Exception Hierarchy

Create a hierarchy based on how callers will handle errors:

```python
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(AppError):
    """Input validation failed."""
    pass

class NotFoundError(AppError):
    """Resource not found."""
    pass

class ExternalServiceError(AppError):
    """Third-party service failed."""
    def __init__(self, service: str, original: Exception | None = None):
        self.service = service
        super().__init__(f"{service} unavailable")
        if original:
            self.__cause__ = original
```

### Storing Meaningful Attributes

Store data as attributes, not just strings:

```python
# BAD - Only string message
class UserError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

raise UserError("User 123 not found")  # Can't programmatically get user_id

# GOOD - Meaningful attributes
class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

error = UserNotFoundError(123)
print(error.user_id)  # 123 - can use programmatically
```

### Preserving Original Traceback

Always use `from` when re-raising:

```python
# BAD - Loses original traceback
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    raise ValidationError("Invalid JSON")

# GOOD - Preserves original traceback
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise ValidationError("Invalid JSON") from e
```

## Third-Party SDK Wrapping

### Wrap at Integration Boundary

```python
import stripe
from tenacity import retry, stop_after_attempt, wait_exponential

class PaymentError(AppError):
    """Payment processing failed."""
    pass

class PaymentDeclinedError(PaymentError):
    """Payment was declined."""
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Payment declined: {reason}")

class PaymentServiceError(PaymentError):
    """Payment service unavailable."""
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(PaymentServiceError)
)
async def charge_card(amount: int, card_token: str) -> str:
    try:
        charge = stripe.Charge.create(amount=amount, source=card_token)
        return charge.id
    except stripe.error.CardError as e:
        raise PaymentDeclinedError(e.user_message) from e
    except stripe.error.RateLimitError as e:
        raise PaymentServiceError("Rate limited") from e
    except stripe.error.APIConnectionError as e:
        raise PaymentServiceError("Connection failed") from e
    except stripe.error.StripeError as e:
        raise PaymentError(f"Stripe error: {e}") from e
```

### Timeout Handling

```python
import asyncio
import httpx

async def fetch_with_timeout(url: str, timeout: float = 10.0) -> dict:
    """Fetch URL with explicit timeout."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException as e:
        raise ExternalServiceError("Request timeout") from e
    except httpx.HTTPStatusError as e:
        raise ExternalServiceError(f"HTTP {e.response.status_code}") from e

# Or use asyncio.timeout (Python 3.11+)
async def fetch_with_asyncio_timeout(url: str) -> dict:
    try:
        async with asyncio.timeout(10.0):
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
    except TimeoutError:
        raise ExternalServiceError("Request timeout")
```

## Anti-Patterns

### Bare Except

```python
# BAD - Catches everything including KeyboardInterrupt, SystemExit
try:
    do_something()
except:
    pass

# GOOD - Catch specific exceptions
try:
    do_something()
except ValueError as e:
    handle_value_error(e)
```

### Catching Exception to Log and Re-raise

```python
# BAD - Redundant, global handler should log
try:
    result = service.process()
except Exception as e:
    logger.exception("Error processing")
    raise

# GOOD - Just let it propagate
result = service.process()  # Global handler logs unhandled errors
```

### Exception for Control Flow

```python
# BAD - Using exception for normal flow
def find_user(user_id: int) -> User | None:
    try:
        return users[user_id]
    except KeyError:
        return None

# GOOD - Use .get() for expected missing keys
def find_user(user_id: int) -> User | None:
    return users.get(user_id)
```

### Catching Too Broadly

```python
# BAD - Catches unrelated errors (typos, logic bugs)
try:
    user = get_user(user_id)
    process_user(user)
except Exception:
    return None  # Hides bugs!

# GOOD - Catch only expected exceptions
try:
    user = get_user(user_id)
except UserNotFoundError:
    return None
process_user(user)  # Other errors propagate
```
