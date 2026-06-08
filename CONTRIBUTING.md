# Contributing Guide

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/hasanhsynsahinn/task-management-api.git
   cd task-management-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

5. **Initialize database**
   ```bash
   alembic upgrade head
   ```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Adding tests
- `chore/` - Maintenance tasks

### Writing Code

1. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Maximum line length: 100 characters
   - Use double quotes for strings

2. **Format Code**
   ```bash
   black app/ tests/
   isort app/ tests/
   ```

3. **Lint Code**
   ```bash
   flake8 app/ tests/
   ```

4. **Type Check**
   ```bash
   mypy app/
   ```

5. **Security Scan**
   ```bash
   bandit -r app/
   ```

### Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run only integration tests
pytest tests/integration/ -v
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Examples:
- `feat: add user authentication`
- `fix: resolve task filtering bug`
- `docs: update API documentation`
- `test: add integration tests for tasks`
- `refactor: optimize database queries`
- `chore: update dependencies`

### Pull Request Process

1. **Before submitting PR**
   ```bash
   # Format code
   black app/ tests/
   isort app/ tests/
   
   # Run all checks
   flake8 app/ tests/
   mypy app/
   bandit -r app/
   
   # Run tests
   pytest -v
   ```

2. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Use descriptive title
   - Reference related issues
   - Describe changes clearly
   - Include screenshots if UI changes

4. **PR Requirements**
   - ✅ All tests passing
   - ✅ No linting errors
   - ✅ Type checking passes
   - ✅ Code coverage >80%
   - ✅ Documentation updated

## Code Review Guidelines

When reviewing code, check for:

1. **Functionality**
   - Does it solve the issue?
   - Are edge cases handled?
   - Are error messages clear?

2. **Code Quality**
   - Follows style guide
   - Type hints present
   - No code duplication
   - Clear variable names

3. **Testing**
   - Unit tests for functions
   - Integration tests for workflows
   - Adequate coverage

4. **Documentation**
   - Docstrings present
   - Comments explain why, not what
   - README updated if needed

5. **Security**
   - No hardcoded secrets
   - Input validation present
   - SQL injection prevention
   - Authentication checks

## Project Structure

```
task-management-api/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── core/                # Core utilities
│   ├── models/              # Database models
│   ├── api/routes/          # API endpoints
│   ├── services/            # Business logic
│   ├── db/                  # Database
│   └── utils/               # Helpers
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── conftest.py          # Pytest config
├── alembic/                 # Database migrations
├── docker/                  # Docker files
├── .github/workflows/       # CI/CD
├── README.md
├── ARCHITECTURE.md
└── requirements.txt
```

## Common Tasks

### Adding a New Feature

1. Create feature branch
2. Create models if needed (`app/models/`)
3. Create schemas (`app/schemas/`)
4. Create routes (`app/api/routes/`)
5. Create services (`app/services/`)
6. Write tests (`tests/unit/` and `tests/integration/`)
7. Update documentation
8. Commit and push
9. Create PR

### Adding a Database Migration

```bash
# Create new migration
alembic revision --autogenerate -m "Add new column"

# Review the migration file
# app/alembic/versions/

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Adding Dependencies

```bash
# For production
pip install package-name
pip freeze > requirements.txt

# For development
pip install package-name
pip freeze > requirements-dev.txt
```

## Issues and Bug Reports

### Before Creating an Issue

- Search existing issues
- Check documentation
- Try latest code from main

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version
- OS
- Database version
```

## Getting Help

- Check [API Documentation](./docs/API.md)
- Read [Architecture](./ARCHITECTURE.md)
- Open [GitHub Discussions](https://github.com/hasanhsynsahinn/task-management-api/discussions)
- Email: contact@hasanhayat.dev

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.
