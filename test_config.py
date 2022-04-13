from enum import Enum
from unittest import TestCase
from unittest.mock import patch
import os
from our_config import env


class TestConfig(TestCase):
    @patch.dict(os.environ, {'SOME_INT_VARIABLE': '123'})
    def test_int_variable_correctly_parsed(self):
        class Config:
            SOME_INT_VARIABLE = env.IntVar()

        config = Config()

        self.assertEqual(config.SOME_INT_VARIABLE, 123)

    @patch.dict(os.environ, {'SOME_STR_VARIABLE': 'something'})
    def test_str_var_correctly_parsed(self):
        class Config:
            SOME_STR_VARIABLE = env.StrVar()

        config = Config()

        self.assertEqual(config.SOME_STR_VARIABLE, 'something')

    def test_optional_var_returns_default_value_when_undefined(self):
        class Config:
            SOME_STR_VARIABLE = env.StrVar(default_value='none', optional=True)

        config = Config()

        self.assertEqual(config.SOME_STR_VARIABLE, 'none')

    def test_config_var_overridden_raises_error(self):
        class Config:
            SOME_STR_VARIABLE = env.StrVar()

        config = Config()

        with self.assertRaises(ValueError):
            config.SOME_STR_VARIABLE = 123


class EnumTestCase(TestCase):
    def setUp(self) -> None:
        class UserTypes(Enum):
            TEACHER = 'teacher'
            STUDENT = 'student'

        class Config:
            CURRENT_USER_TYPE = env.EnumVar(enum_cls=UserTypes)

        self.enum_cls = UserTypes
        self.config_cls = Config

    @patch.dict(os.environ, {'CURRENT_USER_TYPE': 'student'})
    def test_enum_existing_value_returns_value(self):
        config = self.config_cls()

        self.assertEqual(config.CURRENT_USER_TYPE, self.enum_cls.STUDENT)

    @patch.dict(os.environ, {'CURRENT_USER_TYPE': 'qwe'})
    def test_enum_non_existing_value_raises_exception(self):
        with self.assertRaises(ValueError):
            config = self.config_cls()

            _ = config.CURRENT_USER_TYPE
