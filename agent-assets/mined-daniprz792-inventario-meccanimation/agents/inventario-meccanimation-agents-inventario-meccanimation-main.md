# AGENTS.md

## Project overview
This repository is a small Java 17 Maven application for an inventory system. It uses Javalin for HTTP handling and MySQL for persistence.

Key locations:
- [src/main/java/inventario/App.java](src/main/java/inventario/App.java): application entry point
- [src/main/java/inventario/config/ConexionDB.java](src/main/java/inventario/config/ConexionDB.java): database connection setup
- [src/main/java/inventario/model/item.java](src/main/java/inventario/model/item.java): inventory model
- [src/main/java/inventario/dao/ItemDAO.java](src/main/java/inventario/dao/ItemDAO.java): persistence logic
- [src/main/java/inventario/routes/ItemRoutes.java](src/main/java/inventario/routes/ItemRoutes.java): route definitions
- [pom.xml](pom.xml): Maven project configuration

## Architecture conventions
- Keep the project organized by package: `inventario.config`, `inventario.dao`, `inventario.model`, and `inventario.routes`.
- Prefer a simple layered design: model objects, DAO access, and route/controller logic.
- Do not place database logic directly in [src/main/java/inventario/App.java](src/main/java/inventario/App.java); keep it in the config or DAO layers.
- Follow standard Java naming: `PascalCase` for classes and `camelCase` for methods/fields.

## Build and validation commands
Run these from the repository root:
- `mvn compile`
- `mvn test`

To launch the app manually:
- `java -cp target/classes inventario.App`

If the environment has the exec plugin available, this also works:
- `mvn exec:java -Dexec.mainClass=inventario.App`

## Environment expectations
- The application expects a MySQL database at `jdbc:mysql://localhost:3306/inventario_db`.
- The default credentials configured in [src/main/java/inventario/config/ConexionDB.java](src/main/java/inventario/config/ConexionDB.java) are `root` with an empty password.
- If MySQL is unavailable or the schema does not exist, startup or database operations will fail.

## Change guidance for agents
- Keep additions consistent with the existing package structure and naming conventions.
- When adding fields or methods to the inventory entity, update the model class and any DAO logic that depends on it together.
- Favor explicit SQL queries, clear exception handling, and readable variable names.
- Preserve current behavior unless the task explicitly asks for a broader refactor.

## Notes
There is no README or additional project documentation in the repository yet, so these instructions are intentionally minimal and focused on the actual code structure and build workflow.
