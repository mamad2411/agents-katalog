# todo 
- system implementation database with api: 
datasets (proc results) that contain aggregated data that may have stale data or other warnings will contain an exceptionid column with a fk to 
a exception table with a message and a json structured detail field which will be the parameters for a reprocessing job and queue based on dependencies. data driven. 
apis returning such data will append the exception data or query for it. 
- within a topic, the subtopics/pages will have a control at the top where the input praams are that allows them to choose to use the same param values as another 
page/tab in the topic allowing ppl to carry state from one tab to the other smoothly. 

## context
This project/repository is one of several that together make up the "bor" (for Book of Record) system.
The system's projects/repositories (herein called "modules") will consist of heterogeneous elements such as database(s), api(s), client application(s), service(s) and will referred to collectively as the "system" or "bor system". 
Some modules such as databases and apis are "core modules" without which the system cannot function; some modules are optional and can be subscribed to by clients. 
EACH MODULE WILL CONTAIN ITS OWN .CURSORRULES DOCUMENT. THIS AND ONLY THIS .CURSORRULES WILL CONTAIN DOCUMENTATION ABOUT THE SYSTEM AS A WHOLE, 
AND INFORMATION THAT IS COMMON TO ALL MODULES TO AVOID DUPLICATION. 

The system will be used by investment management firms for investment management, risk management, reporting, internal operations, etc.

## core completency
The core competency of the system is data management. 
This sytem will function at the center of many operations and processes within investment management firms. 
Investment management is a data centric industry; data management copmetency is required, this application will excel at data management. 
Examples of what this system will be excellent at:
- reliable, flexible and transparent extract transform and load jobs with dependencies
- metadata validation of business rules in the data
- metadata for subject matter content data (e.g. that in the 'borinst' database which holds investment management data) including table dependencies 
recording denormalized or aggregate tables' dependencies on 3nf tables. 
- metadata for transformations, jobs, job execution
- data processing jobs particularily ETL will be performed by an independent data service which is a core module and can be executed
in an asynchronous manner using the system's messaging middleware. 


## system high level architecture
- application: 
   . user interface
   . handles authentication, jwt issuance
   . handles application level rbac
   . handles jwt header addition for api rbac
   . interacts with data via api and/or services
   
- api(s):

   . abstraction layer above database
   . business domain model
   . standard REST api patterns
   . horizontal scaling

- mysql databases: 
   . domain context
   . redundancy frequency
   . application data
   . data management metadata
   . data validation metadta

- service(s):
   . special purpose functions, transformations, calculations, workflow orchestration
   . separate processes for load balancing

- file storage (bor-files container):
   . ftp server
   . file organization
   . file storage metadata

- sync interprocess communication:
   . docker network
   . TCP/IP between the API and database. 
   . HTTPS between the application and the API. 
   . asynch using message oriented middleware (message service) / message broker implemented with kafka (can also be used to push to next.js web application).
      .. avoid triggers (event storm) preferring metadata on depends, statuses and service polling. events for request, response with service. 

- async interprocess communication approach:
   . docker network
   . bor-message messaging service implementing kafka
   . facilitate asynchronous communication between services
   . consider metadata-polling approach (instead of triggering)
      .. Controlled Execution: No surprise cascades of activity (eventstorms)
      .. Centralized Visibility: Complete system state available in one place in bormeta database
      .. Operational Control: Ability to pause, restart, or reschedule at granular levels
      .. Simpler Debugging: Clear lineage of job execution
      .. Better Resource Management: Workers scale based on available work, not reaction to events


## technical details 
This project will be developed to a high standard of quality but will favour simplicity over sophistication in design and implementation.
Advice and input from AI will be given as an expert professional using industry best practices for the technologies used. 

# secrets
All secrets will be stored in .env files using standard techniques for the technologies used. .env files will follow this naming convention:
- .env
- .env.local
- .env.development
- .env.development.local *not pushed to git
- .env.production
- .env.production.local * not pushed to git

# ports
to see ports in use:
sudo ss -tulwn | grep LISTEN | sort -k5 -n

container      dev   stage prod  docker-internal
-----------------------------------------------
bor-app        4400  4500  4600  3000
bor-api        4410  4510  4610  4000
bor-db         4420  4520  4620  3306
bof-message    4430  4530  4630  9092
bor-workflow   4440  4540  4640  8080
bor-etl        4450  4550  4650  8888
bor-svc-calc   4460  4560  4660  5000
bor-files      4470  4570  4670  21


