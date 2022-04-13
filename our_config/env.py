import os
from enum import Enum


class EnvironmentVar:
    name: str
    optional: bool
    default_value: object

    def __init__(self, *, optional=False, default_value=None):
        self.optional = optional
        self.default_value = default_value

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        assert instance is not None
        if not self.optional and self.name not in os.environ:
            raise ValueError(f'{self.name} is undefined')

        return os.environ.get(self.name, self.default_value)

    def __set__(self, instance, value):
        raise ValueError(f'{self.name} is trying to be re-defined')

    def __delete__(self, instance):
        raise ValueError(f'{self.name} is trying to be deleted')


class IntVar(EnvironmentVar):
    def __get__(self, instance, owner):
        value = super().__get__(instance, owner)
        return int(value)


class StrVar(EnvironmentVar):
    pass


class EnumVar(EnvironmentVar):
    enum_cls: Enum

    def __init__(self, *, enum_cls, **kwargs):
        super().__init__(**kwargs)
        self.enum_cls = enum_cls

    def __get__(self, instance, owner):
        value = super().__get__(instance, owner)
        return self.enum_cls(value)
