---
name: refactoring-patterns
description: |
  Code refactoring techniques and patterns. Apply when improving existing code, reducing
  technical debt, extracting abstractions, or preparing code for new features.
  Covers extract-method, replace-conditional, strategy pattern, and safe refactoring steps.
---

# Refactoring Patterns

## Refactoring Process (Safe Steps)
1. **Write tests first** — cover current behavior before changing anything
2. **One change at a time** — small commits, each passing tests
3. **Rename for clarity** — rename before restructuring
4. **Extract then move** — extract to same file, then move if needed
5. **Verify** — run full test suite after every step

## Extract Method (Most common)
```python
# Before — 80 line function doing everything
def process_order(order_data: dict):
    # 20 lines: validate items
    for item in order_data['items']:
        if not Product.objects.filter(id=item['id'], is_active=True).exists():
            raise ValidationError(f"Product {item['id']} not found")
        if item['quantity'] <= 0:
            raise ValidationError("Quantity must be positive")
    
    # 20 lines: calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in order_data['items'])
    discount = calculate_discount(subtotal, order_data.get('coupon'))
    total = subtotal - discount
    
    # 40 lines: create records, send emails, notify warehouse...

# After — each concern in its own function
def process_order(order_data: dict):
    validated_items = _validate_order_items(order_data['items'])
    pricing = _calculate_order_pricing(validated_items, order_data.get('coupon'))
    order = _create_order_record(order_data, validated_items, pricing)
    _trigger_post_order_events(order)
    return order
```

## Replace Conditional with Strategy
```python
# Before — growing if/elif chain for payment providers
def process_payment(order, provider: str, data: dict):
    if provider == 'payme':
        # 30 lines of Payme logic
    elif provider == 'click':
        # 30 lines of Click logic
    elif provider == 'uzum':
        # 30 lines of Uzum logic

# After — strategy pattern (open/closed principle)
class PaymentProvider(Protocol):
    def create_payment(self, order: Order) -> str: ...
    def verify_webhook(self, data: dict) -> bool: ...

class PaymeProvider:
    def create_payment(self, order: Order) -> str: ...
    def verify_webhook(self, data: dict) -> bool: ...

class ClickProvider:
    def create_payment(self, order: Order) -> str: ...
    def verify_webhook(self, data: dict) -> bool: ...

PROVIDERS: dict[str, PaymentProvider] = {
    'payme': PaymeProvider(),
    'click': ClickProvider(),
    'uzum': UzumProvider(),
}

def process_payment(order, provider: str, data: dict):
    handler = PROVIDERS.get(provider)
    if not handler:
        raise ValueError(f"Unknown payment provider: {provider}")
    return handler.create_payment(order)
```

## Replace Nested Conditionals with Guard Clauses
```python
# Before — deep nesting
def can_place_order(user, cart):
    if user.is_active:
        if not user.is_banned:
            if cart.item_count > 0:
                if cart.total <= user.credit_limit:
                    return True
    return False

# After — guard clauses (early returns)
def can_place_order(user, cart) -> bool:
    if not user.is_active:
        return False
    if user.is_banned:
        return False
    if cart.item_count == 0:
        return False
    if cart.total > user.credit_limit:
        return False
    return True
```

## N+1 → Eager Loading (DB refactoring)
```python
# Find N+1 with django-silk or debug toolbar
# Before — N+1
orders = Order.objects.all()  # 1 query
for order in orders:
    print(order.user.name)     # N queries
    for item in order.items.all():  # N more queries
        print(item.product.name)    # N*M queries

# After — 3 queries total
orders = Order.objects.select_related('user').prefetch_related(
    Prefetch('items', queryset=OrderItem.objects.select_related('product'))
).all()
```
