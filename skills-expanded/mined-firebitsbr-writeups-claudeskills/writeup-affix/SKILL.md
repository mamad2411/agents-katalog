<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-affix
description: CTF writeups and security challenges by affix.
---

# Writeups by affix

Source repository: `/repos/affix`

## Repository Index

- pentest-reporter/DOCKER.md
- pentest-reporter/README.md
- pentest-reporter/TESTING.md
- pentest-reporter/frontend/README_TESTING.md
- pentest-reporter/backend/tests/README.md

## Writeup Content


### File: pentest-reporter/README.md

# Pentest Report Generator Web Application

A Flask + Angular web application for generating professional pentest reports from markdown files. Based on the note-to-report.py script logic.

## Features

- Upload multiple markdown files
- Configurable report settings:
  - Title and subtitle
  - Author information (name, position, email)
  - Title page colors (background, text, rule)
  - Logo (file upload or remote URL)
- Automatic CVSS vector parsing and severity table generation
- PDF generation using Pandoc with the Eisvogel template
- Modern, responsive Angular frontend

## Prerequisites

### Backend Requirements
- Python 3.8+
- Pandoc (with LaTeX support)
- Eisvogel template for Pandoc

### Frontend Requirements
- Node.js 18+ and npm

### Installing Pandoc and Eisvogel Template

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra
```

#### macOS:
```bash
brew install pandoc
brew install basictex
```

#### Install Eisvogel Template:
```bash
mkdir -p ~/.pandoc/templates
cd ~/.pandoc/templates
wget https://raw.githubusercontent.com/enhuiz/eisvogel/refs/heads/master/eisvogel.tex
```

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install npm dependencies:
```bash
npm install
```

3. Start the Angular development server:
```bash
npm start
```

The frontend will start on `http://localhost:4200`

## Usage

1. Open your browser and navigate to `http://localhost:4200`

2. Upload one or more markdown files (.md)

3. Configure your report settings:
   - Enter a title and subtitle
   - Add author information
   - Customize title page colors (use hex color picker or enter hex codes)
   - Add a logo (upload a file or provide a URL)

4. Click "Generate Report"

5. The PDF will be automatically downloaded when ready

## Markdown File Format

Your markdown files can include YAML frontmatter with CVSS vectors:

```markdown
---
cvss: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
severity: [High]
---

## Vulnerability Title

Description of the vulnerability...

### Impact

Impact details...

### Remediation

Remediation steps...
```

If a CVSS vector is provided, the application will automatically generate a severity table in the report.

## API Endpoints

### Health Check
```
GET /api/health
```

Returns the health status of the API.

### Generate Report
```
POST /api/generate-report
```

**Form Data:**
- `files`: Multiple markdown files
- `config`: JSON configuration object
- `logo`: (Optional) Logo image file

**Config Object:**
```json
{
  "title": "Report Title",
  "subtitle": "Report Subtitle",
  "author": ["Name", "Position", "Email"],
  "titlepage_color": "241C3A",
  "titlepage_text_color": "FFFAFA",
  "titlepage_rule_color": "FFFAFA",
  "logo_url": "https://example.com/logo.png"
}
```

**Response:**
- Content-Type: `application/pdf`
- Binary PDF file

## Project Structure

```
.
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/            # Temporary file uploads (created at runtime)
│   └── temp/               # Temporary processing directory (created at runtime)
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts      # Main component
│   │   │   ├── app.component.html    # Component template
│   │   │   ├── app.component.css     # Component styles
│   │   │   ├── app.module.ts         # App module
│   │   │   └── report.service.ts     # API service
│   │   ├── index.html      # Main HTML file
│   │   ├── main.ts         # Bootstrap file
│   │   └── styles.css      # Global styles
│   ├── angular.json        # Angular configuration
│   ├── package.json        # npm dependencies
│   └── tsconfig.json       # TypeScript configuration
│
└── README.md               # This file
```

## Development

### Backend Development

The Flask app runs in debug mode by default. Any changes to `app.py` will automatically reload the server.

### Frontend Development

The Angular development server supports hot module replacement. Any changes to the TypeScript, HTML, or CSS files will automatically refresh the browser.