999999999
This project will create a file storage container for use with the bor project, most specifically the bor-workflow and bor-etl containers. 
The storage container will be accessible from outside its docker container by ftp and over the docker network from the bor-* containers. 
A top requirement is that this is a light and simple to admin implementation of an ftp server, file organization and storage container.
The context is an early stage project that has a next.js web application, a node express api, a mysql 8 database, a workflow service, and an etl service. All are running in separate processes in separate docker containers. 
This service will be used initially in the following business case: a file is ftpd by an external system into the storage container; the workflow service will read the file and use the information to determine the next step in the workflow, which is to run the etl service; the etl service 
will load the data into staging tables in the mysql 8 docker containern database for further processing. 
A simple and flexible implementation is required with transparency into the file storage and organization and easyly managet 
FTP accounts and permissions.

99999999999




# technologies used
- Typescript
- Next.js
- shadcn
- Tailwind CSS.
- Prisma
- Docker
- Node.js
- Auth.js with Google OAuth provider
- Zustand 
- Git
- Github and github actions for CI/CD to production
- Application access will be protected with a RBAC (Role Based Access Control) mechanism using the Prisma tables: 
    . Account
    . Session
    . PrismaUser * see note on this table
    . VerificationToken
    . Role
    . Permission
    . UserRole
    . RolePermission
    . AuthActivity
    ** Note: the above database tables have been created in the 'bor' database (running in bor-db) and seeded, *removing the need for prisma pull, don't do it*. 



## application security 
- The system will use HTTPS communication between the browser and application server. 
- User interface components and navigation links will be restricted by RBAC. 
- API endpoints will use JWTs to enfoce RBAC (*see section below on RBAC coordination with API). 
- Nextauth will use OAuth providers to perform authentication. 
- The 'bor' application will be used to facilitate authentication and rbac using the prisma library and framework. The 'bor' database will hold this data. 
- The database is not exposed outside of the docker network. 
- Users will authenticate via Auth.js using one or more OAuth providers which will work in conjunction with the mysql database and prisma for users, roles, and permissions in conjunction with systems rbac. Prisma will also be used by the app to test the prisma connection to the database. 


## data security 
...

## high availability 
- database volume separation for different backup-restore schedules 

#### for bor-etl 
   # spark/????
   Create domain-specific Spark applications that can be parameterized
   Use the LocalExecutor initially (avoids complex distributed setup)
   Package Spark jobs as self-contained applications
   ### Spark Processing
   - Executes transformation logic
   - Performs data quality checks
   - Handles large dataset operations
   - Runs analytics calculations
   - data on jobs, status, dependencies, etc. accessible to the application for dashboards, monitoring, etc. in bormeta database

 ### worflows management and orchestration
   - Schedules ETL job execution
   - Manages data processing dependencies
   - Handles retries and failure notifications
   - Monitors pipeline health
   - data on jobs, status, dependencies, etc. accessible to the application for dashboards, monitoring, etc. in bormeta database
    

## data validation
   - view-based including compliance checks: use a view of the portfolio 
   - to the extent possible the database itself embeds a lot of validation logic, but 
   for the benefit of flexibility higher layers of the application will perform additional validation. 
   - validation rules, checks, reports will be data driven to the extent possible. 
   - industry best practices will be used for validation rules. 
   - validation logic will be stored in the bormeta database. 
   - validation reports and dashboards as well as supporting troubleshooting tools will be developed using the bormeta database. 
   - consider using rules engine for data validation *and* portfolio compliance checking which 
   is a potential core module of this system. 

   ### Integration Methods
   - Use SparkSubmitOperator for job invocation
   - Pass dynamic parameters to Spark jobs
   - Store results for subsequent tasks
   - Use XComs for task communication

   ### Example Workflow
   1. Airflow initiates market data extraction
   2. Spark processes and normalizes market data
   3. Airflow verifies completion and triggers next steps
   4. Spark joins market data with portfolio holdings
   5. Airflow manages downstream distribution


The application will exist in these git repositories: 
- bor-db 
   . databases for application management, application data, metadata
