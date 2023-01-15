# Quotetje

Quotetje is a free, open-source quotations RESTful Web API.

## API Reference

#### Service Overview

| **Endpoint**     | **HTTP Method** | **CRUD Method** | **Result**                  |
| ---------------- | --------------- | --------------- | --------------------------- |
| `/random`        | GET             | READ            | Get a single random quote   |
| `/quotes`        | GET             | READ            | Get all quotes              |
| `/quotes/:id`    | GET             | READ            | Get a single quote          |
| `/quotes/:tag`   | GET             | READ            | Get all quotes with tag     |
| `/authors`       | GET             | READ            | Get all authors             |
| `/authors/:id`   | GET             | READ            | Get all quotes of an author |
| `/favorites`     | GET             | READ            | Get all saved quotes        |
| `/favorites/`:id | GET             | READ            | Get a single saved quote    |
| `/favorites`     | POST            | CREATE          | Save a personal quote       |
| `/quotetjes`     | POST            | CREATE          | Create a personal quote     |
| `/quotetjes/:id` | PUT             | UPDATE          | Update a personal quote     |
| `/quotetjes/:id` | DELETE          | DELETE          | Delete a personal quote     |

#### Get all quotes

```HTTP
GET /quotes
```

## Tech Stack

- FastAPI

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

| **Variable**             | **Example**                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| `TZ`                     | `Europe/Amsterdam`                                                                         |
| `PUID`                   | `1000`                                                                                     |
| `PGID`                   | `1000`                                                                                     |
| `POSTGRES_DB_DFT`        | `quotes`                                                                                   |
| `POSTGRES_DB_USER`       | `postgres-db-user`                                                                         |
| `POSTGRES_DB_PASSWORD`   | `postgres-db-pass`                                                                         |
| `POSTGRES_DB_APP_USER`   | `postgres-db-api-user`                                                                     |
| `POSTGRES_DB_APP_PASS`   | `postgres-db-api-pass`                                                                     |
| `POSTGRES_DB_CONNECTION` | `postgresql://${POSTGRES_DB_APP_USER}:${POSTGRES_DB_APP_PASS}@postgres/${POSTGRES_DB_DFT}` |
| `API_VERSION`            | `/api/v1`                                                                                  |
| `API_VERSION_NUMBER`     | `0.1.0`                                                                                    |

## How to use

To exececueete this project run

```bash
docker-compose up -d --build
```

## scans image - vulnerabilities

```bash
docker scan quotepje-quotes-api
```

## run the tests

```bash
docker-compose exec quotes-api pytest .
```

## Quote sources

- [Quotable](https://github.com/lukePeavey/quotable)
- [Official Joke API](https://github.com/15Dkatz/official_joke_api)
- [JokeApi](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)

## Acknowledgements

...

## Authors

- [@difegam](https://github.com/difegam)
