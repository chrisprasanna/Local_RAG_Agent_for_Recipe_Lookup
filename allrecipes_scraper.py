from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import ssl
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AllRecipesScraper:
    @staticmethod
    def search(search_string):
        base_url = "https://www.allrecipes.com/search?"
        query_url = urllib.parse.urlencode({"q": search_string})
        url = base_url + query_url

        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
        opener = urllib.request.build_opener(handler)
        response = opener.open(req)
        html_content = response.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        search_data = []
        articles = soup.findAll("a", {"class": "mntl-card-list-items"})
        articles = [a for a in articles if a["href"].startswith("https://www.allrecipes.com/recipe/")]

        for article in articles:
            data = {}
            try:
                data["name"] = article.find("span", {"class": "card__title"}).get_text().strip()
                data["url"] = article['href']
            except Exception as e:
                logger.error(f"Error parsing article: {e}")
            if data:
                search_data.append(data)

        return search_data

    @classmethod
    def get(cls, url):
        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
        opener = urllib.request.build_opener(handler)
        response = opener.open(req)
        html_content = response.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        data = {
            "name": cls._get_name(soup),
            "ingredients": cls._get_ingredients(soup),
            "steps": cls._get_steps(soup),
        }
        return data

    @staticmethod
    def _get_name(soup):
        return soup.find("h1", {"id": "article-heading_2-0"}).get_text().strip()

    @staticmethod
    def _get_ingredients(soup):
        return [li.get_text().strip() for li in soup.find("div", {"id": "mntl-structured-ingredients_1-0"}).find_all("li")]

    @staticmethod
    def _get_steps(soup):
        return [li.get_text().strip() for li in soup.find("div", {"id": "recipe__steps_1-0"}).find_all("li")]

# Example usage in your chatbot
def fetch_recipe_from_allrecipes(query):
    try:
        # Search for recipes
        search_results = AllRecipesScraper.search(query)
        if not search_results:
            logger.error("No recipes found.")
            return None, None, None, None

        # Get the first recipe's details
        recipe_url = search_results[0]["url"]
        recipe_details = AllRecipesScraper.get(recipe_url)

        title = recipe_details["name"]
        ingredients = "\n".join(f"* {item}" for item in recipe_details["ingredients"])
        instructions = "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe_details["steps"]))

        return title, ingredients, instructions, recipe_url
    except Exception as e:
        logger.error(f"Error fetching recipe: {e}")
        return None, None, None, None