- bor-api 
   . REST api for application, user management and database interaction
- bor-message
   . message middleware for asynchronous communication
- bor-workflow
   . workflow orchestration and management
   . 
- bor-etl
   . service to facilitate data movement and transformation
   . 
- bor-svc-calc
   . service to facilitate numerical or proceses-intensive calculations
   . can be invoked asychronously using bor-mmw infrastructure
- bor-app * this repository
   . user interface for system administration, application management including authentication, role-based access control.
   . user interface for data management, ETL, processing, and reporting
   . user interface for investment management, portfolio management, position management, transaction management, allocation, and reporting
   . api endpoints, which are not in bor-api, for user, role, permission, etc. management
- bor-files
   . file storage container
   . ftp server
   . file organization
   . file storage metadata

Each of these will be independently deployable and together function as the full application.
Each of the projects/repositories will be deployed as Docker containers on a single server or on different servers.


## information architecture
# roughly following domain based design
# navigation and page routes will be similar but not identical
# navigation schema will roughly follow the path part after the version (e.g. app/ admin/ portfolio)
# the web application navigation will be organized into "topics" which roughly correspond to the third path element below (e.g. after /api/<version>/). Each topic has one or 
more pages associated with it. The topic's pages are organized into a tabbed layout. The topics and pages are defined in the central navigation configuration.

   

# api structure
# * note that within the next.js app (bor-app), api routes have api/ at the root of the path, while the 
#  standalone api (bor-api) begins the route path with the version v1/ as the root. 

# application administration mostly 'bor' database endpoints
-: implemented in bor-app
=: implemented in bor-api
</nextjsapp/path/route> : </expressapi/path/route>
-GET   /api/admin/users : n/a (prisma direct db connection)
-GET   /api/admin/user-approval : n/a (prisma direct db connection)
-GET   /api/admin/roles : n/a (prisma direct db connection)
-GET   /api/admin/permissions : n/a (prisma direct db connection)
-GET   /api/auth/...
GET   /api/user/...
GET   /api/v1/app/admin/dashboard//
# sysadmin also 'bor' database endpoints
-GET   /api/system/health

GET   /api/v1/app/sys/application
GET   /api/v1/app/sys/client/
GET   /api/v1/app/sys/client{id}/theme/
GET   /api/v1/app/sys/database
GET   /api/v1/app/sys/database{instance}/backup
GET   /api/v1/app/sys/database{instance}/restore
# data management, processing, datasets (get, post, put)
/api/v1/data/cache/
/api/v1/data/cache/{id}[expire | refresh | status | etc]
POST   /api/v1/data/validate               # Validate data integrity
GET    /api/v1/data/audit                  # Get data change audit log
GET    /api/v1/data/process/
GET    /api/v1/data/dataset/prices                 # Get prices (with filtering)
POST   /api/v1/data/dataset/prices                 # Upload/update price data
GET    /api/v1/data/dataset/fx                     # Get FX rates
   /api/v1/data/bulk # GET POST
POST /api/v1/data/dataset/positions #load positions can filter out parts of source (e.g. only load one portid or dateval)
# workflow
GET    /api/v1/workflow/{id}/etc, etc, etc/step/etc.
GET    /api/v1/workflow/
# message
GET    /api/v1/message/....

# portfolio management
GET    /api/v1/port                   # List portfolios (with filtering)
GET    /api/v1/port/{id}              # Get portfolio details
POST   /api/v1/port                   # Create portfolio
PUT    /api/v1/port/{id}              # Update portfolio
GET    /api/v1/port/{id}/holdings     # Get current holdings
GET    /api/v1/port/{id}/performance  # Get performance metrics
GET    /api/v1/port/{id}/attributes   # Get portfolio attributes
POST   /api/v1/port/{id}/rebalance    # Rebalance portfolio
GET    /api/v1/port/{id}/cashflows    # Get pending/historical cashflows
POST   /api/v1/port/{id}/cashflows    # Register new cashflow
   /api/v1/port/{id}/compliance
