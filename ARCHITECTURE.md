"""Architecture and Design Decisions.

This document outlines the architectural choices, design patterns, and technical decisions
made in the Task Management API project.
"""

# Architecture and Design Decisions

## Overview

The Task Management API is built using a layered architecture pattern with clear separation of concerns.
This design ensures scalability, maintainability, and testability.

## Architectural Layers

### 1. Presentation Layer (API Routes)
- **Location**: `app/api/routes/`
- **Responsibility**: Handle HTTP requests and responses
- **Components**:
  - `auth.py`: Authentication endpoints (register, login, refresh)
  - `users.py`: User management endpoints
  - `projects.py`: Project management endpoints
  - `tasks.py`: Task management endpoints

**Design Decision**: Using FastAPI's router system for modularity and automatic OpenAPI documentation.

### 2. Business Logic Layer (Services)
- **Location**: `app/services/`
- **Responsibility**: Implement core business logic
- **Pattern**: Service Layer Pattern

**Design Decision**: Separates business rules from HTTP concerns, enabling reuse and easier testing.

### 3. Data Access Layer (Models & Repository)
- **Location**: `app/models/`
- **Responsibility**: Database interactions using SQLAlchemy ORM
- **Models**:
  - `User`: User accounts with roles
  - `Project`: Project containers
  - `Task`: Individual tasks within projects

**Design Decision**: Using SQLAlchemy ORM for type safety and SQL injection prevention.

### 4. Infrastructure Layer
- **Location**: `app/db/`, `app/config/`, `app/core/`
- **Responsibility**: Cross-cutting concerns
- **Components**:
  - Database connections
  - Configuration management
  - Security and authentication
  - Dependency injection

## Key Design Patterns

### Dependency Injection
**Location**: `app/core/dependencies.py`

Use FastAPI's dependency injection system for:
- Database session management
- Current user authentication
- Authorization checks

**Benefits**:
- Easy testing with mock dependencies
- Clear function dependencies
- Reduced coupling

```python
@router.get("/me")
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user
```

### Repository Pattern
**Implementation**: SQLAlchemy query builders

**Benefits**:
- Abstraction of data access logic
- Easy switching of data sources
- Testable with mocks

### Service Layer Pattern
**Location**: `app/services/`

**Responsibilities**:
- Business logic
- Data validation
- Orchestration of operations

### Security Decisions

#### Password Hashing
- **Algorithm**: bcrypt (via passlib)
- **Configuration**: Default salt rounds
- **Reason**: Industry-standard, resistant to modern attacks

#### JWT Tokens
- **Type**: HS256 (HMAC SHA-256)
- **Access Token Expiry**: 15 minutes (configurable)
- **Refresh Token Expiry**: 7 days (configurable)
- **Reason**: Stateless authentication, scalable

#### Token Structure
```json
{
  "sub": "user_id",
  "role": "USER",
  "exp": 1234567890,
  "iat": 1234566890
}
```

## Database Design

### Schema

#### Users Table
- UUID primary key
- Email with unique constraint
- Hashed password (bcrypt)
- Role-based authorization (ADMIN, MANAGER, USER)
- Soft delete support (is_active flag)

#### Projects Table
- UUID primary key
- Foreign key to owner (Users)
- Timestamps for audit trail
- Indexed by owner_id for efficient queries

#### Tasks Table
- UUID primary key
- Foreign keys to Project and Users
- Status and Priority enums
- Indexed for common queries (project_id, status, assigned_to)

### Indexing Strategy
```sql
-- Users
INDEX idx_email_active ON users(email, is_active);
INDEX idx_role ON users(role);

-- Tasks
INDEX idx_project_status ON tasks(project_id, status);
INDEX idx_assigned_to ON tasks(assigned_to);
INDEX idx_due_date ON tasks(due_date);
```

## Caching Strategy

### Redis Usage
- **Session cache**: User sessions (TTL: 24 hours)
- **Role cache**: User roles (TTL: 1 hour)
- **Query cache**: Frequently accessed data (TTL: 5 minutes)

