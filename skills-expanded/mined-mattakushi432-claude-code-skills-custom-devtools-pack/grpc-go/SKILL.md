---
name: grpc-go
description: "When to activate: gRPC in Go, protobuf, server/client setup, interceptors, streaming, metadata, health checks"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# gRPC in Go

## Proto Definition

```proto
// api/user/v1/user.proto
syntax = "proto3";
package user.v1;
option go_package = "github.com/myorg/myapp/gen/user/v1;userv1";

service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc ListUsers(ListUsersRequest) returns (stream UserResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message GetUserRequest  { string id = 1; }
message GetUserResponse { User user = 1; }
message User {
    string id    = 1;
    string email = 2;
    string name  = 3;
}
```

```bash
# Generate Go code
protoc --go_out=gen --go_opt=paths=source_relative \
       --go-grpc_out=gen --go-grpc_opt=paths=source_relative \
       api/user/v1/user.proto
```

## Server Implementation

```go
package main

import (
    "context"
    "net"

    pb "github.com/myorg/myapp/gen/user/v1"
    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

type userServer struct {
    pb.UnimplementedUserServiceServer  // forward-compat
    repo UserRepository
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    user, err := s.repo.FindByID(ctx, req.Id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
        }
        return nil, status.Errorf(codes.Internal, "internal error: %v", err)
    }
    return &pb.GetUserResponse{User: toProto(user)}, nil
}

func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    users, err := s.repo.List(stream.Context())
    if err != nil { return status.Errorf(codes.Internal, "%v", err) }
    for _, u := range users {
        if err := stream.Send(toProto(u)); err != nil { return err }
    }
    return nil
}

func main() {
    lis, _ := net.Listen("tcp", ":50051")
    srv := grpc.NewServer(
        grpc.ChainUnaryInterceptor(loggingInterceptor, authInterceptor),
    )
    pb.RegisterUserServiceServer(srv, &userServer{repo: NewPGRepo(db)})
    srv.Serve(lis)
}
```

## Interceptors (Middleware)

```go
func loggingInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    log.Printf("method=%s duration=%s err=%v", info.FullMethod, time.Since(start), err)
    return resp, err
}

func authInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok { return nil, status.Error(codes.Unauthenticated, "missing metadata") }
    tokens := md.Get("authorization")
    if len(tokens) == 0 || !validateToken(tokens[0]) {
        return nil, status.Error(codes.Unauthenticated, "invalid token")
    }
    return handler(ctx, req)
}
```

## Client Setup

```go
func NewUserClient(addr string) (pb.UserServiceClient, error) {
    conn, err := grpc.NewClient(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),  // use TLS in prod
        grpc.WithChainUnaryInterceptor(clientAuthInterceptor),
    )
    if err != nil { return nil, err }
    return pb.NewUserServiceClient(conn), nil
}

func clientAuthInterceptor(ctx context.Context, method string, req, reply any, cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
    ctx = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+getToken())
    return invoker(ctx, method, req, reply, cc, opts...)
}
```

## gRPC Health Check

```go
import "google.golang.org/grpc/health/grpc_health_v1"
import "google.golang.org/grpc/health"

healthSrv := health.NewServer()
grpc_health_v1.RegisterHealthServer(grpcServer, healthSrv)
healthSrv.SetServingStatus("user.v1.UserService", grpc_health_v1.HealthCheckResponse_SERVING)
```

## Common Anti-Patterns

- **Not embedding `Unimplemented*Server`** — breaks when new RPCs are added to the proto
- **Returning raw Go errors** — always wrap with `status.Errorf(codes.X, ...)`
- **Blocking stream without context check** — check `stream.Context().Done()` in loops
- **Ignoring connection draining** — call `grpc.GracefulStop()` on shutdown, not `Stop()`
- **Hardcoded TLS-less credentials in prod** — use `credentials.NewTLS(tlsConfig)` in production