# compliance
GET    /api/v1/compliance
# 
GET    /api/v1/instrument                  # List instruments (with filtering)
GET    /api/v1/instrument/{id}             # Get instrument details
POST   /api/v1/instrument                  # Create instrument
PUT    /api/v1/instrument/{id}             # Update instrument
GET    /api/v1/instrument/{id}/pricing     # Get pricing history
GET    /api/v1/instrument/{id}/analytics   # Get instrument analytics
GET    /api/v1/instrument/search           # Search instruments
GET    /api/v1/instrument/sectors          # Get sector classifications
GET    /api/v1/instrument/assetclasses     # Get asset class hierarchy
#

GET    /api/v1/transaction                 # List transactions (with filtering)
GET    /api/v1/transaction/{id}            # Get transaction details
POST   /api/v1/transaction                 # Create transaction
PUT    /api/v1/transaction/{id}            # Update transaction
GET    /api/v1/transaction/pending         # Get pending transactions
POST   /api/v1/transaction/execute         # Execute pending transactions
POST   /api/v1/transaction/cancel          # Cancel pending transaction
GET    /api/v1/transaction/compliance      # Check transaction compliance
#
GET    /api/v1/risk/port/{id}/var     # Get Value at Risk
GET    /api/v1/risk/port/{id}/relvar  # Get Relative VaR (vs benchmark)
GET    /api/v1/risk/port/{id}/stress  # Run stress test scenarios
GET    /api/v1/risk/port/{id}/factors # Get factor exposures
GET    /api/v1/risk/port/{id}/limits  # Get risk limits status
POST   /api/v1/risk/port/{id}/limits  # Set risk limits
GET    /api/v1/risk/port/{id}/concentration # Get concentration risks
#
GET    /api/v1/analytics/port/{id}/performance
GET    /api/v1/analytics/port/{id}/attribution    # Performance attribution
GET    /api/v1/analytics/port/{id}/comparison     # Benchmark comparison
GET    /api/v1/analytics/port/{id}/allocation     # Asset allocation analysis
GET    /api/v1/analytics/port/{id}/scenario       # Run scenario analysis
GET    /api/v1/analytics/port/{id}/optimization   # Portfolio optimization
GET    /api/v1/analytics/port/{id}/forecasts      # Return forecasts
#
GET    /api/v1/report/templates            # Get report templates
POST   /api/v1/report/generate             # Generate custom report
GET    /api/v1/report/scheduled            # Get scheduled reports
POST   /api/v1/report/schedule             # Schedule report generation
GET    /api/v1/report/history              # Get report history
#
# batch operations for common operations
POST /api/v1/transaction/batch  # Create multiple transactions
POST /api/v1/data/prices/batch  # Update multiple prices

# prisma endpoints for Auth and RBAC

## Authentication API (`/api/auth`)
- **Next Auth Handler** (`/api/auth/[...nextauth]`)
  - GET, POST: Handle all authentication operations via Auth.js (NextAuth)
  - Features: Google OAuth provider, JWT session handling, container hostname fixes

- **User Synchronization** (`/api/auth/sync-user`)
  - POST: Syncs authenticated users to Prisma database
  - Requires valid session
  - Creates/updates PrismaUser records and assigns roles

## Admin API (`/api/admin`)
- **User Management** (`/api/admin/users`)
  - GET: Lists all users with their roles
  - PATCH: Updates user approval status
  - Requires 'appadmin' role

- **User Approval** (`/api/admin/user-approval`)
  - Manages user access approval to the system

- **Role Management** (`/api/admin/roles`)
  - Manages RBAC roles

- **Permission Management** (`/api/admin/permissions`)
  - Manages RBAC permissions

## User API (`/api/user`)
- **Session Information** (`/api/user/session-info`)
  - Provides current user session data

- **Data Refresh** (`/api/user/refresh-data`)
  - Refreshes user-specific data

## System API (`/api/system`)
- **Health Check** (`/api/system/health`)
  - GET: Comprehensive system health check
  - Checks API connectivity and database connection
  - Returns detailed component status

## Debug API (`/api/debug`)
- **Static Debug Information** (`/api/debug/static`)
  - Development tools for debugging

## Database Testing (`/api/test-db`)
- Tests database connectivity 

## Proxy Image API (`/api/proxy-image`)
- Proxies image requests to avoid CORS issues

## API Implementation Notes

1. **Security**:
   - Protected endpoints use Auth.js sessions
   - Admin endpoints require 'appadmin' role
   - JWT tokens for API authorization

2. **Error Handling**:
   - Consistent error format with status codes
   - Detailed error messages for troubleshooting

