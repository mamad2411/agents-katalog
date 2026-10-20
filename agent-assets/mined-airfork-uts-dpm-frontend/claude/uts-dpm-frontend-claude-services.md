# Services

API services and business logic, all singleton via `providedIn: 'root'`.

## Files

| File                      | What                                            | When to read                   |
| ------------------------- | ----------------------------------------------- | ------------------------------ |
| `auth.service.ts`         | Authentication, JWT handling, user data storage | Login/logout, token management |
| `user.service.ts`         | User CRUD API calls                             | User management API            |
| `dpm.service.ts`          | DPM CRUD API calls                              | DPM management API             |
| `approvals.service.ts`    | DPM approval/denial API calls                   | Approval workflow API          |
| `autogen.service.ts`      | Auto-generation API calls                       | Bulk DPM generation API        |
| `datagen.service.ts`      | Data generation API calls                       | Test data API                  |
| `error.service.ts`        | Error state management                          | Error handling                 |
| `format.service.ts`       | Date/time formatting utilities                  | Display formatting             |
| `notification.service.ts` | Toast notification service                      | User notifications             |
