from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import ssl
import logging
import random
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of common user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3",
    "Mozilla/5.0 (Machintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

class AllRecipesScraper:
    @staticmethod
    def search(search_string):
        """
        Search recipes parsing the returned HTML data.
        """
        # Valid search URL for AllRecipes
        base_url = "https://www.allrecipes.com/search/results/"
        query_url = urllib.parse.urlencode({"search": search_string})
        url = f"{base_url}?{query_url}"

        try:
            # Make the HTTP request with a random user agent
            req = urllib.request.Request(url)
            req.add_header('User-Agent', random.choice(USER_AGENTS))
            req.add_header('Accept-Language', 'en-US,en;q=0.5')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            req.add_header('Cookie', 'euConsent=true')

            # Handle HTTPS requests
            context = ssl._create_unverified_context()
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
            response = opener.open(req)
            html_content = response.read()

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
            search_data = []

            # Selector for recipe links
            articles = soup.select("a.card__titleLink")
            
            # If the above selector doesn't work, try alternative selectors
            if not articles:
                articles = soup.select("a.mntl-card-list-items")

            if not articles:
                articles = soup.select("a.comp.mntl-card-list-items")

            # Filter only recipe links
            articles = [a for a in articles if a.get("href") and "recipe" in a.get("href")]

            for article in articles:
                data = {}
                try:
                    # Try different selectors for title
                    title_elem = article.select_one(".card__title-text")
                    if not title_elem:
                        title_elem = article.select_one(".card__title")
                    if title_elem:
                        data["name"] = title_elem.get_text().strip()
                    else:
                        data["name"] = article.get_text().strip()
                    data["url"] = article.get("href")

                except Exception as e:
                    logger.error(f"Error parsing article: {e}")
                if data and "name" in data and "url" in data:
                    search_data.append(data)

            if not search_data:
                logger.warning(f"No recipes found for query: {search_string}.")
            return search_data

        except Exception as e:
            logger.error(f"Error fetching search results: {e}")
            return []

    @classmethod
    def get(cls, url):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', random.choice(USER_AGENTS))
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            req.add_header('Cookie', 'euConsent=true')

            context = ssl._create_unverified_context()
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
            response = opener.open(req)
            html_content = response.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            name = cls._get_name(soup)
            ingredients = cls._get_ingredients(soup)
            steps = cls._get_steps(soup)

            if not name or not ingredients or not steps:
                logger.error("Failed to parse recipe details.")
                return None

            data = {
                "name": name,
                "ingredients": ingredients,
                "steps": steps,
            }
            return data
        except Exception as e:
            logger.error(f"Error fetching recipe details: {e}")
            return None

    @staticmethod
    def _get_name(soup):
        # Try different selectors for the recipe name
        selectors = [
            "h1#article-heading_2-0",
            "h1.article-heading",
            "h1.recipe-title",
            "h1.heading-content",
            "h1.recipe-header__title",
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
            
        # If no selector works, try to find any h1 element
        h1 = soup.find("h1")
        if h1:
            return h1.get_text().strip()
        
        return None

    @staticmethod
    def _get_ingredients(soup):
        # Try different selectors for the ingredients list
        selectors = [
            "div#mntl-structured-ingredients_1-0 li",
            "u1.ingredients-section li",
            "u1.mntl-structured-ingredients__list li",
            "div.recipe-ingredients li",
            "div.ingredients-section li",
        ]

        for selector in selectors:
            elements = soup.select_one(selector)
            if elements:
                return [li.get_text().strip() for li in elements]
        
        return []

    @staticmethod
    def _get_steps(soup):
        # Try different selectors for the steps list
        selectors = [
            "div#recipe__steps_1-0 li",
            "o1.recipe-directions__list li",
            "o1.mntl-sc-block-group--OL li",
            "div.recipe-instructions ol li",
            "div.instructions-section li",
        ]

        for selector in selectors:
            elements = soup.select_one(selector)
            if elements:
                return [li.get_text().strip() for li in elements]
        
        return []

# Example usage in your chatbot
def fetch_recipe_from_allrecipes(query):
    try:
        # Add small delay to avoid being rate limited
        time.sleep(1)

        # Search for recipes
        search_results = AllRecipesScraper.search(query)
        if not search_results:
            logger.warning(f"No search results found for query: {query}.")
            return None, None, None, None

        # Get the first recipe's details
        recipe_url = search_results[0]["url"]
        logger.info(f"Fetching recipe from URL: {recipe_url}")

        recipe_details = AllRecipesScraper.get(recipe_url)
        if not recipe_details:
            logger.error(f"Failed to fetch recipe details from URL: {recipe_url}.")
            return None, None, None, None

        title = recipe_details["name"]
        ingredients = "\n".join(f"* {item}" for item in recipe_details["ingredients"])
        instructions = "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe_details["steps"]))

        return title, ingredients, instructions, recipe_url
    except Exception as e:
        logger.error(f"Error fetching recipe: {e}")
        return None, None, None, None