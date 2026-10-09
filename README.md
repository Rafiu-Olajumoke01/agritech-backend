# Agritech Backend

The Django backend for [Agritech](https://github.com/Rafiu-Olajumoke01/agritech), a platform that lets farmers in rural areas list their produce by SMS, even without internet access.

## What it does

- Receives incoming SMS messages from farmers through a webhook endpoint
- Parses and validates each message
- Creates product listings from valid messages
- Serves listings to the website for buyers to browse

## Tech stack

- Python
- Django

## Current status

The SMS receiving and parsing flow is built and has been tested with simulated SMS requests. Connection to a live SMS gateway is planned for the pilot stage.

## Planned

- Buyer orders and confirmation by agents or farmers
- Payments and delivery coordination
- Background processing for messages and notifications

## Author

Built by **Jummy**, a backend-focused software engineer working with Python, Django, Celery, Redis, and PostgreSQL.

GitHub: [Rafiu-Olajumoke01](https://github.com/Rafiu-Olajumoke01)
