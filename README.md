# SpendFlow

> Role-based expense submission and approval API built with FastAPI and PostgreSQL.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-async-4169E1?logo=postgresql&logoColor=white)
![Auth](https://img.shields.io/badge/Auth-JWT-blue)
![Status](https://img.shields.io/badge/status-active%20development-orange)

## Overview

SpendFlow is a backend API for employee expense workflows. Employees can register, authenticate, create and manage expenses, while managers can review company expenses and approve or reject pending submissions.

The project demonstrates practical backend engineering patterns: JWT authentication, role-based authorization, async SQLAlchemy access, explicit service layers, domain error handling, pagination/filtering, migrations, and an OpenAPI contract.

## Current capabilities

- User registration and JWT login
- Authenticated `/auth/me` identity endpoint
- Employee expense creation, listing, retrieval, update, and deletion
- Expense categories and lifecycle states
- Manager-only company expense listing
- Manager approval/rejection of pending expenses
- Filtering by status/category
- Pagination with bounded page size
- Async PostgreSQL persistence through SQLAlchemy
- Alembic database migrations
- Centralized application exception handling
- Generated OpenAPI schema checked into the repository

## Architecture

```text
Client
  |
  v
FastAPI routers
  |
  +--> auth dependencies / role checks
  |
  +--> service layer
  |
  +--> async SQLAlchemy
  |
  v
PostgreSQL
```

```text
app/
├── core/          # settings, security, logging, exception handling
├── db/            # async session/base
├── dependencies/  # authentication/authorization dependencies
├── models/        # users and expenses
├── routers/       # auth, employee expense, manager endpoints
├── schemas/       # API request/response models
├── services/      # auth and expense business logic
└── main.py        # FastAPI application
migrations/        # Alembic migrations
openapi.json       # generated API contract
```

## API highlights

| Area | Endpoint examples | Purpose |
|---|---|---|
| Authentication | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` | Identity and access |
| Employee expenses | `POST /expenses`, `GET /expenses`, `GET/PATCH/DELETE /expenses/{id}` | Expense lifecycle |
| Manager review | `GET /manager/expenses` | Company-wide review queue |
| Decisions | `POST /manager/expenses/{id}/approve`, `.../reject` | Role-protected decisions |

See `openapi.json` or run the application and open `/docs` for the complete contract.

## Configuration

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/spendflow
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit real secrets.

## Running locally

After creating a virtual environment and installing the project dependencies:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for Swagger UI.

> Reproducible dependency packaging is still being standardized in this repository; see the roadmap.

## Engineering focus

- **Role-based access:** manager-only operations are enforced through explicit dependencies.
- **Business-state rules:** approval/rejection logic is separated from route handlers and only applies to valid expense states.
- **Async persistence:** request paths use `AsyncSession` for database work.
- **Layered structure:** routers, schemas, models, dependencies, and services have distinct responsibilities.
- **API contract:** the checked-in OpenAPI document makes the current HTTP surface inspectable without running the app.

## Roadmap

Planned production hardening:

- [ ] Add a reproducible dependency/package definition
- [ ] Add unit/integration tests for auth and expense state transitions
- [ ] Add CI for linting, typing, and tests
- [ ] Add Docker Compose for local PostgreSQL + API
- [ ] Add audit history for manager decisions
- [ ] Add refresh-token/session strategy
- [ ] Add observability and deployment documentation
- [ ] Add a frontend dashboard as a separate client

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Work should be tracked through issues and focused pull requests.

## Status

SpendFlow is an active backend portfolio project. Implemented behavior and planned production hardening are deliberately documented separately.
