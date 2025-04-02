import unittest
from unittest.mock import patch
from allrecipes_scraper import fetch_recipe_from_allrecipes, AllRecipesScraper

class TestRecipeChatbot(unittest.TestCase):
    def test_search_recipes(self):
        # Test searching for recipes with a valid query
        search_results = fetch_recipe_from_allrecipes("chicken")
        self.assertIsNotNone(search_results)
        # We can't guarantee the exact number of results, but we can check if it's a list
        self.assertIsInstance(search_results, list)

    def test_fetch_recipe(self):
        # Mock the search results to ensure consistent test behavior
        with patch.object(AllRecipesScraper, 'search') as mock_search:
            mock_search.return_value = [
                {
                    "name": "Test Recipe",
                    "url": "https://www.allrecipes.com/recipe/280740/hawaiian-garlic-shrimp-scampi/"
                }
            ]
            
            # Mock the get method to return a consistent recipe
            with patch.object(AllRecipesScraper, 'get') as mock_get:
                mock_get.return_value = {
                    "name": "Test Recipe",
                    "ingredients": ["1 lb shrimp", "2 cloves garlic"],
                    "steps": ["Cook shrimp", "Add garlic"],
                }
                
                # Now test the function
                title, ingredients, instructions, link = fetch_recipe_from_allrecipes("chicken")
                self.assertIsNotNone(title)
                self.assertIsNotNone(ingredients)
                self.assertIsNotNone(instructions)
                self.assertIsNotNone(link)

    def test_fetch_recipe_invalid_query(self):
        with patch.object(AllRecipesScraper, 'search') as mock_search:
            # Mock the search method to return an empty list
            mock_search.return_value = []
            
            # Test fetching a recipe with an invalid query
            title, ingredients, instructions, link = fetch_recipe_from_allrecipes("nonexistentrecipe")
            self.assertIsNone(title)
            self.assertIsNone(ingredients)
            self.assertIsNone(instructions)
            self.assertIsNone(link)

if __name__ == "__main__":
    unittest.main()