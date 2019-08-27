import unittest
from game.settings import settings

class SettingsTest(unittest.TestCase):
    def test_settings_not_empty(self):   
        self.assertGreater(len(settings.keys()), 0) 
    
    def test_settings_has_difficulty(self):
        self.assertIn('difficulty', settings.keys())
    
    def test_settings_has_difficulty_items(self):
        self.assertEqual(type(settings['difficulty']), list)
        self.assertGreater(len(settings['difficulty']), 0)
    
    def test_difficulty_entries_complete(self):
        for item in settings['difficulty']:
            self.assertIn('name', item.keys())
            self.assertEqual(type(item['name']), str)
            self.assertIn('width', item.keys())
            self.assertEqual(type(item['width']), int)
            self.assertIn('height', item.keys())
            self.assertEqual(type(item['height']), int)
            self.assertIn('bombs', item.keys())
            self.assertEqual(type(item['bombs']), int)

    def test_settings_has_high_score_count(self):
        self.assertIn('high_score_count', settings.keys())
        self.assertEqual(type(settings['high_score_count']), int)
    
    def test_high_score_count_at_least_three(self):
        self.assertGreaterEqual(settings['high_score_count'], 3)

if __name__ == '__main__':
    unittest.main()