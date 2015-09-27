from unittest import TestCase
from generator import VideoPodGenerator

__author__ = 'lyc'


class TestVideoPodGenerator(TestCase):
    def test_GetInstance(self):
        generator = VideoPodGenerator(10)
        instance = generator.GetInstance()
        self.assertEqual(len(instance), 10)