### Cache Invalidation
- **Time-based**: Automatic expiry
- **Event-based**: On data mutations (updates, deletes)

## Error Handling

### Custom Exceptions
**Location**: `app/core/exceptions.py`

```python
class CredentialsException(HTTPException):
    status_code = 401
    
class NotFoundException(HTTPException):
    status_code = 404
    
class ForbiddenException(HTTPException):
    status_code = 403
```

### Error Response Format
```json
{
  "detail": "User not found",
  "error_code": "NOT_FOUND"
}
```

## Configuration Management

### Environment-Based Configuration
**Location**: `app/config.py`

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    DEBUG: bool
```

### Environment Profiles
- **Development**: Debug enabled, local services
- **Staging**: Debug disabled, remote services
- **Production**: All security features enabled

## Testing Strategy

### Unit Tests
- **Location**: `tests/unit/`
- **Focus**: Individual functions and components
- **Tools**: pytest, faker

### Integration Tests
- **Location**: `tests/integration/`
- **Focus**: Component interactions
- **Database**: Test database (SQLite or separate Postgres)

### Test Coverage Target
- Overall: >80%
- Critical paths: 100%
- Business logic: >90%

## API Design

### RESTful Conventions
```
POST   /api/v1/tasks           # Create
GET    /api/v1/tasks           # List
GET    /api/v1/tasks/{id}      # Read
PATCH  /api/v1/tasks/{id}      # Update
DELETE /api/v1/tasks/{id}      # Delete
```

### Response Format
```json
{
  "id": "uuid",
  "title": "string",
  "status": "OPEN",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Pagination
- **Default limit**: 20
- **Max limit**: 100
- **Query parameters**: `skip` and `limit`

## Scalability Considerations

### Horizontal Scaling
- Stateless API instances
- Load balancer for distribution
- Shared PostgreSQL database
- Redis for distributed caching

### Database Scaling
- Connection pooling (SQLAlchemy)
- Query optimization with indexes
- Prepared statements (ORM-level)
- Replication ready (with Postgres)

### Performance Optimization
1. **Query Optimization**
   - Eager loading (joinedload)
   - Select only needed columns
   - Use indexes for filtering

2. **Caching**
   - Redis for session/role caching
   - HTTP cache headers
   - ETag support

3. **Async Operations**
   - FastAPI async support
   - Non-blocking I/O
   - Background tasks (optional)

## Security Architecture

### Authentication Flow
```
1. User registers → Credentials stored (hashed)
2. User logs in → JWT tokens generated
3. Client sends token in Authorization header
4. API validates token, extracts user ID
5. Role-based access control applied
```

### RBAC Implementation
```python
@router.delete("/items/{item_id}")
async def delete_item(
    item_id: UUID,
    current_user: User = Depends(get_current_admin_user),
):
    # Only admins can delete
    ...
```

### CORS Policy
- Configurable allowed origins
- Credentials support
- Allowed methods: GET, POST, PUT, PATCH, DELETE
- Dynamic based on environment

## Deployment Architecture

### Docker Containerization
- Single Dockerfile for production
- Multi-stage builds (optional)
- Health checks included
- Non-root user for security

### Docker Compose
- Development: All services with hot-reload
- Production: Optimized images, volume mounts

### CI/CD Pipeline
- Tests on every push
- Code quality checks
- Security scanning
- Automated deployment

## Monitoring and Logging

### Logging Strategy
- **Tool**: Python logging + structlog
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Format**: JSON for structured parsing

### Metrics to Track
- Request/response times
- Error rates
- Database query performance
- Cache hit rates

## Future Improvements

1. **Event Sourcing**: For audit trails
2. **Message Queue**: For async tasks
3. **Microservices**: Separate services by domain
4. **GraphQL**: Alternative to REST API
5. **Real-time Updates**: WebSocket support
6. **Advanced Analytics**: ELK stack integration

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [REST API Design](https://restfulapi.net/)
- [12 Factor App](https://12factor.net/)
