# routes Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `routes` directory of the ICTServe project.

## Directory Overview

The `routes` directory contains all the route definitions for the application. This includes:

* `web.php`: Routes for the web interface.
* `api.php`: Routes for the API.
* `console.php`: Artisan command definitions.
* `channels.php`: Broadcasting channel definitions.

## Instructions

* **Route Definitions:** When adding new routes, group them logically. Use route model binding where appropriate.
* **Naming Conventions:** Follow the existing naming conventions for routes.
* **Middleware:** Apply middleware to routes as needed to protect them and perform other actions.
* **Authentication:** Ensure that routes that require authentication are protected with the `auth` middleware.