## Production Deployment

### Backend

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

Build the Angular app for production:

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`. Serve them with a web server like Nginx.

### CORS Configuration

For production, update the CORS settings in `backend/app.py` to only allow your frontend domain:

```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

## Troubleshooting

### Pandoc Not Found
Ensure Pandoc is installed and in your PATH. Test with:
```bash
pandoc --version
```

### Eisvogel Template Not Found
Verify the template is in the correct location:
```bash
ls ~/.pandoc/templates/eisvogel.tex
```

### LaTeX Errors
Make sure you have a complete LaTeX distribution installed. The Eisvogel template requires several LaTeX packages.

### CORS Errors
If you see CORS errors in the browser console, ensure the Flask backend is running and Flask-CORS is properly configured.

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.



### File: pentest-reporter/backend/tests/README.md

# Backend Unit Tests

Comprehensive unit tests for the report generator backend.

## Test Coverage

### Utils Module Tests
- **test_utils_security.py**
  - Filename sanitization
  - Path traversal validation
  - URL safety checks (SSRF prevention)
  - Private IP detection
  - Protocol validation

- **test_utils_file_validator.py**
  - File extension validation (markdown and images)
  - Magic byte validation
  - File content validation (UTF-8 and images)

### Processors Module Tests
- **test_processors_cvss.py**
  - CVSS vector string parsing
  - LaTeX table generation
  - Severity calculation
  - YAML frontmatter processing

- **test_processors_markdown.py**
  - YAML frontmatter extraction
  - Content cleaning and sanitization
  - Script/iframe tag removal
  - File processing workflow

### Handlers Module Tests
- **test_handlers_file_upload.py**
  - Logo file upload validation
  - Logo URL download and validation
  - Markdown file upload validation
  - Security checks (path traversal, SSRF, file size)

### Generators Module Tests
- **test_generators_report.py**
  - Title page generation
  - PDF report generation
  - Pandoc integration
  - Configuration handling

## Running Tests

### Install Test Dependencies
```bash
pip install -r tests/requirements-test.txt
```

### Run All Tests
```bash
# Using pytest
pytest

# With coverage report
pytest --cov=. --cov-report=html

# Verbose output
pytest -v
```

### Run Specific Test Files
```bash
pytest tests/test_utils_security.py
pytest tests/test_processors_cvss.py
```

### Run Specific Test Classes
```bash
pytest tests/test_utils_security.py::TestIsSafeUrl
```

### Run Specific Test Methods
```bash
pytest tests/test_utils_security.py::TestIsSafeUrl::test_localhost_rejected
```

## Test Organization

Tests follow the same structure as the source code:
```
backend/
├── utils/
│   ├── security.py
│   └── file_validator.py
├── processors/
│   ├── cvss_processor.py
│   └── markdown_processor.py
├── handlers/
│   └── file_upload.py
├── generators/
│   └── report_generator.py
└── tests/
    ├── test_utils_security.py
    ├── test_utils_file_validator.py
    ├── test_processors_cvss.py
    ├── test_processors_markdown.py
    ├── test_handlers_file_upload.py
    └── test_generators_report.py
```

## Coverage Goals

- **Target Coverage**: 80%+
- **Critical Modules**: 90%+ (security, file validation)
- **Report Location**: `htmlcov/index.html` after running with `--cov-report=html`

## Continuous Integration

Tests should be run automatically on:
- Pre-commit hooks
- Pull request creation
- Merge to main branch

## Writing New Tests

When adding new functionality:
1. Write tests first (TDD approach)
2. Follow existing test patterns
3. Use descriptive test names
4. Test edge cases and error conditions
5. Mock external dependencies (requests, pypandoc)



### File: pentest-reporter/DOCKER.md

# Docker Deployment Guide

This guide explains how to build and run the pentest Reporter application using Docker with nginx and WSGI (Gunicorn).

## Architecture

The Docker setup includes:
- **nginx**: Serves the Angular frontend and proxies API requests
- **Gunicorn (WSGI)**: Runs the Flask backend application
- **Supervisor**: Manages both nginx and Gunicorn processes
- **Multi-stage build**: Optimizes the final image size

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (optional, for easier deployment)

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:8080`

### Using Docker CLI

```bash
# Build the Docker image
docker build -t pentest-reporter:latest .

