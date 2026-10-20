# database Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `database` directory of the ICTServe project.

## Directory Overview

The `database` directory contains everything related to the application's database, including:

* **Migrations:** Files that define the database schema.
* **Factories:** Model factories for generating test data.
* **Seeders:** Files for seeding the database with initial data.

## Instructions

* **Migrations:** When creating new migrations, use the `laravel/pint` conventions for formatting. Ensure that each migration has a `down()` method to make it reversible.
* **Factories:** When creating factories, use the Faker library to generate realistic data.
* **Seeders:** Use seeders to populate the database with essential data for the application to run. Keep seeders organized and focused on a specific purpose.
