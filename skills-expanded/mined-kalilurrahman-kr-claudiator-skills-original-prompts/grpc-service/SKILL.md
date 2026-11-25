---
name: grpc-service
description: Design and implement gRPC services with Protocol Buffer schemas, streaming patterns, error handling, and client generation. Outputs .proto files, server implementation, client code, and load balancing configuration.
argument-hint: [service name, operations, streaming requirements, language]
allowed-tools: Read, Write, Bash
---

# gRPC Service Design

Design production-ready gRPC services with strongly-typed contracts, efficient binary serialization, and support for all four communication patterns: unary, server-streaming, client-streaming, and bidirectional streaming.

## Process

1. **Define the service contract** in `.proto` first — this is your source of truth.
2. **Choose streaming pattern** per RPC: unary, server-stream, client-stream, or bidi.
3. **Design message types** — prefer flat structures, avoid deep nesting.
4. **Plan error codes** — use gRPC status codes + rich error details.
5. **Add metadata** — request IDs, auth tokens, tracing in headers.
6. **Generate stubs** — server and client from `.proto` using protoc.
7. **Implement interceptors** — auth, logging, tracing, retry as middleware.
8. **Configure load balancing** — client-side or proxy-based.
9. **Write integration tests** with real proto types.

## Output Format

### Proto Definition

```protobuf
// order_service.proto
syntax = "proto3";

package orders.v1;

option go_package = "github.com/example/api/orders/v1;ordersv1";
option java_package = "com.example.orders.v1";

import "google/protobuf/timestamp.proto";
import "google/rpc/status.proto";

// ── Messages ──────────────────────────────────────────────

message Order {
  string order_id = 1;
  string user_id = 2;
  repeated OrderItem items = 3;
  OrderStatus status = 4;
  Money total = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
}

message OrderItem {
  string product_id = 1;
  string product_name = 2;
  int32 quantity = 3;
  Money unit_price = 4;
}

message Money {
  string currency_code = 1;  // ISO 4217: "USD", "EUR"
  int64 units = 2;            // Whole units
  int32 nanos = 3;            // Fractional nanos (0-999,999,999)
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;  // Always define 0 as unspecified
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}

// ── Requests / Responses ──────────────────────────────────

message CreateOrderRequest {
  string user_id = 1;
  repeated OrderItem items = 2;
  string idempotency_key = 3;  // Client-generated UUID for dedup
}

message CreateOrderResponse {
  Order order = 1;
}

message GetOrderRequest {
  string order_id = 1;
}

message GetOrderResponse {
  Order order = 1;
}

message ListOrdersRequest {
  string user_id = 1;
  int32 page_size = 2;           // Default 20, max 100
  string page_token = 3;         // Cursor-based pagination
  OrderStatus status_filter = 4; // Optional filter
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;   // Empty if no more pages
  int32 total_count = 3;
}

// Server-streaming: real-time order status updates
message WatchOrderRequest {
  string order_id = 1;
}

// Bidi streaming: bulk order processing
message ProcessOrderRequest {
  oneof payload {
    CreateOrderRequest create = 1;
    string cancel_order_id = 2;
  }
}

message ProcessOrderResponse {
  string idempotency_key = 1;
  oneof result {
    Order order = 2;
    google.rpc.Status error = 3;
  }
}

// ── Service ───────────────────────────────────────────────

service OrderService {
  // Unary: standard request/response
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  
  // Server-streaming: push updates to client
  rpc WatchOrder(WatchOrderRequest) returns (stream Order);
  
  // Bidi-streaming: high-throughput bulk processing
  rpc ProcessOrders(stream ProcessOrderRequest) returns (stream ProcessOrderResponse);
}
```

### Server Implementation (Python)

