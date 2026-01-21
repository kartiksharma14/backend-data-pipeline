# Backend Data Pipeline – Technical Assessment

## Overview
This project implements a containerized backend data pipeline:

Flask Mock API → FastAPI Ingestion Service → PostgreSQL

## Tech Stack
- Python 3.10
- Flask
- FastAPI
- PostgreSQL 15
- SQLAlchemy
- Docker & Docker Compose

## Architecture
- Flask serves paginated mock customer data from JSON
- FastAPI ingests data, handles pagination automatically, and upserts into PostgreSQL
- FastAPI exposes query APIs backed by the database

## Setup Instructions

### Prerequisites
- Docker Desktop
- Git

### Start Services
```bash
docker compose up -d --build