3. **Response Format**:
   - Standardized success/error responses
   - Consistent data structures

4. **Architecture**:
   - Dynamic routing for data freshness
   - Proxy pattern to bor-api service with auth data


## api client service

The BOR system uses a centralized API client service to standardize and simplify interactions between the bor-app frontend and the bor-api backend. This service handles all external API calls and provides a consistent interface for making requests.

### Purpose

1. **Standardization**: Provides a single, consistent way to make API requests across the application
2. **Request Management**: Handles URL construction, headers, authentication tokens, and request formatting
3. **Response Processing**: Standardizes error handling, response parsing, and status code management
4. **Versioning**: Manages API versioning through configuration rather than code changes
5. **Authentication**: Automatically includes auth tokens and handles authentication-related errors

### Main Functionality

1. **Core Request Methods**:
   - `get(endpoint, options)`: For retrieving data
   - `post(endpoint, data, options)`: For creating resources
   - `put(endpoint, data, options)`: For updating resources
   - `delete(endpoint, options)`: For removing resources
   - `patch(endpoint, data, options)`: For partial updates

2. **URL Construction**:
   - Maps internal paths to external API paths
   - Handles versioning (`/api/v1/...`)
   - Supports both absolute and relative endpoint paths

3. **Authentication**:
   - Automatically adds JWT tokens to requests
   - Refreshes tokens when needed
   - Handles authentication failures

4. **Error Handling**:
   - Standardizes error responses
   - Provides meaningful error messages
   - Supports retry logic for temporary failures
   - Maps HTTP status codes to application-specific errors

5. **Caching**:
   - Optional response caching for GET requests
   - Cache invalidation on mutations
   - Configurable cache duration

### Implementation Details

1. **Architecture**:
   - TypeScript class-based implementation
   - Singleton pattern for application-wide use
   - Modular design with separate concerns for different aspects

2. **Configuration**:
   - Environment-based API URL selection
   - Configurable timeout and retry settings
   - Versioning configuration

3. **Integration Points**:
   - React hooks for component-level API access
   - Server-side implementation for API routes
   - Context provider for application-wide configuration

4. **Route Mapping**:
   - Configuration-driven mapping between internal and external routes
   - Support for path parameters and query strings
   - Validation of required parameters

5. **Security**:
   - CSRF protection
   - Safe handling of sensitive information
   - Prevention of common API vulnerabilities

This API client service ensures that all communication between the frontend and backend follows consistent patterns, reducing duplication and making maintenance easier as the application grows.

## jwt creation, payload, management
see ./docs/auth-jwt/api-coordination.md
see ./docs/auth-jwt/jwt-implementation.md
see ./docs/auth-jwt/README.md


-- above is system-wide information, below is bor-app information 
      -- after editing this file, copy to related repo's ref/ dir 
      -- e.g.: cp .cursorrules ../bor-db/ref/.cursorrulesMAIN
----------------------------------------------------------------------------------

## application description
This project creates a Next.js web application that will use the API created in the bor-api project. The web application will be used in the context 
of an institutional investment management firm. The application will have three catefories of functionality:
1 application and user administration including authentication, role-based access control, and user preferences
2 investment management functionality including position management, transaction management, allocation, and reporting
3 data management functionality including ETL jobs, processing jobs, data health and validation, and system monitoring
These three categories will have a single page application (SPA) style interface.

## technology, general:
- This project will create a Next.js web application that will use the API created in the bor-api project which uses the database created in the bor-db project. 
- A docker network called 'bor-network' will be created to allow the containers to communicate with each other.
- the project will use modern, best practices, and industry standard technologies for web application architecture and development.
- the project will use the latest version of Next.js for the web framework.
- the project will use the latest version of shadcn for the UI components.
- the project will use the latest version of tailwind css for the UI design.
- the project will use the latest version of Auth.js for authentication.
- the project will use the latest version of Prisma for the database ORM for Auth, Roles, Permissions, and Users and prisma database connection checks.
- the project will use the latest version of zod for schema validation.