```python
# server.py
import grpc
import asyncio
import logging
from concurrent import futures
from typing import AsyncIterator

import orders_pb2
import orders_pb2_grpc
from grpc import ServicerContext
from grpc_status import rpc_status
from google.rpc import status_pb2, code_pb2

logger = logging.getLogger(__name__)

class OrderServicer(orders_pb2_grpc.OrderServiceServicer):
    
    def __init__(self, db, event_bus):
        self.db = db
        self.event_bus = event_bus
    
    # ── Unary ──────────────────────────────────────────────
    
    async def CreateOrder(
        self,
        request: orders_pb2.CreateOrderRequest,
        context: ServicerContext
    ) -> orders_pb2.CreateOrderResponse:
        # Extract metadata
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get("x-request-id", "unknown")
        user_id = metadata.get("x-user-id")
        
        if not user_id:
            await context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                "Missing x-user-id header"
            )
        
        # Validate
        if not request.items:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Order must contain at least one item"
            )
        
        # Idempotency check
        if request.idempotency_key:
            existing = await self.db.get_order_by_idempotency_key(
                request.idempotency_key
            )
            if existing:
                return orders_pb2.CreateOrderResponse(
                    order=self._to_proto(existing)
                )
        
        try:
            order = await self.db.create_order(
                user_id=request.user_id,
                items=request.items,
                idempotency_key=request.idempotency_key
            )
            await self.event_bus.publish("order.created", order)
            return orders_pb2.CreateOrderResponse(order=self._to_proto(order))
        
        except ValueError as e:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except Exception as e:
            logger.error(f"CreateOrder failed: {e}", extra={"request_id": request_id})
            await context.abort(grpc.StatusCode.INTERNAL, "Internal error")
    
    # ── Server Streaming ───────────────────────────────────
    
    async def WatchOrder(
        self,
        request: orders_pb2.WatchOrderRequest,
        context: ServicerContext
    ) -> AsyncIterator[orders_pb2.Order]:
        order_id = request.order_id
        
        # Send current state immediately
        order = await self.db.get_order(order_id)
        if not order:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"Order {order_id} not found")
            return
        
        yield self._to_proto(order)
        
        # Stream updates via event subscription
        async with self.event_bus.subscribe(f"order.{order_id}.*") as subscription:
            async for event in subscription:
                if context.cancelled():
                    break
                    
                updated_order = await self.db.get_order(order_id)
                if updated_order:
                    yield self._to_proto(updated_order)
                
                # Stop streaming once terminal state reached
                if updated_order.status in (
                    orders_pb2.ORDER_STATUS_DELIVERED,
                    orders_pb2.ORDER_STATUS_CANCELLED
                ):
                    break
    
    # ── Bidi Streaming ─────────────────────────────────────
    
    async def ProcessOrders(
        self,
        request_iterator: AsyncIterator[orders_pb2.ProcessOrderRequest],
        context: ServicerContext
    ) -> AsyncIterator[orders_pb2.ProcessOrderResponse]:
        async for request in request_iterator:
            try:
                if request.HasField("create"):
                    order = await self.db.create_order(
                        user_id=request.create.user_id,
                        items=request.create.items
                    )
                    yield orders_pb2.ProcessOrderResponse(
                        idempotency_key=request.create.idempotency_key,
                        order=self._to_proto(order)
                    )
                elif request.cancel_order_id:
                    await self.db.cancel_order(request.cancel_order_id)
                    yield orders_pb2.ProcessOrderResponse(
                        idempotency_key=request.cancel_order_id,
                        order=orders_pb2.Order(
                            order_id=request.cancel_order_id,
                            status=orders_pb2.ORDER_STATUS_CANCELLED
                        )
                    )
            except Exception as e:
                rich_status = status_pb2.Status(
                    code=code_pb2.INTERNAL,
                    message=str(e)
                )
                yield orders_pb2.ProcessOrderResponse(
                    idempotency_key="",
                    error=rich_status
                )
    
    def _to_proto(self, order) -> orders_pb2.Order:
        return orders_pb2.Order(
            order_id=str(order.id),
            user_id=str(order.user_id),
            status=orders_pb2.OrderStatus.Value(f"ORDER_STATUS_{order.status.upper()}"),
            items=[
                orders_pb2.OrderItem(
                    product_id=str(item.product_id),
                    product_name=item.product_name,
                    quantity=item.quantity,
                )
                for item in order.items
            ]
        )


# ── Interceptors ───────────────────────────────────────────

class LoggingInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        metadata = dict(handler_call_details.invocation_metadata)
        request_id = metadata.get("x-request-id", "unknown")
        
        start = asyncio.get_event_loop().time()
        try:
            response = await continuation(handler_call_details)
            elapsed = asyncio.get_event_loop().time() - start
            logger.info(f"gRPC {method} OK {elapsed*1000:.1f}ms", 
                       extra={"request_id": request_id})
            return response
        except grpc.RpcError as e:
            elapsed = asyncio.get_event_loop().time() - start
            logger.error(f"gRPC {method} {e.code()} {elapsed*1000:.1f}ms",
                        extra={"request_id": request_id})
            raise


class AuthInterceptor(grpc.aio.ServerInterceptor):
    PUBLIC_METHODS = {"/orders.v1.OrderService/GetOrder"}
    
    async def intercept_service(self, continuation, handler_call_details):
        if handler_call_details.method in self.PUBLIC_METHODS:
            return await continuation(handler_call_details)
        
        metadata = dict(handler_call_details.invocation_metadata)
        token = metadata.get("authorization", "").removeprefix("Bearer ")
        
        if not token:
            raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, "Missing token")
        
        try:
            payload = verify_jwt(token)
            # Attach user info to context for servicer
            handler_call_details.invocation_metadata.append(
                ("x-user-id", payload["sub"])
            )
        except Exception:
            raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        return await continuation(handler_call_details)


# ── Server Setup ───────────────────────────────────────────

async def serve():
    server = grpc.aio.server(
        interceptors=[AuthInterceptor(), LoggingInterceptor()],
        options=[
            ("grpc.max_receive_message_length", 16 * 1024 * 1024),  # 16MB
            ("grpc.max_send_message_length", 16 * 1024 * 1024),
            ("grpc.keepalive_time_ms", 30000),
            ("grpc.keepalive_timeout_ms", 5000),
            ("grpc.keepalive_permit_without_calls", True),
        ]
    )
    
    orders_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderServicer(db=get_db(), event_bus=get_event_bus()),
        server
    )
    
    # Enable reflection for debugging tools (grpcurl, BloomRPC)
    from grpc_reflection.v1alpha import reflection
    SERVICE_NAMES = (
        orders_pb2.DESCRIPTOR.services_by_name["OrderService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    await server.start()
    logger.info(f"gRPC server listening on {listen_addr}")
    
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
```

