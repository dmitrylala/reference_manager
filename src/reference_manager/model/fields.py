from dataclasses import dataclass, field
from datetime import date

from .descriptors import NumbersHyphen, PositiveNumber

# format for datetime.date output
DATE_FORMAT = "%d.%m.%y"

# -----------------------------------------------
#               Fields base classes
# -----------------------------------------------


@dataclass
class TextField:
    value: str
    invite: str
    callback_type: object = str
    optional: bool = False

    def __str__(self):
        return self.value

    def __bool__(self):
        return self.value != ""


@dataclass
class NumberField:
    value: int
    invite: str
    callback_type: object = int
    optional: bool = False

    def __str__(self):
        return str(int(self.value))


@dataclass
class DateField:
    value: date
    invite: str
    callback_type: object = date
    optional: bool = False

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


# ----------------------------------
#               Fields
# ----------------------------------


@dataclass
class Author(TextField):
    invite: str = "Введите автора (-ов)"


@dataclass
class Year(NumberField):
    value: int = field(default=PositiveNumber())
    invite: str = "Введите год"


@dataclass
class Name(TextField):
    invite: str = "Введите название"


@dataclass
class Editor(TextField):
    invite: str = "Введите редактора (-ов)"
    optional: bool = True


@dataclass
class Translator(TextField):
    invite: str = "Введите переводчика (-ов)"
    optional: bool = True


@dataclass
class City(TextField):
    invite: str = "Введите город"


@dataclass
class PublishingHouse(TextField):
    invite: str = "Введите издательство"


@dataclass
class Pages(TextField):
    value: str = field(default=NumbersHyphen())
    invite: str = "Введите диапазон страниц (через тире)"
    optional: bool = True


@dataclass
class Url(TextField):
    invite: str = "Введите URL"


@dataclass
class RequestDate(DateField):
    value: date = date.today()
    invite: str = "Введите дату обращения"
