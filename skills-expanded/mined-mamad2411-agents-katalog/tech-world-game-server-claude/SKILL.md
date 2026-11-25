# CLAUDE.md - tech_world_game_server

## Project Overview

Dart WebSocket server for Tech World multiplayer game. Manages player connections and broadcasts messages.

## Build & Run

```bash
dart pub get
dart run bin/server.dart  # runs on port 443 with SSL
dart test
```

## Key Files

- `bin/server.dart`: Entry point, creates shelf server with SSL on port 443
- `lib/client_connections_service.dart`: Core logic - manages connections, handles all message types
- `lib/locator.dart`: Service locator for dependency injection

## Message Types Handled

All message types from `tech_world_networking_types`:
- `arrival`: Player joins, server stores connection and broadcasts updated player list
- `departure`: Player leaves, server removes connection and broadcasts
- `other_users`: Request to broadcast current player list
- `player_path`: Movement data, relayed to all other connected clients

## Architecture Notes

### ClientConnectionsService
- Maintains `presenceMap`: `Map<WebSocketChannel, NetworkUser>`
- `defaultMessageHandler`: Attached to each WebSocket, routes messages by `type` field
- `_broadcastOtherUsers()`: Sends each client a list of OTHER players (excludes self)
- `_broadcastPlayerPath()`: Relays path to all clients except sender

### Server Configuration
- Binds to `0.0.0.0` for Cloud Run compatibility
- Requires SSL certs at `/app/cert.pem` and `/app/key.pem`
- Port 443 for WSS

## Deployment

Push tagged commit triggers GitHub Actions:
```bash
git tag v1.0.0 && git push --tags
```

Deploys to GCP Compute Engine VM via Docker.

## Testing

- Tests in `test/tech_world_game_server_test.dart`
- Can inject custom message handler via `ClientConnectionsService` constructor