# Run the container
docker run -d \
  --name pentest-reporter \
  -p 8080:80 \
  pentest-reporter:latest

# View logs
docker logs -f pentest-reporter

# Stop the container
docker stop pentest-reporter
docker rm pentest-reporter
```

## Configuration

### Port Mapping

By default, the application runs on port 8080. To change this:

**Docker Compose:**
Edit `docker-compose.yml` and change the port mapping:
```yaml
ports:
  - "3000:80"  # Map to port 3000 instead
```

**Docker CLI:**
```bash
docker run -d -p 3000:80 pentest-reporter:latest
```

### Environment Variables

You can set environment variables in `docker-compose.yml`:
```yaml
environment:
  - FLASK_ENV=production
  - MAX_CONTENT_LENGTH=52428800  # 50MB in bytes
```

### Persistent Storage (Optional)

To persist uploads and temp files, uncomment the volumes section in `docker-compose.yml`:
```yaml
volumes:
  - ./backend/uploads:/app/backend/uploads
  - ./backend/temp:/app/backend/temp
```

## Health Check

The container includes a health check that monitors the Flask API:
```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' pentest-reporter
```

The health endpoint is available at `http://localhost:8080/api/health`

## Production Considerations

### Resource Limits

Add resource limits in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

### HTTPS/SSL

To add HTTPS support:
1. Mount SSL certificates:
   ```yaml
   volumes:
     - ./certs:/etc/nginx/certs:ro
   ```

2. Update `nginx.conf` to include SSL configuration:
   ```nginx
   server {
       listen 443 ssl;
       ssl_certificate /etc/nginx/certs/cert.pem;
       ssl_certificate_key /etc/nginx/certs/key.pem;
       # ... rest of configuration
   }
   ```

### Scaling

To run multiple backend workers, modify the Gunicorn configuration in the Dockerfile:
```bash
command=gunicorn --bind 127.0.0.1:5000 --workers 8 --timeout 300 wsgi:app
```

## Troubleshooting

### Check Application Logs

```bash
# All logs
docker-compose logs -f

# Backend logs only
docker exec pentest-reporter tail -f /var/log/gunicorn.out.log

# nginx logs
docker exec pentest-reporter tail -f /var/log/nginx/access.log
docker exec pentest-reporter tail -f /var/log/nginx/error.log
```

### Container Won't Start

```bash
# Check container status
docker ps -a

# Inspect container
docker inspect pentest-reporter

# Check supervisor status
docker exec pentest-reporter supervisorctl status
```

### PDF Generation Issues

The container includes all necessary LaTeX packages. If you encounter issues:
```bash
# Enter the container
docker exec -it pentest-reporter bash

# Test pandoc
pandoc --version

# Check LaTeX installation
which xelatex
```

### Memory Issues

PDF generation is memory-intensive. Increase Docker's memory allocation:
- Docker Desktop: Preferences → Resources → Memory (set to at least 4GB)
- Docker CLI: Use `--memory` flag when running

## Updating the Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Development Mode

For development with hot-reload, use the original `start-backend.sh` and `start-frontend.sh` scripts instead of Docker.

## Support

For issues specific to the Docker setup, check:
- Supervisor logs: `/var/log/supervisor/supervisord.log`
- Gunicorn logs: `/var/log/gunicorn.out.log` and `/var/log/gunicorn.err.log`
- nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`



### File: pentest-reporter/TESTING.md

# Testing Documentation

Comprehensive unit tests for the JIRA Reporter Application.

## Overview

The application has extensive test coverage for both backend and frontend components, focusing on security, functionality, and edge cases.

## Backend Tests (Python)

### Location
`/backend/tests/`

### Test Files
1. **test_utils_security.py** - Security utility functions
   - Filename sanitization
   - Path traversal validation
   - SSRF prevention (URL validation, private IP detection)
   - Protocol validation

2. **test_utils_file_validator.py** - File validation
   - Extension validation (markdown, images)
   - Magic byte validation
   - UTF-8 content validation

3. **test_processors_cvss.py** - CVSS processing
   - Vector string parsing
   - LaTeX table generation
   - Severity calculation
   - YAML frontmatter processing

4. **test_processors_markdown.py** - Markdown processing
   - YAML frontmatter extraction
   - Content cleaning (script/iframe removal)
   - File processing workflow
   - Security sanitization

5. **test_handlers_file_upload.py** - File upload handlers
   - Logo file validation
   - Logo URL download (with SSRF protection)
   - Markdown file validation
   - Security checks (path traversal, file size)

6. **test_generators_report.py** - Report generation
   - Title page generation
   - PDF generation workflow
   - Pandoc integration
   - Configuration handling

### Running Backend Tests

```bash
cd backend

