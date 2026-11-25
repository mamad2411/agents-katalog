---
name: python-grpc
description: "When to activate: gRPC, protobuf, grpcio, async gRPC, streaming, service definitions, interceptors"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python gRPC Patterns

## Project Structure
```
proto/
  └── user/
      └── v1/
          └── user.proto
src/
  └── generated/
      └── user/
          └── v1/
              ├── user_pb2.py
              └── user_pb2_grpc.py
  └── services/
      └── user_service.py
```

## Proto Definition
```protobuf
syntax = "proto3";
package user.v1;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User);
  rpc CreateUser(CreateUserRequest) returns (User);
}

message User {
  int64 id = 1;
  string email = 2;
  string name = 3;
  google.protobuf.Timestamp created_at = 4;
}

message GetUserRequest { int64 id = 1; }
message ListUsersRequest { int32 page_size = 1; string page_token = 2; }
message CreateUserRequest { string email = 1; string name = 2; }
```

## Async Service Implementation
```python
import grpc
from grpc import aio
from generated.user.v1 import user_pb2, user_pb2_grpc

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo
    
    async def GetUser(self, request: user_pb2.GetUserRequest, context: aio.ServicerContext) -> user_pb2.User:
        user = await self._repo.get_by_id(request.id)
        if user is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"User {request.id} not found")
        return user_pb2.User(id=user.id, email=user.email, name=user.name)
    
    async def ListUsers(self, request: user_pb2.ListUsersRequest, context: aio.ServicerContext):
        async for user in self._repo.stream_all(page_size=request.page_size):
            yield user_pb2.User(id=user.id, email=user.email, name=user.name)

async def serve() -> None:
    server = aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(user_repo), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
```

## Interceptors
```python
class LoggingInterceptor(aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        start = time.monotonic()
        method = handler_call_details.method
        try:
            result = await continuation(handler_call_details)
            logger.info("gRPC %s OK %.3fs", method, time.monotonic() - start)
            return result
        except Exception as e:
            logger.error("gRPC %s FAILED %.3fs: %s", method, time.monotonic() - start, e)
            raise
```

## Code Generation
```bash
python -m grpc_tools.protoc \
    -I proto \
    --python_out=src/generated \
    --grpc_python_out=src/generated \
    --pyi_out=src/generated \
    proto/user/v1/user.proto
```
