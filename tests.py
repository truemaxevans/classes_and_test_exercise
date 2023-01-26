import unittest
from main import BaseClass

class TestBaseClass(unittest.TestCase):

    def setUp(self):
        self.base_class = BaseClass("Kostyukov", True, name="Vlad", birth_date="1995", email="a@gmail.com", phone_number="371200000", address="Duntes 6a", photo="photo.jpg")

    def test_validate_name(self):
        self.base_class.validate_name("Vlad")
        self.assertRaises(ValueError, self.base_class.validate_name, "Vlad1")

    def test_validate_birth_date(self):
        self.base_class.validate_birth_date("1995")
        self.base_class.validate_birth_date("")
        self.assertEqual(self.base_class.birth_date, "2000")

    def test_validate_email(self):
        self.base_class.validate_email("a@gmail.com")
        self.base_class.validate_email("a")
        self.assertEqual(self.base_class.email, "a@gmail.com")

    def test_validate_phone_number(self):
        self.base_class.validate_phone_number("371200000")
        self.base_class.validate_phone_number("12345")
        self.assertRaises(ValueError, self.base_class.validate_phone_number, "123")

    def test_validate_is_administrator(self):
        self.base_class.validate_is_administrator(True)
        self.assertEqual(self.base_class.is_administrator, True)

    def test_validate_photo(self):
        self.base_class.validate_photo("photo.jpg")
        self.assertRaises(ValueError, self.base_class.validate_photo, "test.png")
        self.assertRaises(ValueError, self.base_class.validate_photo, "not_exist.jpg")
