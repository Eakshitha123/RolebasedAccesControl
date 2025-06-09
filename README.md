video explanation : https://drive.google.com/file/d/12lvKc9Tr-VpDaAao7J_AD4ivCl1xlmua/view?usp=sharing (open access link)

# Role-Based Access Control (RBAC) System

## Overview
This is a Role-Based Access Control (RBAC) system built with Flask. It provides secure user authentication and role-based access to different parts of the application. The system is modular, database-driven, and follows standard web security practices.

## Features
- User login and registration
- Role-based access control (e.g., admin, user)
- Protected routes for dashboard and file access
- Database integration using SQLAlchemy and SQLite
- Alembic for database migrations
- Modular Flask structure

## Security Principles (CIA Triad)

1. **Confidentiality**:
   - Only authorized users can access specific endpoints based on their roles.
   - Sensitive operations are protected using decorators and checks.

2. **Integrity**:
   - Data validation and ORM-based operations help prevent manipulation.
   - Alembic tracks and controls changes to the database schema.

3. **Availability**:
   - Flask handles lightweight, fast routing.
   - Basic error handling ensures uptime during unexpected inputs.

## Tech Stack
- Python 3.x
- Flask Web Framework
- SQLite Database
- SQLAlchemy ORM
- Alembic for DB migrations




