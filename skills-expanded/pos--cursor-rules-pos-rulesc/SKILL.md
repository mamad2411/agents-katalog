---
description: 
globs: 
alwaysApply: true
---
Here’s a **text-based project rules document** specifically tailored to your **Spring Boot POS system backend** using **Maven and MySQL**, without Swagger or MapStruct:

---

# 📄 Project Rules: POS System Backend (Spring Boot)

## 1. Project Setup

* **Build Tool:** Maven
* **Database:** MySQL
* **Java Version:** 17 or latest LTS version
* **Frameworks and Libraries:**

  * Spring Boot
  * Spring Web
  * Spring Data JPA
  * Spring Validation
  * Lombok
  * MySQL Connector
  * Spring Security (if required)

---

## 2. Project Structure

Organize the project using a clean, layered structure:

```
src/main/java
 └── com.pos
      ├── controller
      ├── service
      ├── repository
      ├── model
      ├── dto
      ├── config
      └── exception
```

* Use lowercase package names.
* Separate concerns clearly: controllers handle HTTP, services handle business logic, repositories handle database access.

---

## 3. API Design

* Use RESTful API principles.
* Base URL: `/api/v1/`
* Example Endpoints:

  * `GET /api/v1/products`
  * `POST /api/v1/products`
  * `POST /api/v1/sales`
  * `GET /api/v1/sales/{id}`
* Use plural nouns for resources.

---

## 4. Database Design

* Tables:

  * `products`
  * `categories`
  * `sales`
  * `sale_items`
  * `users` (optional)
* Relationships:

  * Category → Products (One-to-Many)
  * Sale → Sale Items (One-to-Many)
  * Sale Item → Product (Many-to-One)
* Use auto-increment IDs or UUIDs as primary keys.
* Ensure proper normalization.

---

## 5. Validation Rules

* Validate all API inputs using Spring’s `@Valid` and validation annotations in DTOs.
* Validate:

  * Product price > 0
  * Product quantity ≥ 0
  * Non-empty fields for product name, category name, customer name

---

## 6. Transaction Management

* Use `@Transactional` at the service layer for multi-step operations.
* Ensure stock is properly updated when a sale is made.
* All related changes should be committed or rolled back together.

---

## 7. Error Handling

* Use global exception handling with `@ControllerAdvice`.
* Return a consistent error response structure:

```
{
  "timestamp": "2025-06-30T10:00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Product not found",
  "path": "/api/v1/products/1"
}
```

---

## 9. Security (If Required)

* Secure APIs using Spring Security.
* Consider using JWT for stateless authentication.
* Protect endpoints like sales creation or inventory updates.


