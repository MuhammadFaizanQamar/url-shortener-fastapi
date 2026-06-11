# URL Shortener API

A RESTful URL shortening service built with FastAPI. Paste a long URL, get a short code back, and track how many times each link was clicked.

## Live Demo
Coming soon

## Features
- Shorten any URL to a clean 7-character code
- Redirect short URLs to original destinations
- Track click counts for every shortened URL
- Interactive frontend UI
- Auto-generated API documentation at `/docs`

## Tech Stack
- **FastAPI** — modern Python API framework
- **SQLAlchemy** — database ORM
- **SQLite** — lightweight database
- **Pydantic** — request/response validation
- **Jinja2** — frontend templating
- **Bootstrap 5** — UI styling

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/ui` | Frontend interface |
| POST | `/shorten` | Shorten a URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/stats/all` | View all URLs and click counts |

## Request & Response Examples

**Shorten a URL:**

## Screenshots

### Frontend UI
![Frontend](screenshots/frontend.png)

### API Documentation
![API Docs](screenshots/docs.png)
```json 
