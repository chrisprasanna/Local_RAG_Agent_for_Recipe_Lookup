# Recipe Chatbot

## Overview

The **Recipe Chatbot** is a Python-based application that helps users find easy and healthy recipes from [allrecipes.com](https://www.allrecipes.com). Users can ask the chatbot for meal ideas, and it will scrape recipes from the website, format the results, and present them in a user-friendly format using Markdown syntax.

The application uses the `langchain` framework and the `OllamaLLM` model to generate responses, making it conversational and engaging.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.9 or later
- Docker (optional, for containerized usage)
- Git (optional, for cloning the repository)
- [Ollama](https://ollama.ai/) (for running the LLM)

---

## Installation and Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/chrisprasanna/Local_RAG_Agent_for_Car_Manual.git
cd Local_RAG_Agent_for_Car_Manual
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate  # For Windows
# source venv/bin/activate  # For macOS/Linux
```

### 3. Install Dependencies
Install the required Python libraries using pip:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Pull the Required Ollama Models
Ensure you have Ollama installed locally, then pull the required model:
```bash
ollama pull llama3.2
```

---

## Usage Instructions

### Run the Application
To start the chatbot, run the following command:
```bash
python main.py
```

### Interact with the Chatbot
- The chatbot will prompt you to ask a question about what you want to cook.
- Example: "What can I make with chicken and broccoli?"
- Type `q` or `quit` to exit the chatbot.

---

## Overview of Components

1. **`main.py`**
   - The main application file that:
     - Accepts user input.
     - Scrapes recipes from allrecipes.com using `urllib` and `BeautifulSoup`.
     - Formats the recipe data and generates a response using the `OllamaLLM` model.
     - Includes a FastAPI-based health check endpoint for monitoring.

2. **`allrecipes_scraper.py`**
   - Contains the `AllRecipesScraper` class for scraping recipes from allrecipes.com.
   - Includes methods for searching recipes and fetching detailed recipe information.

3. **`requirements.txt`**
   - Lists all the dependencies required for the project.

4. **`Dockerfile`**
   - Defines the Docker image for containerizing the application.

5. **`tests/test_main.py`**
   - Contains unit tests for the `fetch_recipe_from_allrecipes` function.

6. **`.github/workflows/test.yml`**
   - GitHub Actions workflow for automated testing and Docker builds.

---

## Dependencies

The project uses the following Python libraries:

- `langchain-core`: Core framework for building conversational AI applications.
- `langchain-ollama`: Integration with the Ollama LLM.
- `beautifulsoup4`: For parsing and extracting data from HTML.
- `urllib3`: For making HTTP requests.
- `fastapi`: For creating a health check endpoint.
- `uvicorn`: For running the FastAPI server.
- `pytest`: For testing.
- `flake8` and `black`: For linting and formatting.

---

## Docker Usage

### Build the Docker Image
Ensure Docker is installed and running, then build the image:
```bash
docker build -t recipe-chatbot .
```

### Run the Docker Container
Run the chatbot in a container:
```bash
docker run --rm -p 8080:8080 recipe-chatbot
```

### Stop the Container
The container will stop automatically when the chatbot exits.

---

## Limitations

- **Web Scraping Dependency**: The application relies on the structure of allrecipes.com. If the website changes its structure, the scraper may break.
- **Limited Query Understanding**: The chatbot may not handle complex or ambiguous queries well.
- **Internet Requirement**: The application requires an active internet connection to fetch recipes.
- **Performance**: Web scraping can be slow, especially for large queries or during high traffic on allrecipes.com.

---

## Possible Improvements

- Improve query understanding using advanced NLP techniques.
- Cache results to reduce repeated web scraping.
- Add a web-based or mobile interface for easier interaction.
- Enhance error handling for failed web scraping or invalid user queries.
- Add support for multiple recipe websites.