# Instructions

This are instructions for Cursor to help you understand the content I'm building for my workshop.

This is a practical guide to understanding PostgreSQL's storage mechanisms focused on Rubyists.

My README.md is the main content I'm building for my workshop. The ruby files in the examples directory are examples I'm using to build the content.

Every file should be documented in the README.md file. All concepts are defined in the README using the markdown file assuming it will be rendered in a browser through the github pages feature.


## Markup

You can use markdown in the code to help you understand the code.

For example, you can use ````ascii to draw ascii diagrams.

```ascii
+------------------+
|       Header     |
+------------------+
```

Use mermaid to draw diagrams.

```mermaid
graph TD
    A --> B
    B --> C
```

Use ruby to talk about code and run code.

```ruby
puts "Hello, world!"
```

By default the $DATABASE_URL is set to the local postgres database.

You can change the $DATABASE_URL to connect to a different database.

```bash
export DATABASE_URL="postgres://username:password@localhost:5432/database_name"
```


