# Isaac Twitter Bot

Isaac is an automated Twitter (X) bot designed to engage with the community on topics ranging from Science and Philosophy to Technology and Malawi. Named after the persona "Isaac," a Malawian intellectual, the bot uses AI to generate insightful, witty, and analytical engagement.

## Features

- **Automated Engagement**: Isaac searches for relevant tweets and performs a "triple action": Quote, Repost, and Reply.
- **Persona-Driven AI**: Powered by OpenRouter (GPT-3.5 Turbo), Isaac maintains a consistent Malawian intellectual persona.
- **Topic Focus**: Targeted keywords include Science, Philosophy, Quantum Physics, Biotechnology, and Malawian Tech.
- **Web Interface**: A FastAPI-based dashboard to monitor live logs and bot health.
- **Deployment Ready**: Includes a `render.yaml` for seamless deployment on Render.com.

## Tech Stack

- **Language**: Python 3.x
- **Framework**: FastAPI
- **Twitter API**: Tweepy
- **AI Integration**: OpenAI/OpenRouter
- **Server**: Uvicorn

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Twitter Developer Account with API credentials.
- An OpenRouter API key.

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your credentials (refer to `.env.example` for the required keys):
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`
- `TWITTER_BEARER_TOKEN`
- `OPENROUTER_API_KEY`

### 4. Running the Bot
Start the FastAPI server and the bot loop:
```bash
python main.py
```
The bot will be accessible at `http://localhost:8000`.

## API Endpoints

- `GET /`: Returns bot status and recent activity logs.
- `GET /logs`: Returns the full history of session logs.
- `GET /health`: Basic health check for monitoring services.

## Project Structure

- `main.py`: Entry point, FastAPI app, and the main engagement loop.
- `ai_orchestrator.py`: Logic for generating persona-based responses using AI.
- `twitter_client.py`: Wrapper for Tweepy to interact with the Twitter API.
- `isaac_persona.md`: Definition of Isaac's personality and values.
- `render.yaml`: Configuration for Render deployment.

## License
[MIT License](LICENSE) (or specify your preferred license)
