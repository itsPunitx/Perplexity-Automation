# Perplexity Automation API

A FastAPI-based server that automates Perplexity.AI searches using browser automation (Playwright). This project simulates the Perplexity API by interacting with the website UI, extracting answers, and serving them through a clean HTTP API.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Legal & Ethical Notice](#legal--ethical-notice)

## Overview

This project creates a simple HTTP API that accepts user prompts and returns Perplexity.AI answers by controlling a browser in the background. It is intended for research, learning, and demonstration purposes where direct Perplexity API access is unavailable.

## Features

- Automates Perplexity.AI UI using Playwright
- Async FastAPI endpoint for real-time queries
- Returns extracted answer text and (where possible) reference sources
- Multiple selectors and fallback logic for resilience to UI changes
- Dockerfile for cloud deployment
- Health and debug endpoints

## How It Works

1. Receives a prompt via API (GET or POST).
2. Launches a headless Chromium browser session using Playwright.
3. Fills the prompt into Perplexity.AI's input box and submits the query.
4. Waits for the answer element to appear.
5. Extracts the answer text and (optionally) sources.
6. Returns the result as JSON to the API client.

## Project Structure

```
perplexity-automation-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── automator.py
│   └── config.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── build.sh
└── README.md
```

## Setup & Installation

### Requirements

- Python 3.11+
- Node.js & npm (for Playwright installation, optional)
- Docker (for containerized deployment, optional)

### Install Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/perplexity-automation-api.git
   cd perplexity-automation-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize Playwright browsers:

   ```bash
   playwright install chromium
   playwright install-deps chromium
   ```

5. (Optional) Copy `.env.example` to `.env` and adjust settings.

### Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Single Search

```bash
curl "http://localhost:8000/search?prompt=What%20is%20artificial%20intelligence?"
```

#### API Documentation

After running, visit:  
`http://localhost:8000/docs`  
for interactive documentation with example requests.

## API Endpoints

| Method | Endpoint     | Description                      |
|--------|-------------|----------------------------------|
| GET    | /health     | Returns service status           |
| GET    | /search     | Prompt search via query param    |
| POST   | /search     | Prompt search via JSON body      |
| POST   | /batch-search | Batch prompts, returns results |

## Deployment

### With Docker

1. Build the Docker image:

   ```bash
   docker build -t perplexity-api .
   ```

2. Run the container:

   ```bash
   docker run -p 8000:8000 --env-file .env perplexity-api
   ```

### On Render(or other PaaS)

- Upload your repo.
- Set environment variables as needed (see `.env.example`).
- For Docker: select Docker as the environment (recommended for browser support).

## Troubleshooting

- **"Target page, context or browser has been closed"**  
  Make sure browser and context are not closed on each request. Use the lifespan pattern in FastAPI.

- **Element Not Found Errors**  
  Update selectors in `automator.py` as Perplexity's UI changes.

- **Playwright Install Issues**
  Re-run `playwright install chromium` and ensure system dependencies are met.

- **Deployment on PaaS**
  Render/Heroku free tiers may not support headless browsers – prefer Docker deployment.

## Legal & Ethical Notice

- This project scrapes a public website and is for educational and demonstration use only.
- Check Perplexity.AI's terms of service before heavy or commercial use.
- Respect rate limits and be considerate in your usage.
- Direct commercial or high-volume use may violate Perplexity's policies.

## Contributing

Pull requests and issue reports are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## License

[MIT License](./LICENSE) – see LICENSE file for details.

## Acknowledgments

- [Perplexity.AI](https://www.perplexity.ai/) for the core search experience
- [Microsoft Playwright](https://playwright.dev/) for browser automation
- [FastAPI](https://fastapi.tiangolo.com/) for the async API framework

This README provides a comprehensive overview for users, contributors, and anyone deploying or evaluating your Perplexity automation API project. Adapt project URLs, usernames, and credits as suits your repository.
