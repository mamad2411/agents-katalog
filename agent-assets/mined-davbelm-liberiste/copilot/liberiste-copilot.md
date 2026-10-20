<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# UniResource Hub - Copilot Instructions

This is a full-stack web application for centralizing learning resources for ALU students.

## Project Structure

- **Backend**: Python FastAPI with PostgreSQL database
- **Frontend**: React TypeScript with Tailwind CSS
- **Authentication**: JWT-based with bcrypt password hashing
- **File Storage**: Cloud storage integration (AWS S3 compatible)

## Key Requirements

- Follow the SRS document requirements for all features
- Implement secure authentication as per FR 1.x requirements
- Support resource upload/management as per FR 2.x requirements
- Implement search and filtering as per FR 3.x requirements
- Follow security best practices (HTTPS, password hashing, input validation)
- Ensure responsive design for web browsers
- Use proper error handling and validation

## Code Style

- Use TypeScript for frontend components
- Follow FastAPI best practices for backend APIs
- Use Pydantic models for data validation
- Implement proper database relationships using SQLAlchemy
- Write clean, documented code with proper error handling

## Database Schema

Follow the UML class diagram from the SRS:

- User (userID, email, passwordHash, firstName, lastName, accountStatus)
- Resource (resourceID, title, description, uploadDate, resourceType, filePath/url, uploaderID)
- Category (categoryID, name)
- Tag (tagID, name)
- Bookmark (bookmarkID, userID, resourceID, bookmarkDate)
