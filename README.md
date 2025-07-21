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
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project creates a RESTful HTTP API that accepts user prompts and returns Perplexity.AI answers by controlling a real browser in the background. It's ideal for research, learning, and demonstration where direct Perplexity API access is unavailable.

## Features

- Automates Perplexity.AI UI using Playwright and Chromium
- Async FastAPI endpoint for real-time, concurrent queries
- Extracts answer text and (where possible) web sources
- Multiple selectors and fallback logic for resilience to UI changes
- Robust Docker container for cloud deployment or local testing
- Health and debug endpoints

## How It Works

1. Receives a prompt via API (GET or POST)
2. Launches a headless Chromium browser using Playwright
3. Fills and submits the prompt into Perplexity.AI's search box
4. Waits for the answer to load, then extracts answer text (optionally, sources)
5. Returns results as JSON via API

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
- Playwright dependencies (see Dockerfile or Playwright docs)
- Docker (optional, for containerized deployment)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsPunitx/Perplexity-Automation.git
   cd Perplexity-Automation
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Chromium browser**
   ```bash
   playwright install chromium
   playwright install-deps chromium
   ```

5. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # edit `.env` as needed
   ```

### Run API Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Single Search

```bash
curl "http://localhost:8000/search?prompt=What%20is%20artificial%20intelligence?"
```

### API Documentation

After running, view interactive docs at:

```
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint         | Description                     |
|--------|-----------------|---------------------------------|
| GET    | `/health`       | Returns service status          |
| GET    | `/search`       | Search: provide prompt as query |
| POST   | `/search`       | Search: provide prompt as JSON  |
| POST   | `/batch-search` | Search multiple prompts         |
| GET    | `/docs`         | API Swagger documentation       |

## Deployment

### Using Docker

1. **Build Docker image**
   ```bash
   docker build -t perplexity-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env perplexity-api
   ```

### (Optional) Deploy to Other Platforms

- For Render or other PaaS, set environment variables and use Docker as environment for browser support.
- Never expose your endpoints to the public unless authentication/rate-limiting is in place.

## Troubleshooting

- **"Target page, context or browser has been closed"**  
  Ensure browser and context are not closed after each request. Use FastAPI's lifespan manager.
- **Selector Errors**  
  Update selectors in `automator.py` if Perplexity changes UI.
- **Browser Install Issues**  
  Re-run `playwright install chromium` and check dependencies.
- **Timeouts**  
  Increase timeout value in your config or API call.

## Legal & Ethical Notice

- This project automates a public website and is for educational and demonstration use only.
- Carefully review and comply with Perplexity.AI’s terms of service.
- Avoid high-frequency or commercial use.
- Always respect fair use, rate limits, and web service resources.

## Contributing

Pull requests or issues are welcome! See `CONTRIBUTING.md` for guidelines.

## License

MIT License – see `LICENSE` file for full terms.

## Acknowledgments

- [Perplexity.AI](https://www.perplexity.ai/) for the UI searched
- [Microsoft Playwright](https://playwright.dev/) for browser automation
- [FastAPI](https://fastapi.tiangolo.com/) for web API architecture

> For personal and research use only. Not an official API.
