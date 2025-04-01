import unittest
from main import fetch_recipe_from_allrecipes

class TestRecipeChatbot(unittest.TestCase):
    def test_search_recipes(self):
        # Test searching for recipes with a valid query
        search_results = fetch_recipe_from_allrecipes("chicken")
        print(search_results)
        self.assertIsNotNone(search_results)
        self.assertGreater(len(search_results), 0)
    def test_fetch_recipe(self):
        # Test fetching a recipe with a valid query
        title, ingredients, instructions, link = fetch_recipe_from_allrecipes("chicken")
        self.assertIsNotNone(title)
        self.assertIsNotNone(ingredients)
        self.assertIsNotNone(instructions)
        self.assertIsNotNone(link)

    def test_fetch_recipe_invalid_query(self):
        # Test fetching a recipe with an invalid query
        title, ingredients, instructions, link = fetch_recipe_from_allrecipes("invalidquery12345")
        self.assertIsNone(title)
        self.assertIsNone(ingredients)
        self.assertIsNone(instructions)
        self.assertIsNone(link)

if __name__ == "__main__":
    unittest.main()