# Install test dependencies
pip install -r tests/requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_utils_security.py

# Run specific test
pytest tests/test_utils_security.py::TestIsSafeUrl::test_localhost_rejected
```

### Backend Test Statistics
- **Total Test Files**: 6
- **Test Classes**: 20+
- **Individual Tests**: 100+
- **Coverage Target**: 80%+

## Frontend Tests (TypeScript/Jasmine)

### Location
`/frontend/src/app/`

### Test Files
1. **file-upload.component.spec.ts** - File upload component
   - File selection validation
   - Type checking (.md, .markdown)
   - Size validation (10MB limit)
   - Suspicious filename detection
   - Path traversal prevention
   - File removal functionality

2. **logo-upload.component.spec.ts** - Logo upload component
   - Image type validation
   - Size validation (5MB limit)
   - URL handling
   - File removal

3. **toast.component.spec.ts** - Toast notification component
   - Message display (success/error/warning/info)
   - Auto-dismiss functionality
   - Multiple toast handling
   - Icon display

4. **cvss-info.component.spec.ts** - CVSS info component
   - Toggle functionality
   - Content visibility
   - Template rendering

5. **toast.service.spec.ts** - Toast service
   - Toast creation
   - ID generation
   - Observable streams
   - Removal functionality

### Running Frontend Tests

```bash
cd frontend

# Run all tests
ng test

# Run once (CI mode)
ng test --watch=false

# Run with coverage
ng test --code-coverage

# View coverage report
open coverage/reporter-app/index.html
```

### Frontend Test Statistics
- **Total Test Files**: 5
- **Test Suites**: 15+
- **Individual Tests**: 80+
- **Coverage Target**: 80%+

## Test Coverage

### Security Tests
✅ Path traversal prevention
✅ SSRF attack prevention
✅ Command injection detection
✅ File type validation
✅ File size limits
✅ Malicious content removal (script/iframe tags)
✅ Private IP blocking
✅ Protocol validation

### Functionality Tests
✅ File upload/download
✅ CVSS vector processing
✅ PDF generation
✅ Markdown processing
✅ Title page generation
✅ Toast notifications
✅ Component interactions

### Edge Case Tests
✅ Empty files
✅ Oversized files
✅ Invalid file types
✅ Malformed inputs
✅ Multiple simultaneous operations
✅ Null/undefined handling

## Continuous Integration

### Recommended CI Pipeline

```yaml
# Example GitHub Actions workflow
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r tests/requirements-test.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          ng test --watch=false --code-coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Test Execution Time

- **Backend Tests**: ~5-10 seconds
- **Frontend Tests**: ~10-15 seconds
- **Total**: ~15-25 seconds

## Key Testing Principles

1. **Test-Driven Development (TDD)**: Write tests before implementation
2. **Security First**: All security features have comprehensive tests
3. **Edge Cases**: Test boundary conditions and error states
4. **Mock External Dependencies**: Use mocks for HTTP requests, file I/O
5. **Descriptive Names**: Test names clearly describe what they test
6. **Isolation**: Each test is independent and can run in any order

## Maintenance

- Update tests when adding new features
- Maintain >80% code coverage
- Review test failures in CI/CD pipeline
- Refactor tests alongside code refactoring
- Keep test dependencies up to date

## Documentation

- **Backend**: `/backend/tests/README.md`
- **Frontend**: `/frontend/README_TESTING.md`

## Quick Start

