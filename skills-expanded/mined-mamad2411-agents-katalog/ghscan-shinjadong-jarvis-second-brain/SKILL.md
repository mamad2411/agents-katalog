# E-commerce Patterns Skill

## Overview
이커머스 일반 패턴 및 베스트 프랙티스

## Common Entities

### Product
```python
@dataclass
class Product:
    id: str
    name: str
    price: int
    stock: int
    status: Literal["active", "inactive", "soldout"]
```

### Order
```python
@dataclass
class Order:
    id: str
    items: List[OrderItem]
    total: int
    status: OrderStatus
    created_at: datetime
```

### OrderItem
```python
@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: int
```

## State Machines

### Order Status
```
PENDING → PAID → PREPARING → SHIPPED → DELIVERED
    ↓        ↓         ↓
  CANCELLED  REFUND_REQUESTED → REFUNDED
```

### Payment Status
```
READY → PROCESSING → COMPLETED → SETTLED
                 ↓
              FAILED
```

## API Patterns

### Pagination
```python
def get_orders(page: int = 1, size: int = 20):
    offset = (page - 1) * size
    return {
        "items": orders[offset:offset+size],
        "total": len(orders),
        "page": page,
        "size": size
    }
```

### Error Response
```json
{
  "error": {
    "code": "INVALID_ORDER_STATUS",
    "message": "Cannot ship cancelled order",
    "details": {"orderId": "12345", "currentStatus": "CANCELLED"}
  }
}
```

## Best Practices

### Inventory Management
- 주문 시 재고 차감 (pessimistic lock)
- 결제 실패 시 재고 복구
- 실시간 재고 동기화

### Price Handling
- 금액은 정수(원)로 저장
- 할인/세금 계산 시 반올림 규칙 명시
- 가격 변경 이력 보관