### Client Implementation

```python
# client.py
import grpc
import asyncio
from contextlib import asynccontextmanager
import uuid

import orders_pb2
import orders_pb2_grpc

class OrderServiceClient:
    def __init__(self, address: str, timeout: float = 5.0):
        self.address = address
        self.timeout = timeout
        self._channel = None
        self._stub = None
    
    async def __aenter__(self):
        self._channel = grpc.aio.insecure_channel(
            self.address,
            options=[
                ("grpc.lb_policy_name", "round_robin"),
                ("grpc.keepalive_time_ms", 30000),
            ]
        )
        self._stub = orders_pb2_grpc.OrderServiceStub(self._channel)
        return self
    
    async def __aexit__(self, *args):
        await self._channel.close()
    
    def _metadata(self, token: str) -> list[tuple]:
        return [
            ("authorization", f"Bearer {token}"),
            ("x-request-id", str(uuid.uuid4())),
        ]
    
    async def create_order(self, user_id: str, items: list, token: str) -> orders_pb2.Order:
        request = orders_pb2.CreateOrderRequest(
            user_id=user_id,
            items=[orders_pb2.OrderItem(**item) for item in items],
            idempotency_key=str(uuid.uuid4())
        )
        
        try:
            response = await self._stub.CreateOrder(
                request,
                metadata=self._metadata(token),
                timeout=self.timeout
            )
            return response.order
        
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise OrderAlreadyExistsError(e.details())
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise ValidationError(e.details())
            elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                raise TimeoutError(f"CreateOrder timed out after {self.timeout}s")
            else:
                raise ServiceError(f"gRPC error {e.code()}: {e.details()}")
    
    async def watch_order(self, order_id: str, token: str):
        """Stream order status updates until terminal state."""
        request = orders_pb2.WatchOrderRequest(order_id=order_id)
        
        async for order in self._stub.WatchOrder(
            request,
            metadata=self._metadata(token),
            timeout=300  # 5 minute max watch
        ):
            yield order
            if order.status in (
                orders_pb2.ORDER_STATUS_DELIVERED,
                orders_pb2.ORDER_STATUS_CANCELLED
            ):
                break


# Usage
async def main():
    async with OrderServiceClient("localhost:50051") as client:
        # Unary call
        order = await client.create_order(
            user_id="user-123",
            items=[{"product_id": "prod-1", "quantity": 2}],
            token="eyJ..."
        )
        print(f"Created order: {order.order_id}")
        
        # Server streaming
        async for update in client.watch_order(order.order_id, token="eyJ..."):
            print(f"Order status: {orders_pb2.OrderStatus.Name(update.status)}")
```

