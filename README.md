# GameBackEnd

A Flask backend for mobile games. It manages user data and game-related features through a MySQL database and can run as a Firebase/Google Cloud Function.

## Main technologies

- Flask and Flask-SQLAlchemy
- MySQL with PyMySQL
- Pydantic request validation
- Google Cloud SQL Connector
- Firebase Functions

## Project structure

```text
app/
├── api/       # Domain-based Flask blueprints
├── models/    # SQLAlchemy models
├── schemas/   # Pydantic request schemas
├── config.py  # Environment configuration
├── database.py
└── errors.py  # Central error handlers
docs/api/      # API documentation
main.py        # Firebase Functions entry point
```

## Local setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure the required environment variables:

```bash
export ENVIRONMENT=DEVELOPMENT
export DB_HOST=localhost
export GCSQL_USER_NAME=your_database_user
export GCSQL_PASSWORD=your_database_password
export GCSQL_DB_NAME=your_database_name
```

Start the Flask development server:

```bash
flask --app app run --debug
```

Keep credentials in local environment files or a secret manager. Do not commit them to the repository.

## API domains

The application contains endpoints for users, categories, statistics, missions, daily levels, progression, Catventure, badges, and tournaments.

Available documentation:

- [Users API](docs/api/users.md)
- [Categories API](docs/api/categories.md)
- [Statistics API](docs/api/statistics.md)

## Deployment

The `jigsaw_functions` function in `main.py` is the HTTP entry point for deployment to Firebase Functions or Google Cloud Functions.

## License

This project is licensed under the [MIT License](LICENSE).
