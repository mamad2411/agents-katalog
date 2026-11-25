---
description: 
globs: 
alwaysApply: false
---
# Rule: Development Best Practices and Anti-Over-Engineering
## Goal
To provide clear guidance on common development scenarios, prevent over-engineering, and promote simple, maintainable solutions based on 100+ project experience.

## Core Philosophy
**SIMPLE FIRST, OPTIMIZE LATER** - Always start with the simplest solution that works. Complexity should be added only when there's a clear, measurable need.

## Common Scenarios and Solutions

### State Management
**❌ Over-engineered:**
```javascript
// Don't create complex Redux store for simple UI state
const userProfileSlice = createSlice({
  name: 'userProfile',
  initialState: { isEditing: false, showTooltip: false },
  reducers: { ... }
});
```

**✅ Simple solution:**
```javascript
// Use local state for UI-only state
const [isEditing, setIsEditing] = useState(false);
const [showTooltip, setShowTooltip] = useState(false);
```

### API Calls
**❌ Over-engineered:**
```javascript
// Don't create complex service classes for simple API calls
class UserService {
  private apiClient: AxiosInstance;
  constructor() { ... }
  async getUser(id: string): Promise<ApiResponse<User>> { ... }
}
```

**✅ Simple solution:**
```javascript
// Use simple async functions
const getUser = async (id: string): Promise<User> => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
};
```

### Form Handling
**❌ Over-engineered:**
```javascript
// Don't create complex form builders for simple forms
const formConfig = {
  fields: [
    { name: 'email', type: 'email', validators: [...] },
    { name: 'password', type: 'password', validators: [...] }
  ]
};
```

**✅ Simple solution:**
```javascript
// Use react-hook-form with zod for straightforward validation
const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(loginSchema)
});
```

## When to Add Complexity

### Add abstractions when:
- **Rule of 3**: You're repeating the same pattern in 3+ places
- **Clear performance issue**: Profiling shows actual bottlenecks
- **Specific requirement**: Business needs demand the complexity

### Don't add abstractions for:
- **Hypothetical future needs**: "We might need this later"
- **Developer preference**: "I like this pattern better"
- **Resume-driven development**: Using tech because it's trendy

## Code Patterns to Prefer

### Custom Hooks (Good abstraction)
```javascript
// Extract reusable logic into custom hooks
const useUser = (id: string) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    getUser(id).then(setUser).finally(() => setLoading(false));
  }, [id]);
  
  return { user, loading };
};
```

### Utility Functions (Good abstraction)
```javascript
// Create utilities for common operations
const formatCurrency = (amount: number, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};
```

### Configuration Objects (Good for flexibility)
```javascript
// Use config objects for components with many options
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}
```

## Red Flags to Watch For
1. **More files than features**: Creating multiple files for a single simple feature
2. **Deep nesting**: More than 3 levels of folder nesting without clear purpose
3. **Abstract naming**: Generic names like `Manager`, `Handler`, `Service` without context
4. **Premature optimization**: Adding caching, memoization, or complex patterns before measuring need
5. **Framework within framework**: Building custom abstractions on top of well-established libraries

## Decision Framework
When facing a technical decision, ask:
1. **Is this the simplest solution that works?**
2. **Can I implement this in under 30 minutes?**
3. **Will a junior developer understand this in 6 months?**
4. **Am I solving a real problem or an imaginary one?**

If any answer is "no," reconsider the approach.

## Code Examples Library

### Authentication Hook
```javascript
const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      verifyToken(token).then(setUser).catch(() => {
        localStorage.removeItem('token');
      }).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials) => {
    const { user, token } = await loginUser(credentials);
    localStorage.setItem('token', token);
    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return { user, loading, login, logout };
};
```

### Error Handling
```javascript
const withErrorHandling = (asyncFn) => {
  return async (...args) => {
    try {
      return await asyncFn(...args);
    } catch (error) {
      console.error('Operation failed:', error);
      toast.error('Something went wrong. Please try again.');
      throw error;
    }
  };
};
```

### API Response Handler
```javascript
const handleApiResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'Request failed');
  }
  return response.json();
};

```