## look, feel styling 
This will follow a Single Page App design framework. 
The appliation will have a clean modern look with a reserved professional aesthetic. 
There will be a header containing  application notifications on the left, and two user controls on the right: user login, logout; dark light toggle. 
There will be a slim footer at the bottom of the scrollable main area (i.e. it can become larger within a set limit before scrolling) containing 
helpful infrmation and server, network, services settings (e.g. 'production', 'version', 'db connection verified', 'api responding', etc)
There will be a sidebar on the left with icons and names under section headings. The sidebar will be hidable. The items that 
the icons represent will be called "topics". Topics will have one or more pages associated with them, each using sharable components. 
When a topic is selected in the side navigation section, the main section will show a tabbed layout containing a tabl for each of the topic's 
pages as defined in the central navigation configuration. Every topic will have a default page loaded in the leftmost tab. The other tabs will load
their content on being selected (having their tab clicked. )
State in general will be minimized in this app, where necessary for user purposes (e.g. inter page state), Zustand will maintain it. See more
information below on state. 
The application will toggle between light and dark mode; all visible elements will be styled to be visible and aesthetically pleasing in both modes. 
The main content area under the header and right of the sidebar will have a tab component at its outermost navigation, with a default 
page in the first tab; other tabs as specified by the "topic" meta. 
The definition of topics, their associated pages, and other information is stored in a central, easily maintainable place. 
The application will make heavy use of shadcn (not shadcn-ui) components for the clean professional styling. 
Topics will correspond to page route and api route paths. 



- The App will use Prisma to communicate with the database for the purposes of Auth and RBAC but for all other functionality the app will 
use the bor-api REST API to communicate with the database and facilitate the other functionality. An exception to this is a database health check endpoint in the next.js route which
will test prisma's ability to connect to the database and will therefore connect directly as opposed to checkign database connectivity via the api.
This application will use the standard next.js routing as recommended, as pass-through/proxy endpoints which will fetch from a 1:1 endpoint:endpoint mapping to the bor-api API along with a jwt. 
* Note on user ids: within the prisma tables there is an entity called PrismaUser which has a row for each authenticated user. These users' IDs are
stored as a UUID in the PrismaUser.id field and other prisma tables reference this field in FKs. 
Elsewhere in the 'bor' database there is a User table which is responsible for application users information and providing a reference for 
all other user-related information in other tables (e.g. which User.id modified a record in another table; OR what application access does a User have). 
This small amount of complexity is for the purpose of having separation of application logic from the currently implemented Auth framework (Prisma). There 
are more implementation details for this arrangement throughout the various services/containers used in the bor system. 

- State will be managed with a combination of React context and Zustand. React context will be used for high level application state and RBAC, 
with Zustand implementing storage when necessary for business rules and user experience. State in general will be minimized and if necessary 
stored in localstorage or cookies. 

## developer details
You are a senior, experiences full stack system architect, designer and developer with years of production code in the above listed technologies. 
You have experience in data-centric environments and are very capable with relational database implementations and usage including normalized database design and query optimization. 
You follow industry best practices. 
You take price in the quality of your work. 
You are technically competent but prefer simple implementations. 
You carefully consider tradeoffs to be made during design decisions. 

## application (not system) architecture
The application will be a single page browser application with a backend api.
The application will use Next.js for the web framework for pages and api endpoints however the endpoints will pass-through/proxy to the bor-api project endponits where the actual logic resides. There will be a 1:1 mapping of endpoints between the two projects.
The shadcn framework will be used for the UI components in conjunction with tailwind css.
The application will be responsive and mobile friendly.
The system will be designed for simplicity but with the experience of a senior designer and developer using best practices.
The system will be deployed using standard Docker techniques, but not using Docker Compose which is not supported in some target environments.
The system will be deployed using a CI/CD pipeline to a target environment.

# Authentication System Architecture




The BOR application implements a robust authentication system with the following components:

1. **Auth.js (NextAuth) Configuration**
   - Located at `/src/auth.ts`
   - Uses Google provider for OAuth authentication
   - PrismaAdapter is used for auth. 
   - Custom JWT with extended fields for roles, permissions, and approval status
   - Session strategy is JWT-based with 30-day expiration

2. **Client-Side Authentication**
   - Custom `useAuth()` hook that provides:
     - Authentication status (`isAuthenticated`, `isLoading`)
     - User information
     - Permission checking (`hasPermission()`)
     - Role checking (`hasRole()`)
     - Approval status checking (`isApproved`)

