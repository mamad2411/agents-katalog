---
name: wpcom-rest-api-reference
description: "Comprehensive Guide to WordPress.com REST API Endpoints. A reference for using the WordPress.com v1.1 REST API to read, write, and manage WordPress.com site data."
---

# WordPress.com REST API Reference

The **WordPress.com REST API** (`v1.1`) provides a comprehensive suite of endpoints to manage WordPress.com sites, user accounts, and Jetpack-connected self-hosted sites.

## Endpoint Structure

The base URL for the WordPress.com REST API is:
`https://public-api.wordpress.com/rest/v1.1/`

*Note: While standard WordPress Core uses `/wp-json/wp/v2/`, WordPress.com exposes many proprietary endpoints through its custom `v1.1` structure.*

## Key Endpoint Categories

### 1. Sites
Manage site settings, metadata, and general information.
* **GET `/sites/{site}`**: Retrieve information about a specific site (by domain or site ID).
* **POST `/sites/{site}`**: Update site settings (title, description, timezone).

### 2. Posts & Pages
Create, read, update, and delete content.
* **GET `/sites/{site}/posts`**: Fetch a list of published posts (supports pagination, filtering by category/tag/author).
* **POST `/sites/{site}/posts/new`**: Create a new post.
* **POST `/sites/{site}/posts/{post_ID}`**: Update an existing post.

### 3. Users & Authentication
Manage user profiles and roles.
* **GET `/me`**: Get information about the currently authenticated WordPress.com user.
* **GET `/sites/{site}/users`**: List all users registered on a specific site.

### 4. Comments
Manage engagement and moderation.
* **GET `/sites/{site}/posts/{post_ID}/replies`**: Fetch comments for a specific post.
* **POST `/sites/{site}/comments/{comment_ID}`**: Approve, spam, or delete a comment.

### 5. Media
Manage the WordPress.com media library.
* **GET `/sites/{site}/media`**: List uploaded media items.
* **POST `/sites/{site}/media/new`**: Upload a new media file (supports multipart form data).

## Authentication

Most `GET` requests for public data do not require authentication. However, interacting with private sites or executing `POST`/`DELETE` requests requires an **OAuth2 Bearer Token**.

To authenticate a request, include the token in the `Authorization` header:
```bash
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Pagination & Limits

* **Default Limit**: Most list endpoints return 20 items by default.
* **Max Limit**: You can usually request up to 100 items per page using the `number=100` query parameter.
* **Offset/Page**: Navigate through results using `page=2` or `offset=20`.

## Rate Limiting
The WordPress.com REST API is rate-limited to ensure stability. If you exceed the limits, you will receive a `429 Too Many Requests` HTTP status code. Ensure your application implements exponential backoff and respects the `Retry-After` header.
