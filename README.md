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
git clone https://github.com/chrisprasanna/Local_RAG_Agent_for_Recipe_Lookup.git
cd Local_RAG_Agent_for_Recipe_Lookup
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
python -m pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

### 4. Pull the Required Ollama Models
Ensure you have Ollama installed locally, then pull the required model:
```bash
ollama pull llama3.2
```

## Usage Instructions
### Run the Application
To start the chatbot, run the following command:
```bash
python [main.py](http://_vscodecontentref_/1)
```
### Interact with the Chatbot
- The chatbot will prompt you to ask a question about what you want to cook.
- Example: "What can I make with chicken and broccoli?"
- Type `q` or `quit` to exit the chatbot.

## Overview of Components
1. `main.py`
The main application file that:
    - Accepts user input.
    - Scrapes recipes from allrecipes.com using `requests` and `BeautifulSoup`.
    - Formats the recipe data and generates a response using the `OllamaLLM` model.

2. `requirements.txt`
Lists all the dependencies required for the project.

3. `Dockerfile`
Defines the Docker image for containerizing the application.

4. `tests/test_main.py`
Contains unit tests for the `fetch_recipe_from_allrecipes` function.

5. `.github/workflows/test.yml`
GitHub Actions workflow for automated testing and Docker builds.

## Dependencies
The project uses the following Python libraries:

- `langchain`: Framework for building conversational AI applications.
- `langchain-ollama`: Integration with the Ollama LLM.
- `requests`: For making HTTP requests to fetch recipe data.
- `beautifulsoup4`: For parsing and extracting data from HTML.

## Docker Usage
### Build the Docker Image
Ensure Docker is installed and running, then build the image:
```bash
docker build -t recipe-chatbot .
```
### Run the Docker Container
Run the chatbot in a container:
```bash
docker run --rm recipe-chatbot
```
### Stop the Container
The container will stop automatically when the chatbot exits.

## Limitations
- **Web Scraping Dependency**: The application relies on the structure of allrecipes.com. If the website changes its structure, the scraper may break.
- **Limited Query Understanding**: The chatbot may not handle complex or ambiguous queries well.
- **Internet Requirement**: The application requires an active internet connection to fetch recipes.
- **Performance**: Web scraping can be slow, especially for large queries or during high traffic on allrecipes.com.

## Possible Improvements
- Improve query understanding using advanced NLP techniques.
- Cache results to reduce repeated web scraping.
- Add a web-based or mobile interface for easier interaction.
- Enhance error handling for failed web scraping or invalid user queries.
- Add support for multiple recipe websites. 