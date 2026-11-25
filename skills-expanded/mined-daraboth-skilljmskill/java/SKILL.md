---
name: java
description: Standards for writing clean Java — OOP fundamentals (classes, encapsulation, inheritance, polymorphism), collections, exceptions, try-with-resources, streams, and file I/O. Use when the user writes or reviews Java, builds CLI tools or backend logic in core Java, or asks OOP design questions. Explicitly avoids Spring Boot and other heavyweight frameworks — focuses on vanilla Java MVPs.
---

# Skill: Java

> **Purpose**: Write clean Java code. Build MVPs with no frameworks — just core Java.

## When to Use
- Writing or reviewing Java code
- Building CLI tools or backend logic
- OOP design questions
- File I/O operations

---

## OOP Fundamentals

### Classes — The Blueprint
```java
public class User {
    private final String name;
    private final String email;
    private String role;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
        this.role = "user";
    }

    public String getName() { return name; }
    public String getEmail() { return email; }
    public String getRole() { return role; }

    public void promoteToAdmin() {
        this.role = "admin";
    }

    @Override
    public String toString() {
        return String.format("User{name='%s', email='%s', role='%s'}", name, email, role);
    }
}
```

### Interfaces — The Contract
```java
public interface DataStore<T> {
    void save(T item);
    T findById(int id);
    List<T> findAll();
    void deleteById(int id);
}
```

### Inheritance — Use Sparingly
```java
// Prefer composition over inheritance
// Use interfaces + implementation, not deep class hierarchies

public class FileDataStore implements DataStore<User> {
    private final String filePath;
    private final List<User> users = new ArrayList<>();

    public FileDataStore(String filePath) {
        this.filePath = filePath;
    }

    @Override
    public void save(User user) { users.add(user); }

    @Override
    public User findById(int id) { return users.get(id); }

    @Override
    public List<User> findAll() { return Collections.unmodifiableList(users); }

    @Override
    public void deleteById(int id) { users.remove(id); }
}
```

---

## Method Design

```java
// ✅ Good: single purpose, descriptive name, early return
public Optional<User> findByEmail(String email) {
    if (email == null || email.isBlank()) {
        return Optional.empty();
    }
    return users.stream()
        .filter(u -> u.getEmail().equalsIgnoreCase(email))
        .findFirst();
}

// ❌ Bad: does too much, vague name
public void process(String input) {
    // parses, validates, saves, sends email — pick one
}
```

---

## File I/O

### Reading a File
```java
public static List<String> readLines(String path) {
    List<String> lines = new ArrayList<>();
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        String line;
        while ((line = reader.readLine()) != null) {
            lines.add(line);
        }
    } catch (IOException e) {
        System.err.println("Failed to read " + path + ": " + e.getMessage());
    }
    return lines;
}
```

### Writing a File
```java
public static void writeLines(String path, List<String> lines) {
    try (BufferedWriter writer = new BufferedWriter(new FileWriter(path))) {
        for (String line : lines) {
            writer.write(line);
            writer.newLine();
        }
    } catch (IOException e) {
        System.err.println("Failed to write " + path + ": " + e.getMessage());
    }
}
```

---

## MVP Example: CLI Task Manager

```java
import java.util.*;

public class TaskApp {
    private static final List<String> tasks = new ArrayList<>();
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("=== Task Manager ===");
        boolean running = true;

        while (running) {
            System.out.println("\n1) Add task  2) List tasks  3) Remove task  4) Quit");
            System.out.print("> ");
            String choice = scanner.nextLine().trim();

            switch (choice) {
                case "1" -> addTask();
                case "2" -> listTasks();
                case "3" -> removeTask();
                case "4" -> running = false;
                default  -> System.out.println("Invalid option.");
            }
        }
        System.out.println("Goodbye!");
    }

    private static void addTask() {
        System.out.print("Task: ");
        String task = scanner.nextLine().trim();
        if (task.isEmpty()) {
            System.out.println("Task cannot be empty.");
            return;
        }
        tasks.add(task);
        System.out.println("Added: " + task);
    }

    private static void listTasks() {
        if (tasks.isEmpty()) {
            System.out.println("No tasks yet.");
            return;
        }
        for (int i = 0; i < tasks.size(); i++) {
            System.out.printf("  %d. %s%n", i + 1, tasks.get(i));
        }
    }

    private static void removeTask() {
        listTasks();
        if (tasks.isEmpty()) return;
        System.out.print("Remove #: ");
        try {
            int index = Integer.parseInt(scanner.nextLine().trim()) - 1;
            if (index >= 0 && index < tasks.size()) {
                System.out.println("Removed: " + tasks.remove(index));
            } else {
                System.out.println("Invalid number.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Enter a valid number.");
        }
    }
}
```

**Compile and run**:
```bash
javac TaskApp.java
java TaskApp
```

---

## Best Practices
1. **Use `final` for fields that don't change** — signals intent
2. **Always close resources** — use try-with-resources
3. **Use `Optional` instead of returning null**
4. **Keep classes under 200 lines** — split by responsibility
5. **Explicit imports** — no wildcard `import java.util.*`

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Comparing strings with `==` | Use `.equals()` or `.equalsIgnoreCase()` |
| Not closing streams/readers | Use try-with-resources |
| Giant main() method | Extract into small methods |
| Public fields | Use private fields + getters |
| Catching `Exception` broadly | Catch specific exceptions |
