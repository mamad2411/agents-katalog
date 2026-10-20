# Make me a duck

You are a junior architect and code janitor. Your goal is to create an Open API 3.0 schema to describe an API that supports the storage and retrieval of Rubber Ducks. This API should support a GET operation to get all Rubber Ducks and a POST operation to store a Rubber Duck.

The Rubber Ducks can have a name, color, and size. Size is an enum of "small", "medium", "large".

Open API Schema Rules:

- Must be formatted as yaml.
- Must include a description of the API.
- Must include appropriate tags.
- Must include http://localhost:8080 as a server.
- All operations should accept and return JSON.
- All operations should include a usage example.
- Operations should not return a parent level array. Instead, the returning array should be nested in an object.
- Each operation should have an appropriate error response using a consistent error schema.
- GET /ducks must use the operation ID `getDucks`.
- POST /ducks must use the operation ID `createDuck`.
- Name the schemas `RubberDuck`, `DuckRequest`, `DucksResponse`, and `Error`.

## Check the result

- GET `/ducks` and POST `/ducks` both exist.
- The operation IDs and schema names match the names above.
- `name`, `color`, and `size` are required.
- `size` only allows `small`, `medium`, or `large`.
- GET returns an object containing a `ducks` array, not an array by itself.
- POST returns the created duck with a `201` status.
- Errors use the same `Error` schema.
- The server URL starts with `http`, not `https`.

If yours looks different, ask AI to fix it. We'll use
[`docs/openapi.yaml`](./docs/openapi.yaml) as our checkpoint before generating Go.
