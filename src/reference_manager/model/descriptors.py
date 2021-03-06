from abc import ABC, abstractmethod


class BaseDescriptor(ABC):
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


class Number(BaseDescriptor):
    def validate(self, value):
        try:
            int(value)
        except ValueError:
            raise TypeError(f"Not an integer: {value}")


class PositiveNumber(Number):
    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError(f"Not a positive number: {value}")


class Text(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Not a text: {value}")


class NumbersHyphen(Text):
    def validate(self, value):
        super().validate(value)

        if value == "":
            return

        count_hyphen = value.count('-')
        if count_hyphen >= 2:
            raise ValueError(f"Too many '-' symbols: {count_hyphen}")
        elif count_hyphen == 1:
            try:
                page_start, page_end = map(
                    lambda x: int(x.strip()),
                    value.split('-')
                )
            except ValueError:
                raise ValueError(f"Bad page range: {value}")

            if page_start >= page_end:
                raise ValueError(f"Start page >= end page: {page_start}")

            return

        try:
            int(value.strip())
        except ValueError:
            raise ValueError(f"Bad page: {value}")
