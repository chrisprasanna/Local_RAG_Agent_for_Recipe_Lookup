from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from allrecipes_scraper import fetch_recipe_from_allrecipes
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