3. **Server-Side Authentication**
   - Auth utils (`lib/auth-utils.ts`) with functions for checking:
     - `hasPermission()`
     - `hasRole()`
     - `isAuthenticated()`
     - `isApproved()`

4. **Protection Mechanisms**
   - Middleware (`middleware.ts`) for protecting routes at the application level
   - API middleware (`lib/api-middleware.ts`) with `protectRoute()` HOF for API routes
   - `PermissionGate` component for conditional UI rendering based on permissions/roles

5. **Authentication Flow**
   - Sign-in page available at `/auth/signin`
   - Google OAuth implemented
   - Custom error and unauthorized pages
   - Sign-out functionality in the Navigation component

6. **Database Schema**
   - Prisma schema includes models for:
     - PrismaUser, Account, Session, VerificationToken (standard Auth.js models)
     - Role, Permission, UserRole, RolePermission (for RBAC)
     - AuthActivity (for logging authentication events)

7. **Integration in UI**
   - NextAuthProvider wraps the application in the root layout
   - Navigation uses authentication state to display different UI elements
   - Protected routes in both pages and API endpoints


## RBAC coordination with API

The BOR system implements an integrated Role-Based Access Control (RBAC) mechanism that coordinates between the bor-app (Next.js frontend) and bor-api (backend API) using JWT tokens. This approach ensures consistent authorization across the entire application stack.

## Roles and Permissions

### Prisma Schema Implementation

The RBAC system is implemented using the following Prisma models in the `bor` database:

```prisma
model PrismaUser {
  id            String    @id @default(cuid())
  UserId        String    @unique  **this is the bor database (bor.User.)
  email         String    @unique
  name          String?
  image         String?
  isApproved    Boolean   @default(false)
  accounts      Account[]
  sessions      Session[]
  userRoles     UserRole[]
  authActivity  AuthActivity[]
}

model Role {
  id            String    @id @default(cuid())
  name          String    @unique
  description   String?
  userRoles     UserRole[]
  rolePermissions RolePermission[]
}

model Permission {
  id            String    @id @default(cuid())
  name          String    @unique
  description   String?
  rolePermissions RolePermission[]
}

model UserRole {
  id            String    @id @default(cuid())
  userId        String
  roleId        String
  user          PrismaUser @relation(fields: [userId], references: [id])
  role          Role      @relation(fields: [roleId], references: [id])
  @@unique([userId, roleId])
}

model RolePermission {
  id            String    @id @default(cuid())
  roleId        String
  permissionId  String
  role          Role      @relation(fields: [roleId], references: [id])
  permission    Permission @relation(fields: [permissionId], references: [id])
  @@unique([roleId, permissionId])
}
```


### Access Control Implementation

1. **Page Protection**
   - Pages are protected using Next.js middleware (`middleware.ts`)
   - Routes are checked against user permissions before rendering
   - Unauthorized access redirects to `/auth/unauthorized`

2. **Component Protection**
   - Components use the `PermissionGate` wrapper:
   ```tsx
   <PermissionGate 
     requiredPermissions={['view_portfolio']}
     fallback={<UnauthorizedMessage />}
   >
     <PortfolioComponent />
   </PermissionGate>
   ```

3. **API Endpoint Protection**
   - API routes use the `protectRoute` higher-order function:
   ```typescript
   export default protectRoute(
     ['manage_users'],
     async function handler(req: NextApiRequest, res: NextApiResponse) {
       // Protected route logic
     }
   );
   ```

4. **Permission Checking**
   - Client-side: `useAuth()` hook provides permission checking
   - Server-side: `hasPermission()` utility function
   - Both use the JWT token's permission claims

### Default Roles and Permissions

The system includes these default roles:
- `admin`: Full system access
- `user`: Basic user access
- `viewer`: Read-only access
- `data_manager`: ETL and data management access

Common permissions include:
- `view_*`: Read access to specific resources
- `manage_*`: Full access to specific resources
- `execute_*`: Ability to run specific operations
- `approve_*`: Ability to approve specific actions

### Permission Inheritance

- Roles can have multiple permissions
- Users can have multiple roles
- Permissions are additive (most permissive wins)
- System checks all user roles for required permissions

This implementation provides granular control over user access while maintaining simplicity in the permission model.

## testing 
tbd 

