# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Go test project that validates FTP server functionality using Docker containers. The project uses `dockertest` to spin up a vsftpd FTP server, mounts test data, and verifies file listings.

## Commands

### Testing
```bash
go test -v        # Run all tests with verbose output
go test -run TestFTPServer  # Run specific test
```

### Dependencies
```bash
go mod download   # Download dependencies
go mod tidy       # Clean up and verify dependencies
```

## Architecture

The project follows a test-driven approach with these key components:

- **Docker Integration**: Uses `github.com/ory/dockertest/v3` to programmatically manage Docker containers
- **FTP Server**: Runs `fauria/vsftpd` Docker image as the FTP server for testing
- **FTP Client**: Uses `github.com/jlaffaye/ftp` for FTP client operations
- **Test Data**: The `testdata/` directory is mounted into the Docker container at `/home/vsftpd/testuser` and contains test files that should be accessible via FTP
- **Verification**: Tests connect to the FTP server and verify that `file1.txt` and `file2.txt` can be listed

## Key Implementation Notes

- The main test file is `main_test.go`
- FTP server uses credentials: username=`testuser`, password=`testpass`
- The test uses EPSV disabled mode to avoid passive mode connection issues in Docker
- The test should clean up Docker resources after completion using `defer` statements
- If listing files fails due to passive mode issues, the test falls back to checking individual file existence

## Test Structure

The test uses table-driven testing with the following test cases:
1. **FTP (plain)** - Standard unencrypted FTP connection using fauria/vsftpd
   - Ports: 21 (control), 21100-21110 (passive mode)
2. **FTPS (with TLS)** - TLS-encrypted FTP connection using phpstorm/ftps
   - Ports: 21 (control), 30010-30019 (passive mode)
   - Uses explicit FTPS (AUTH TLS)
   - `InsecureSkipVerify: true` to ignore certificate errors

## Test Case Structure

Each test case contains:
- `name`: Test case name
- `repository`, `tag`: Docker image details
- `useTLS`: Whether to use TLS
- `tlsConfig`: TLS configuration
- `envVars`: Environment variables for the container
- `dialOptions`: FTP client dial options
- `mountPath`: Path where testdata is mounted in the container
- `username`, `password`: FTP credentials
- `pasvMinPort`, `pasvMaxPort`: Passive mode port range

## Port Binding

The test automatically binds:
- FTP control port (21) to a random available port
- Passive mode ports to the specified range (fixed ports)

## CI/CD

This project uses GitHub Actions for continuous integration:

### Workflow: `.github/workflows/test.yml`
- **Triggers**: 
  - Push to any branch
  - Pull requests to any branch
- **Environment**: Ubuntu latest (includes Docker pre-installed)
- **Go Version**: 1.21
- **Actions**:
  1. Checkout code
  2. Set up Go environment
  3. Verify Docker is available (`docker --version` and `docker info`)
  4. Download dependencies (`go mod download`)
  5. Run tests with verbose output (`go test -v`)
     - Sets `DOCKER_HOST` environment variable to ensure Docker socket access

The workflow ensures all tests pass before merging changes and provides immediate feedback on code quality.

### Docker Requirements
- GitHub Actions Ubuntu runners include Docker pre-installed
- The workflow verifies Docker availability before running tests
- Tests will automatically pull required Docker images:
  - `bfren/ftps:latest` (for FTPS testing)
  - `garethflowers/ftp-server:latest` (for plain FTP testing)
- Required port ranges must be available:
  - 60000-60010 (FTPS passive mode)
  - 40000-40009 (FTP passive mode)