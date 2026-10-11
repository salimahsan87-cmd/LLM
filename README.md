# AI-Powered Telegram Bot with RAG

A Python-based Telegram bot that combines Retrieval-Augmented Generation (RAG), vector search, a language model API, and real-time weather information.

## Features

- **AI Chat:** Generates responses using a language model through the GapGPT API.
- **Retrieval-Augmented Generation (RAG):** Retrieves relevant information from a collection of Persian documents before generating a response.
- **Semantic Search:** Uses Sentence Transformers to convert text into embeddings.
- **Vector Database:** Uses ChromaDB to store document embeddings and retrieve relevant content.
- **Weather Information:** Retrieves current weather data and temperature in Celsius using the OpenWeatherMap API.
- **Photo Handling:** Receives and saves images sent by Telegram users.
- **Voice Message Handling:** Receives and saves voice messages.

## Technologies Used

- Python
- python-telegram-bot
- Sentence Transformers
- ChromaDB
- OpenAI Python SDK
- GapGPT API
- OpenWeatherMap API
- Requests

## How RAG Works in This Project

1. A user sends a text message to the Telegram bot.
2. The Sentence Transformer model converts the message into an embedding.
3. ChromaDB searches for the two most relevant documents.
4. The retrieved documents are added to the prompt.
5. The language model generates a response using the retrieved context.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the placeholders with your repository URL and project folder name.

### 2. Install dependencies

```bash
pip install python-telegram-bot requests openai sentence-transformers chromadb
```

### 3. Configure API keys

The application requires the following API keys:

- Telegram Bot API token
- GapGPT API key
- OpenWeatherMap API key

The current implementation requests these keys through Python's `getpass()` function, so they do not need to be hardcoded into the source code.

**Security:** Never commit API keys or other secrets to a public repository.

### 4. Run the bot

```bash
python Bot_Telegram.py
```

Replace `Bot_Telegram.py` with the name of your Python entry-point file.

## Available Commands

| Command | Description |
|---|---|
| `/start` | Starts the bot |
| `/weather` | Requests a city name and returns weather information |

## Current Limitations

- The RAG knowledge base currently contains five predefined Persian documents.
- The system retrieves the two closest documents without a calibrated relevance threshold.
- Photo and voice handlers save incoming files; image understanding and speech recognition are not implemented.
- Error handling and production deployment can be improved.

## Future Improvements

- Add document ingestion for larger knowledge bases.
- Evaluate retrieval quality and tune relevance thresholds.
- Improve exception handling and logging.
- Add automated tests.
- Use environment variables or a dedicated secrets manager for API credentials.
- Improve file handling for multiple concurrent users.

## Purpose

This project was developed as a practical learning project to explore the integration of Telegram bots, language model APIs, semantic search, and Retrieval-Augmented Generation in Python.
