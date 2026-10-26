# TaskBox API

A simple task management REST API built with Python, FastAPI, PostgreSQL and Docker Compose.

## Features

- Create tasks
- List all tasks
- Mark tasks as completed
- Delete tasks
- Persistent PostgreSQL storage
- Container health checks
- Development mode with automatic code reloading

## Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- PostgreSQL 16
- Docker
- Docker Compose

## Project Structure

```text
task-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── compose.dev.yaml
├── requirements.txt
└── README.md
```

## Getting Started

### Requirements

- Docker Engine
- Docker Compose

Python dependencies are installed inside the Docker image.

### Configuration

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your database credentials.

### Run in development mode

```bash
docker compose -f compose.yaml -f compose.dev.yaml up --build -d
```

Check container status:

```bash
docker compose -f compose.yaml -f compose.dev.yaml ps
```

View API logs:

```bash
docker compose -f compose.yaml -f compose.dev.yaml logs -f api
```

Open the interactive API documentation:

http://localhost:8000/docs

### Stop the application

```bash
docker compose -f compose.yaml -f compose.dev.yaml down
```

Database data is stored in a named Docker volume and persists when containers are removed. To remove the project's containers, network and database volume, use `docker compose down -v` with the same Compose files. **This deletes the stored database data.**

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| PATCH | `/tasks/{task_id}/done` | Mark a task as completed |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Architecture

- **API:** FastAPI runs inside a Docker container.
- **Database:** PostgreSQL runs in a separate container.
- **Networking:** Docker Compose creates a network so the API can connect to the database using the hostname `db`.
- **Persistence:** A named Docker volume stores PostgreSQL data outside the database container.
- **Health checks:** Docker checks whether the API and database are ready.
- **Development workflow:** A bind mount exposes local application code inside the API container, and Uvicorn reloads the application when Python files change.

## Learning Goals

This project demonstrates containerization, Docker image builds, multi-container orchestration, environment variables, container networking, persistent volumes, health checks and development workflows with Docker Compose.