### Health Check

```protobuf
// health.proto (standard gRPC health check protocol)
syntax = "proto3";
package grpc.health.v1;

message HealthCheckRequest {
  string service = 1;
}
message HealthCheckResponse {
  enum ServingStatus {
    UNKNOWN = 0;
    SERVING = 1;
    NOT_SERVING = 2;
    SERVICE_UNKNOWN = 3;
  }
  ServingStatus status = 1;
}
service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
  rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);
}
```

```python
# Health servicer
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

health_servicer = health.HealthServicer()
health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

# Mark service as healthy/unhealthy dynamically
health_servicer.set("orders.v1.OrderService", health_pb2.HealthCheckResponse.SERVING)
```

## Testing

```python
import pytest
import grpc
from grpc.experimental import aio

@pytest.fixture
async def grpc_channel():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        yield channel

@pytest.mark.asyncio
async def test_create_order(grpc_channel):
    stub = orders_pb2_grpc.OrderServiceStub(grpc_channel)
    
    response = await stub.CreateOrder(
        orders_pb2.CreateOrderRequest(
            user_id="user-1",
            items=[orders_pb2.OrderItem(product_id="prod-1", quantity=1)],
            idempotency_key="key-123"
        ),
        metadata=[("authorization", "Bearer test-token")]
    )
    
    assert response.order.order_id != ""
    assert response.order.status == orders_pb2.ORDER_STATUS_PENDING

@pytest.mark.asyncio
async def test_create_order_unauthenticated(grpc_channel):
    stub = orders_pb2_grpc.OrderServiceStub(grpc_channel)
    
    with pytest.raises(grpc.RpcError) as exc_info:
        await stub.CreateOrder(
            orders_pb2.CreateOrderRequest(user_id="user-1"),
            # No auth metadata
        )
    
    assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
```

## Rules

- **Proto-first design** — `.proto` is the contract; implementation follows.
- **Always define field 0 as `_UNSPECIFIED`** in enums — proto3 default is 0.
- **Never reuse field numbers** — removing fields, mark them `reserved`.
- **Use `google.protobuf.Timestamp`** for times, never string timestamps.
- **Idempotency keys on mutations** — clients can safely retry on network failure.
- **Deadline propagation** — always accept and forward deadlines, never set `timeout=None`.
- **Rich error details** — use `google.rpc.Status` for structured errors, not just text.
- **Enable reflection** in non-production for tooling (grpcurl, BloomRPC).
- **Keepalive pings** — required for long-lived connections through load balancers.
- **Separate read and write services** — easier to scale and secure independently.
