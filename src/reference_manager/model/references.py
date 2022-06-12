from __future__ import annotations

from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum
from typing import Callable

from .fields import Text, Number, Year, Date, Pages


class Reference(ABC):
    @property
    @abstractmethod
    def cls_rus(self):
        pass

    @property
    @abstractmethod
    def fields(self):
        pass

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


FieldInfo = namedtuple(
    "FieldInfo",
    field_names=("name", "invite", "type")
)


class RefType(Enum):
    Transtextual = 0
    Subscript = 1


class Monography(Reference):
    cls_rus = "Монография"

    fields = (
        FieldInfo("author", "Введите автора (-ов)", str),
        FieldInfo("year", "Введите год", int),
        FieldInfo("name", "Введите название", str),
        FieldInfo("editor", "Введите редактора (-ов)", str),
        FieldInfo("translator", "Введите переводчика (-ов)", str),
        FieldInfo("city", "Введите город", str),
        FieldInfo("publishing_house", "Введите издательство", str),
        FieldInfo("pages", "Введите количество страниц/номер страниц (-ы)", str),
    )

    author = Text()
    year = Year()
    name = Text()
    editor = Text()
    translator = Text()
    city = Text()
    publishing_house = Text()
    pages = Pages()

    def __init__(
            self,
            author: str = "Корнелиус Х.",
            year: int = 1992,
            name: str = "Выиграть может каждый: Как разрешать конфликты",
            editor: str = "Х. Корнелиус, З. Фэйр",
            translator: str = "П. Е. Патрушева",
            city: str = "М.",
            publishing_house: str = "Стрингер",
            pages: str = "116",
    ):
        self.ref_type = RefType.Transtextual
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        editor = f"{self.editor}" if self.editor else ""
        semicolon = "; " if editor else ""
        translator = f"{semicolon}пер. {self.translator}" if self.translator else ""
        backslashes = " // " if editor or translator else ""

        res_transtextual = f"{self.author} ({int(self.year)}) {self.name}" \
                           f"{backslashes}{editor}{translator}. — " \
                           f"{self.city}: {self.publishing_house}. " \
                           f"— С. {self.pages}."
        res_subscript = f"{self.author} {self.name}{backslashes}" \
                        f"{editor}{translator}. — " \
                        f"{self.city}: {self.publishing_house}, " \
                        f"{int(self.year)}. — С. {self.pages}."

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class CollectionArticle(Reference):
    cls_rus = "Статья в сборнике"

    fields = (
        FieldInfo("author", "Введите автора (-ов) статьи", str),
        FieldInfo("year", "Введите год", int),
        FieldInfo("article_name", "Введите название статьи", str),
        FieldInfo("editor", "Введите редактора (-ов) сборника", str),
        FieldInfo("collection_name", "Введите название сборника", str),
        FieldInfo("city", "Введите город", str),
        FieldInfo("publishing_house", "Введите издательство", str),
        FieldInfo("pages", "Введите диапазон страниц (через тире)", str),
    )

    author = Text()
    year = Year()
    article_name = Text()
    editor = Text()
    collection_name = Text()
    city = Text()
    publishing_house = Text()
    pages = Pages()

    def __init__(
            self,
            author: str = "Дмитриев Т. А.",
            year: int = 2009,
            article_name: str = "Антонио Грамши",
            editor: str = "В. А. Куренной",
            collection_name: str = "История и теория "
                                   "интеллигенции и интеллектуалов",
            city: str = "Москва",
            publishing_house: str = "Наследие Евразии",
            pages: str = "207-228",
    ):
        self.ref_type = RefType.Transtextual
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        res_transtextual = f"{self.author} ({int(self.year)}) " \
                           f"{self.article_name} // {self.editor} " \
                           f"(Ред.). {self.collection_name}. {self.city}:" \
                           f" {self.publishing_house}. С. {self.pages}."
        res_subscript = f"{self.author} " \
                        f"{self.article_name} // {self.editor} " \
                        f"(Ред.). {self.collection_name}. {self.city}:" \
                        f" {self.publishing_house}, {int(self.year)}. " \
                        f"С. {self.pages}."

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class JournalArticle(Reference):
    cls_rus = "Статья в журнале"

    fields = (
        FieldInfo("author", "Введите автора (-ов) статьи", str),
        FieldInfo("year", "Введите год", int),
        FieldInfo("article_name", "Введите название статьи", str),
        FieldInfo("journal_name", "Введите название журнала", str),
        FieldInfo("journal_number", "Введите номер журнала", int),
        FieldInfo("pages", "Введите диапазон страниц (через тире)", str),
    )

    author = Text()
    year = Year()
    article_name = Text()
    journal_name = Text()
    journal_number = Number()
    pages = Pages()

    def __init__(
            self,
            author: str = "Шлыков П.",
            year: int = 2011,
            article_name: str = "Турецкий национализм в XX веке: "
                                "поиски национальной идентичности",
            journal_name: str = "Вопросы национализма",
            journal_number: int = 5,
            pages: str = "135-155",
    ):
        self.ref_type = RefType.Transtextual
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        res_transtextual = f"{self.author} ({int(self.year)}) " \
                           f"{self.article_name} // {self.journal_name}." \
                           f" №{self.journal_number}. С. {self.pages}."
        res_subscript = f"{self.author} {self.article_name} // " \
                        f"{self.journal_name}. {int(self.year)}. " \
                        f"№{self.journal_number}. С. {self.pages}."

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class TextMultivolume(Reference):
    cls_rus = "Текст, опубликованный в многотомном издании"

    fields = (
        FieldInfo("author", "Введите автора (-ов) текста", str),
        FieldInfo("year", "Введите год", int),
        FieldInfo("text_name", "Введите название текста", str),
        FieldInfo("multivolume_author", "Введите автора/"
                                        "составителя тома", str),
        FieldInfo("multivolume_name", "Введите название многотомного "
                                      "издания", str),
        FieldInfo("city", "Введите город", str),
        FieldInfo("publishing_house", "Введите издательство", str),
        FieldInfo("pages", "Введите диапазон страниц (через тире)", str),
        FieldInfo("first_publication", "Введите информацию о первой "
                                       "публикации", str),
    )

    author = Text()
    year = Year()
    text_name = Text()
    multivolume_author = Text()
    multivolume_name = Text()
    city = Text()
    publishing_house = Text()
    pages = Pages()
    first_publication = Text()

    def __init__(
            self,
            author: str = "Добролюбов Н. А.",
            year: int = 1989,
            text_name: str = "Новый кодекс русской практической мудрости",
            multivolume_author: str = "П. А. Лебедев (Сост.)",
            multivolume_name: str = "Антология педагогической мысли России "
                                    "первой половины XIX в. "
                                    "(до реформ 60-х гг.)",
            city: str = "Москва",
            publishing_house: str = "Педагогика",
            pages: str = "486-498",
            first_publication: str = "Современник. 1859. № 6",
    ):
        self.ref_type = RefType.Transtextual
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        res_transtextual = f"{self.author} ({int(self.year)}) {self.text_name} " \
                           f"// {self.multivolume_author} " \
                           f"{self.multivolume_name} {self.city}: " \
                           f"{self.publishing_house}. С. {self.pages}. " \
                           f"Первая публикация: {self.first_publication}."
        res_subscript = "Пока не поддерживается :)"

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class DigitalLegalAct(Reference):
    cls_rus = "Нормативно-правовой акт, электронный ресурс"

    fields = (
        FieldInfo("name", "Введите название", str),
        FieldInfo("url", "Введите URL", str),
        FieldInfo("article", "Введите статью", str),
        FieldInfo("request_date", "Введите дату обращения", str),
    )

    name = Text()
    url = Text()
    article = Text()
    request_date = Date()

    def __init__(
            self,
            name: str = "Справочная информация «Пособие по беременности и родам"
                        " в 2019 г.»",
            url: str = "http://www.consultant.ru/law/ref/poleznye"
                       "-sovety/detskie-posobija/posobie-po-beremennosti-i-"
                       "rodam/",
            article: str = "ч. 5 ст. 123",
            request_date: str = "27.03.2019",
    ):
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        res = f"{self.name}"
        comma = ", " if self.article != "" else ""
        res += comma + f"{self.article} // {self.url} " \
                       f"(дата обращения: {self.request_date})"
        return res


class ReferenceCreator:
    ref_classes = (
        Monography,
        CollectionArticle,
        JournalArticle,
        TextMultivolume,
        DigitalLegalAct,
    )
    ref_names = tuple(ref.cls_rus for ref in ref_classes)
    references = dict(zip(ref_names, ref_classes))

    reference_types = {
        "Затекстовая": RefType.Transtextual,
        "Подстрочная": RefType.Subscript
    }

    def __init__(
            self,
            ref_type: str,
            text_handler: Callable, number_handler: Callable,
            ref_styler=None,
    ):
        self.text_handler = text_handler
        self.number_handler = number_handler
        self.ref_styler = ref_styler
        self.ref_type = self.reference_types[ref_type]

    def process(self, ref_name: str):
        reference = self.references[ref_name]()
        for i, field in enumerate(reference.fields):
            if field.type == int:
                val = self.number_handler(
                    label=field.invite,
                    value=getattr(reference, field.name),
                    key=str(i)
                )
            else:
                val = self.text_handler(
                    label=field.invite,
                    value=getattr(reference, field.name),
                    key=str(i)
                )
            setattr(reference, field.name, val)
        reference.ref_type = self.ref_type
        return self.ref_styler.apply(str(reference))
