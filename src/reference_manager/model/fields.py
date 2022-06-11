from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def validate(self, value):
        try:
            int(value)
        except ValueError:
            raise TypeError(f"Not an integer: {value}")


class Year(Number):
    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError(f"Not a year: {value}")


class Text(Validator):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Not a text: {value}")


class Pages(Text):
    def validate(self, value):
        super().validate(value)

        count_hyphen = value.count('-')
        if count_hyphen >= 2:
            raise ValueError(f"Too many '-' symbols: {count_hyphen}")
        elif count_hyphen == 1:
            try:
                page_start, page_end = map(int, map(str.strip, value.split('-')))
            except ValueError:
                raise ValueError(f"Bad page range: {value}")

            if page_start >= page_end:
                raise ValueError(f"Start page >= end page: {page_start}")
        else:
            try:
                int(value.strip())
            except ValueError:
                raise ValueError(f"Bad page: {value}")


class Date(Text):
    def validate(self, value):
        super().validate(value)

        sep = '.'

        count_dots = value.count(sep)
        if count_dots != 2:
            raise ValueError(f"Number of symbols {sep} "
                             f"doesn't equal to 2: {count_dots}")

        try:
            day, month, year = map(int, map(str.strip, value.split(sep)))
        except ValueError:
            raise ValueError(f"Bad date: {value}")

        if day not in range(1, 32):
            raise ValueError(f"day is not from 1 to 31: {day}")

        if month not in range(1, 13):
            raise ValueError(f"month is not from 1 to 12: {month}")

        if year <= 0:
            raise ValueError(f"Bad year: {year}")