## deployment 
The project will be deployed using standard Docker techniques, but not using Docker Compose which is not supported in some target environments.
The project will be deployed using a CI/CD pipeline to a target environment.
 # to ensure prod has all of the .env files, some of which are .gitignored 
scp bor-db/.env* robmenning.com@xenodochial-turing.108-175-7-118.plesk.page:/var/www/vhosts/robmenning.com/bor/bor-db/
scp bor-api/.env* robmenning.com@xenodochial-turing.108-175-7-118.plesk.page:/var/www/vhosts/robmenning.com/bor/bor-api/
scp bor-app/.env* robmenning.com@xenodochial-turing.108-175-7-118.plesk.page:/var/www/vhosts/robmenning.com/bor/bor-app/

docker exec -it bor-db mysql -u borAllAdmin -pkBu9pjz2vi bor -e "insert into UserRole (id, userId, roleId) select concat(r.id, ':', pu.id) as id, pu.id as userId, r.id as roleId from PrismaUser pu join Role r on 1=1 where pu.email = 'robmenning@gmail.com';"
-or-
docker exec -it bor-db mysql -u borAllSvc -pu67nyNgomZ but -e "insert into UserRole (id, userId, roleId) select concat(r.id, ':', pu.id) as id, pu.id as userId, r.id as roleId from PrismaUser pu join Role r on 1=1 where pu.email = 'robmenning@gmail.com';"


# DEV ITERATIONS
DEV:
(npm run: 
clear && rm -rf .next node_modules/.cache node_modules/.vite && npm install && npm run dev
)

1. clear; docker stop bor-app && docker rm bor-app && docker rmi bor-app:dev && ./scripts/docker-run-dev.sh
2. git push origin <branch>

PROD:
3. logged in as robmenning.com@xenodochial-turing...
3.a. cd ~/bor/bor-app
3.b. git pull origin <branch>
4. logged in as root@xenodochial-turing
4.a. cd /var/www/vhosts/robmenning.com/bor/bor-app
4.b. clear; docker stop bor-app; docker rm bor-app; ./scripts/docker-run-prod.sh; docker ps


## running and monitoring in different environments:

The BOR application includes a set of scripts to facilitate development, testing, deployment, and monitoring across different environments. These scripts are located in the `script` directory:

### Development Scripts


### Docker Container Scripts


### Deployment Scripts


### Usage Instructions


## apache and nginx configuration
DID NOT USE THIS...
## apache and nginx configuration
if ($http_origin ~* (.*\.robmenning.com)) {
	set $cors "true";
}

location ~* /(sqllearn)/ {
	if ($cors = "true") {
		add_header 'Access-Control-Allow-Origin' "$http_origin";
		add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PUT';
		add_header 'Access-Control-Allow-Credentials' 'true';
		add_header 'Access-Control-Allow-Headers' 'User-Agent,Keep-Alive,Content-Type';
	}

	proxy_pass http://108.175.7.118:3004;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection 'upgrade';
	proxy_set_header Host $host;
	proxy_cache_bypass $http_upgrade;
}

... USED THIS INSTEAD IN THE APACHE CONFIGURATION (BOTH THE HTTP AND HTTPS CONFIGURATIONS):
<IfModule mod_proxy.c>
	ProxyRequests Off
	ProxyPreserveHost On

	<Location />
		ProxyPass http://localhost:4600/
		ProxyPassReverse http://localhost:4600/
	</Location>
</IfModule>
... LATER UPDATED TO THIS FOR API COMMUNICATION:
<IfModule mod_proxy.c>
    ProxyRequests Off
    ProxyPreserveHost On
    
    # Proxy API requests to bor-api
    <Location /api/>
        ProxyPass http://localhost:4610/
        ProxyPassReverse http://localhost:4610/
    </Location>
    
    # Proxy all other requests to bor-app
    <Location />
        ProxyPass http://localhost:4600/
        ProxyPassReverse http://localhost:4600/
    </Location>
</IfModule>




### Feature Implementation (ongoing)

1. **User administration**:
   - User management
   - Role-based access control
   - User preferences

2. **Investment management**:
   - Position management
   - Transaction management
   - Allocation and reporting

3. **Data management**:
   - ETL jobs
   - Processing jobs
   - Data health and validation
   - System monitoring
