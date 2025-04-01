from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = OllamaLLM(
    model="llama3.2",
    temperature=0.3,  # lower the temperature for a more focused response
)

# Create a template for the chat prompt to format the recipe response
template = """
You are an expert chef and you are looking for a recipe to cook. You want to cook a dish that is easy to make and is healthy.
Format your responses using Markdown syntax.

Question: {question}

Recipe Title: {title}

Ingredients:
{ingredients}

Instructions:
{instructions}

Link: {link}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def fetch_recipe_from_allrecipes(query):
    """
    Fetch a recipe from allrecipes.com based on the query.
    """
    try:
        # Search for recipes on allrecipes.com
        search_url = f"https://www.allrecipes.com/search/results/?search={query}"
        response = requests.get(search_url)
        response.raise_for_status()

        # Parse the search results page
        soup = BeautifulSoup(response.text, "html.parser")
        recipe_link = soup.select_one(".card__titleLink")
        if not recipe_link:
            return None, None, None, None

        recipe_url = recipe_link["href"]

        # Fetch the recipe page
        recipe_response = requests.get(recipe_url)
        recipe_response.raise_for_status()
        recipe_soup = BeautifulSoup(recipe_response.text, "html.parser")

        # Extract recipe title
        title = recipe_soup.select_one(".headline.heading-content").get_text(strip=True)

        # Extract ingredients
        ingredients = recipe_soup.select(".ingredients-item")
        ingredients_list = "\n".join(
            f"* {item.get_text(strip=True)}" for item in ingredients
        )

        # Extract instructions
        instructions = recipe_soup.select(".instructions-section-item")
        instructions_list = "\n".join(
            f"{i+1}. {step.get_text(strip=True)}"
            for i, step in enumerate(instructions)
        )

        return title, ingredients_list, instructions_list, recipe_url
    except Exception as e:
        logger.error(f"Error fetching recipe: {e}")
        return None, None, None, None


def main():
    print("\n# Welcome to the Cooking Recipe Chatbot!\n")
    print("\nThis chatbot will help you find a cooking recipe that is easy to make and healthy.")
    print("\nType 'q' to quit.\n")
    while True:
        try:
            print("\n---")
            question = input("Your question: ")
            if question.lower() in ("q", "quit", "exit"):
                break

            # Fetch a recipe from allrecipes.com
            title, ingredients, instructions, link = fetch_recipe_from_allrecipes(question)
            if not title:
                print("\nNo recipes found. Please try a different query.")
                continue

            # Generate a response using the model
            response = chain.invoke(
                question=question,
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                link=link,
            )
            print("\nResponse:")
            print(response)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print("\nAn error occurred. Please try again.")


if __name__ == "__main__":
    main()