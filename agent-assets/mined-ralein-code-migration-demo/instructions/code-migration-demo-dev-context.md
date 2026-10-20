---
description: "Local development environment context — database credentials, Tomcat configuration, service ports, local URLs. SELF-MAINTAINING: Append new ports/URLs/env as you discover them."
applyTo: "**"
---

# Local Development Environment

Self-Maintaining Instruction: If during any task you discover new database credentials, service ports, local URLs, environment variables, or other dev environment details that are NOT already listed here — append them to the appropriate section below. Keep entries concise and consistent.

---

## Databases

### Oracle (legacy)

| Service           | Host      | Port | User   | Password      | SID/Service |
| ----------------- | --------- | ---- | ------ | ------------- | ----------- |
| VehicleServiceApp | localhost | 1521 | SYSTEM | <set locally> | XEPDB1      |

Evidence: README.md (DBConnection snippet)

### SQLite (local dev via mock Oracle driver)

| Service           | File path          | Notes                                                          |
| ----------------- | ------------------ | -------------------------------------------------------------- |
| VehicleServiceApp | vehicle_service.db | Created/initialized by mock driver; table VEHICLE auto-created |

Evidence: run.md

## Cache / Key-Value

| Service                             | Host | Port | Auth |
| ----------------------------------- | ---- | ---- | ---- |
| _None detected — confirm with team_ |      |      |      |

## Message Brokers

| System                              | Local Endpoint | Management UI | Credentials |
| ----------------------------------- | -------------- | ------------- | ----------- |
| _None detected — confirm with team_ |                |               |             |

## Object Storage

| System                              | Endpoint | Bucket | Credentials |
| ----------------------------------- | -------- | ------ | ----------- |
| _None detected — confirm with team_ |          |        |             |

## Search / Analytics

| System                              | Endpoint | Index / Database |
| ----------------------------------- | -------- | ---------------- |
| _None detected — confirm with team_ |          |                  |

---

## Native Run (no containers)

| Process   | Start command (bash)                                                                                                                          | Start command (PowerShell) | Stop / restart                       |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------ |
| Tomcat 9  | export JAVA_HOME=/home/ralein/Desktop/Insurance-Portal/Backend/jdk && export PATH=$JAVA_HOME/bin:$PATH && /home/ralein/tomcat9/bin/startup.sh | <confirm with team>        | /home/ralein/tomcat9/bin/shutdown.sh |
| Tail logs | tail -f /home/ralein/tomcat9/logs/catalina.out                                                                                                | <confirm with team>        | Ctrl+C                               |

### Tomcat Context Mapping

- Context path: /VehicleServiceApp
- docBase: /home/ralein/Desktop/VehicleServiceApp/src/main/webapp
- Classes mount: /home/ralein/Desktop/VehicleServiceApp/build/classes (per run.md example)

---

## Local URLs

| Service        | URL                                                       |
| -------------- | --------------------------------------------------------- |
| Dashboard      | http://localhost:8080/VehicleServiceApp/                  |
| View Vehicles  | http://localhost:8080/VehicleServiceApp/viewVehicles      |
| Search Vehicle | http://localhost:8080/VehicleServiceApp/searchVehicle.jsp |

## Credential / Config Files

| File                                   | Contents (summary)                                 |
| -------------------------------------- | -------------------------------------------------- |
| src/main/webapp/WEB-INF/lib/ojdbc8.jar | Oracle JDBC driver (legacy usage)                  |
| vehicle_service.db                     | SQLite DB file for local development (mock driver) |

---

## Environment Variables (Names Only)

| Variable  | Used By                    | Purpose                                   |
| --------- | -------------------------- | ----------------------------------------- |
| JAVA_HOME | Tomcat run scripts (local) | Point to JDK used for Tomcat              |
| PATH      | Shell                      | Ensure JAVA_HOME/bin precedes system Java |
