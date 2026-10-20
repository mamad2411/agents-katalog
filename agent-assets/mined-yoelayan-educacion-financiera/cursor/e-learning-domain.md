---
description: 
globs: 
alwaysApply: true
---
# E-Learning Platform Domain Guide

This guide covers the domain-specific aspects of the financial education e-learning platform.

## Core Domain Concepts

### Educational Structure
- **Courses**: Main learning units with structured content
- **Lessons/Modules**: Individual learning components within courses
- **Assessments**: Quizzes, tests, and evaluations
- **Progress Tracking**: Student advancement through content
- **Certificates**: Completion credentials

### User Roles & Permissions
- **Students**: Primary learners consuming content
- **Instructors**: Content creators and course managers
- **Administrators**: Platform managers with full access
- **Moderators**: Discussion and content moderators

## Application Architecture

### Courses App
**Location**: [apps/courses/](mdc:educacion_financiera/educacion_financiera/apps/courses)

Key responsibilities:
- Course creation and management
- Content organization and delivery
- Learning path definition
- Course enrollment and access control

**Core Models** (likely in [models.py](mdc:educacion_financiera/educacion_financiera/apps/courses/models.py)):
- Course: Main course entity
- Lesson/Module: Individual learning units
- Enrollment: Student-course relationships
- Progress: Learning advancement tracking

### Profiles App
**Location**: [apps/profiles/](mdc:educacion_financiera/educacion_financiera/apps/profiles)

Key responsibilities:
- Extended user profile information
- Learning preferences and settings
- Achievement and badge tracking
- Personal learning dashboard

### Discussions App
**Location**: [apps/discussions/](mdc:educacion_financiera/educacion_financiera/apps/discussions)

Key responsibilities:
- Course-specific forums
- Q&A functionality
- Peer-to-peer learning
- Instructor-student communication

### Payments & Subscriptions
**Payments**: [apps/payments/](mdc:educacion_financiera/educacion_financiera/apps/payments)
**Subscriptions**: [apps/subscriptions/](mdc:educacion_financiera/educacion_financiera/apps/subscriptions)

Key responsibilities:
- Course purchase processing
- Subscription management
- Payment gateway integration
- Revenue tracking and reporting

## Business Logic Patterns

### Enrollment Management
```python
# Example enrollment logic pattern
class EnrollmentManager:
    def enroll_student(self, student, course):
        # Check prerequisites
        # Verify payment/subscription
        # Create enrollment record
        # Initialize progress tracking
        pass
```

### Progress Tracking
- Track completion of individual lessons
- Calculate overall course progress
- Trigger completion events and certificates
- Update user achievements

### Content Access Control
- Verify enrollment status
- Check subscription validity
- Implement content drip/scheduling
- Handle premium vs. free content

## Financial Education Specifics

### Content Types
- **Video Lessons**: Primary instructional content
- **Interactive Exercises**: Practical financial calculations
- **Case Studies**: Real-world financial scenarios
- **Assessments**: Knowledge validation
- **Resources**: Downloadable materials and tools

### Learning Paths
- **Beginner**: Basic financial literacy
- **Intermediate**: Investment and planning
- **Advanced**: Complex financial strategies
- **Specialized**: Specific topics (retirement, taxes, etc.)

### Gamification Elements
- **Points**: Earned through lesson completion
- **Badges**: Achievement recognition
- **Leaderboards**: Peer comparison and motivation
- **Certificates**: Formal completion recognition

## Integration Points

### User Management
- Extends Django's built-in User model
- Custom user fields in [users/](mdc:educacion_financiera/educacion_financiera/users)
- Profile extensions in profiles app

### Authentication & Authorization
- Course access permissions
- Role-based content visibility
- Subscription-based feature access
- Social authentication integration

### Notifications & Communication
- Course announcements
- Progress notifications
- Discussion updates
- Payment confirmations

### Analytics & Reporting
- Learning analytics and insights
- Course performance metrics
- User engagement tracking
- Revenue and subscription analytics

## API Design Patterns

### RESTful Endpoints
```python
# Example API structure
/api/v1/courses/                    # Course listing
/api/v1/courses/{id}/               # Course detail
/api/v1/courses/{id}/enroll/        # Enrollment action
/api/v1/courses/{id}/progress/      # Progress tracking
/api/v1/users/{id}/enrollments/     # User enrollments
```

### Serializer Patterns
- Nested serializers for related data
- Different serialization levels (list vs. detail)
- Permission-based field inclusion
- Optimized queries with select_related

## Background Tasks

### Celery Integration
**Configuration**: [config/celery_app.py](mdc:educacion_financiera/config/celery_app.py)

Common async tasks:
- Email notifications (course updates, completions)
- Certificate generation
- Progress calculations
- Payment processing
- Data analytics and reporting

### Task Examples
```python
# Example background tasks
@shared_task
def send_course_completion_email(user_id, course_id):
    pass

@shared_task
def generate_certificate(enrollment_id):
    pass

@shared_task
def update_course_analytics():
    pass
```

## Data Models Best Practices

### Audit Fields
- created_at, updated_at timestamps
- created_by, updated_by user tracking
- Soft deletion with is_active flags

### Relationships
- Use appropriate foreign key relationships
- Consider many-to-many for flexible associations
- Implement proper cascade behaviors

### Validation
- Model-level validation for business rules
- Custom validators for domain-specific logic
- Form validation for user input
