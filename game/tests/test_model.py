import pytest
from test_plus.test import TestCase

from game.model import Model


class ModelTestCase(TestCase):
    def setUp(self):
        self.m = Model()

    def test_create(self):
        m = Model()
        self.assertNotEqual(m, None)

    def test_result_5(self):
        result = self.m.step(1.25, 0.25)
        self.assertEquals(result, 5)

    def test_result_fraction(self):
        result = self.m.step(1, 2)
        self.assertEquals(result, 0.5)

