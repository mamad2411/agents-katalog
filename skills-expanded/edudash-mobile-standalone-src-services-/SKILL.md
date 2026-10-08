# Service Layer Rules for EduDash Pro

## API Service Standards

### Supabase Integration
- Always use the Supabase client with proper typing
- Implement RLS (Row Level Security) for multi-tenancy
- Use service role client for Super-Admin operations that bypass RLS
- Include proper error handling for database operations

### Multi-Tenant Data Access
```typescript
// Always include school_id in queries for tenant isolation
const { data, error } = await supabase
  .from('lessons')
  .select('*')
  .eq('school_id', schoolId)
  .eq('teacher_id', teacherId);

// Super-Admin queries can bypass tenant isolation using service client
const { data, error } = await supabaseServiceClient
  .from('schools')
  .select('*'); // No school_id filter needed for platform-wide queries
```

### AI Service Integration
- Abstract all Anthropic Claude API calls into dedicated services
- Implement proper rate limiting and error handling
- Cache responses when appropriate
- Log AI usage for billing and monitoring
- Use streaming responses for better UX on mobile

### Error Handling Patterns
```typescript
export interface ServiceResponse<T> {
  data?: T;
  error?: {
    message: string;
    code?: string;
    details?: any;
  };
  meta?: {
    requestId: string;
    timestamp: Date;
    cached?: boolean;
  };
}

// Always return consistent error responses
export const handleServiceError = (error: unknown): ServiceResponse<never> => {
  console.error('Service error:', error);
  return {
    error: {
      message: error instanceof Error ? error.message : 'Unknown error',
      code: 'SERVICE_ERROR',
      details: error
    },
    meta: {
      requestId: crypto.randomUUID(),
      timestamp: new Date()
    }
  };
};
```

### File Upload Services
- Use Supabase Storage with proper bucket policies
- Implement file type validation and size limits
- Generate secure URLs with expiration
- Handle mobile-specific upload considerations (network reliability)

### Real-time Services
- Use Supabase real-time subscriptions for live updates
- Implement proper connection handling for mobile networks
- Handle offline scenarios gracefully
- Clean up subscriptions to prevent memory leaks

### Authentication Services
- Implement role-based access control (RBAC)
- Handle session management across different user types
- Support impersonation for Super-Admin support
- Include proper logout and session cleanup

### Service Layer Structure
```typescript
// services/
├── auth/
│   ├── authService.ts          # Authentication logic
│   ├── roleService.ts          # Role management
│   └── impersonationService.ts # Admin impersonation
├── ai/
│   ├── lessonGenerator.ts      # AI lesson creation
│   ├── gradingService.ts       # AI-powered grading
│   └── chatService.ts          # AI chat interactions
├── data/
│   ├── schoolService.ts        # School/tenant management
│   ├── userService.ts          # User management
│   └── contentService.ts       # Lessons, homework, etc.
├── media/
│   ├── uploadService.ts        # File uploads
│   └── storageService.ts       # Storage management
└── notifications/
    ├── pushService.ts          # Push notifications
    └── emailService.ts         # Email notifications
```

### Performance Considerations
- Implement proper caching strategies
- Use pagination for large datasets
- Optimize queries for mobile networks
- Consider offline-first approaches where appropriate
- Monitor and log performance metrics
