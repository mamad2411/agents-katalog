# C# Best Practices and Rules

## Core Rules for Junior Developers

### 1. Always Use Proper Disposal for IDisposable Objects

```csharp
// ❌ BAD: Resource not properly disposed
SqlConnection connection = new SqlConnection(connectionString);
connection.Open();
// ... do work ...
// Connection might never be closed!

// ✅ GOOD: Using statement ensures proper disposal
using (SqlConnection connection = new SqlConnection(connectionString))
{
    connection.Open();
    // ... do work ...
} // Connection automatically disposed here

// ✅ EVEN BETTER: Modern using declaration (C# 8.0+)
using var connection = new SqlConnection(connectionString);
connection.Open();
// ... do work ...
// Connection disposed at end of scope
```

### 2. Use Null Checking and Null-Conditional Operators

```csharp
// ❌ BAD: Potential NullReferenceException
public string GetUserEmail(User user)
{
    return user.Email.ToLower(); // Will crash if user or Email is null
}

// ✅ GOOD: Proper null checking
public string GetUserEmail(User user)
{
    if (user == null)
        throw new ArgumentNullException(nameof(user));

    return user.Email?.ToLower() ?? "no email";
}

// ✅ BETTER: Using C# 8.0+ null-safety
public string GetUserEmail(User user)
{
    ArgumentNullException.ThrowIfNull(user);
    return user.Email?.ToLower() ?? "no email";
}
```

### 3. Use Strong Typing and Avoid Magic Strings/Numbers

```csharp
// ❌ BAD: Magic strings and numbers
public void ProcessOrder(string status)
{
    if (status == "pending") // Magic string
    {
        // Process with magic number
        CalculateDiscount(100); // What does 100 mean?
    }
}

// ✅ GOOD: Using enums and constants
public enum OrderStatus
{
    Pending,
    Processing,
    Completed
}

public class OrderProcessor
{
    private const decimal StandardDiscountRate = 100m;

    public void ProcessOrder(OrderStatus status)
    {
        if (status == OrderStatus.Pending)
        {
            CalculateDiscount(StandardDiscountRate);
        }
    }
}
```

## Additional Tips

1. **Exception Handling**

   - Use specific exception types instead of catching Exception
   - Only catch exceptions you can handle
   - Always include meaningful exception messages
   - Use try-catch blocks only when necessary

2. **Code Organization**

   - Follow consistent naming conventions
   - Keep methods small and focused
   - Use meaningful variable names
   - Group related functionality into classes

3. **Performance**

   - Use StringBuilder for string concatenation in loops
   - Implement IDisposable for classes with unmanaged resources
   - Use async/await for I/O operations
   - Consider using value types for small, simple types

4. **Common Pitfalls to Avoid**
   - Don't ignore exceptions
   - Don't use public fields (use properties instead)
   - Don't return null collections (return empty ones)
   - Don't use string concatenation in loops