```bash
# Backend
cd backend && pip install -r tests/requirements-test.txt && pytest

# Frontend
cd frontend && npm install && ng test --watch=false
```



### File: pentest-reporter/frontend/README_TESTING.md

# Frontend Unit Tests

Comprehensive unit tests for the Angular frontend components and services.

## Test Coverage

### Component Tests
- **file-upload.component.spec.ts**
  - File selection and validation
  - Markdown file type checking
  - File size validation (10MB limit)
  - Empty file detection
  - Maximum file count (50 files)
  - Suspicious filename detection
  - Path traversal prevention
  - File removal functionality

- **logo-upload.component.spec.ts**
  - Logo file upload validation
  - Image type checking (PNG, JPEG, SVG, etc.)
  - File size validation (5MB limit)
  - Logo URL handling
  - Logo removal functionality

- **toast.component.spec.ts**
  - Toast message display
  - Success/error/warning/info types
  - Toast removal
  - Auto-dismiss functionality
  - Multiple toast handling
  - Icon display for different types

- **cvss-info.component.spec.ts**
  - Toggle functionality
  - Details visibility
  - Template content rendering

### Service Tests
- **toast.service.spec.ts**
  - Toast creation methods
  - Unique ID generation
  - Toast removal
  - Observable stream handling
  - Multiple toast management

## Running Tests

### Run All Tests
```bash
# Using Angular CLI
ng test

# Run once (CI mode)
ng test --watch=false

# With code coverage
ng test --code-coverage
```

### Run Specific Test Files
```bash
ng test --include='**/file-upload.component.spec.ts'
ng test --include='**/toast.service.spec.ts'
```

### View Coverage Report
After running tests with coverage:
```bash
# Coverage report is in: coverage/reporter-app/index.html
open coverage/reporter-app/index.html
```

## Test Configuration

Tests use Jasmine and Karma configured in:
- `karma.conf.js` - Test runner configuration
- `tsconfig.spec.json` - TypeScript configuration for tests

## Test Patterns

### Component Testing
```typescript
describe('ComponentName', () => {
  let component: ComponentName;
  let fixture: ComponentFixture<ComponentName>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComponentName],
      providers: [...]
    }).compileComponents();

    fixture = TestBed.createComponent(ComponentName);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

### Service Testing
```typescript
describe('ServiceName', () => {
  let service: ServiceName;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ServiceName]
    });
    service = TestBed.inject(ServiceName);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
```

### Mocking Dependencies
```typescript
const mockService = jasmine.createSpyObj('ServiceName', ['method1', 'method2']);

await TestBed.configureTestingModule({
  providers: [
    { provide: ServiceName, useValue: mockService }
  ]
}).compileComponents();
```

## Coverage Goals

- **Target Coverage**: 80%+
- **Components**: 85%+ (UI components with user interactions)
- **Services**: 90%+ (Core business logic)

## Key Test Scenarios

### Security Testing
- Path traversal attempts
- Command injection patterns
- File type validation
- File size limits
- Suspicious filename detection

### User Interaction Testing
- File upload/removal
- Form input validation
- Button clicks
- Toggle functionality
- Toast notifications

### Edge Cases
- Empty inputs
- Invalid file types
- Oversized files
- Multiple simultaneous actions
- Null/undefined handling

## Continuous Integration

Tests run automatically on:
- `ng test` during development
- Pre-commit hooks (if configured)
- CI/CD pipeline builds

## Writing New Tests

When adding new components:
1. Create `.spec.ts` file alongside component
2. Follow existing test patterns
3. Test all public methods
4. Test user interactions
5. Test error conditions
6. Test accessibility features

## Debugging Tests

```bash
# Run tests in Chrome for debugging
ng test --browsers=Chrome

# Run tests in headless mode
ng test --browsers=ChromeHeadless

# Run tests with source maps
ng test --source-map
```

## Common Issues

### Tests Timing Out
- Increase timeout in `karma.conf.js`
- Use `done()` callback for async tests
- Ensure observables complete

### Component Not Found
- Check imports in test file
- Verify component is standalone
- Check TestBed configuration

### Spy Not Called
- Ensure `fixture.detectChanges()` is called
- Check event binding syntax
- Verify spy is on correct object

