from __future__ import annotations

from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import date
from enum import Enum
from typing import Callable

from .fields import Text, PositiveNumber, Pages


DATE_FORMAT = "%d.%m.%y"


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
        FieldInfo("editor", "Введите редактора (-ов) (опционально)", str),
        FieldInfo("translator", "Введите переводчика (-ов) (опционально)", str),
        FieldInfo("city", "Введите город", str),
        FieldInfo("publishing_house", "Введите издательство", str),
        FieldInfo("pages", "Введите количество страниц/номер страниц (-ы) (опционально)", str),
        FieldInfo("url", "Введите URL (опционально - отображается только "
                         "если еще введена дата обращения)", str),
        FieldInfo("request_date", "Введите дату обращения (опционально)", date),
    )

    year = PositiveNumber()
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
            url: str = "http://www.philosophy.ru/library/bahtin/"
                       "rable.html#_ftn1",
            request_date: date = date.today(),
    ):
        self.author = author
        self.year = year
        self.name = name
        self.editor = editor
        self.translator = translator
        self.city = city
        self.publishing_house = publishing_house
        self.pages = pages
        self.url = url
        self.ref_type = RefType.Transtextual
        self.request_date = request_date

    def __str__(self):
        editor = f"{self.editor}" if self.editor else ""
        semicolon = "; " if editor else ""
        translator = f"{semicolon}пер. {self.translator}" if self.translator else ""
        backslashes = " // " if editor or translator else ""

        url = ""
        if self.url and self.request_date:
            url = f" [Электронный ресурс]. URL: {self.url} " \
                  f"(дата обращения: {self.request_date.strftime(DATE_FORMAT)})"
        pages = f"— С. {self.pages}." if self.pages else ""

        res_transtextual = f"{self.author} ({int(self.year)}) {self.name}" \
                           f"{backslashes}{editor}{translator}. — " \
                           f"{self.city}: {self.publishing_house}. " \
                           f"{pages}{url}"
        res_subscript = f"{self.author} {self.name}{backslashes}" \
                        f"{editor}{translator}. — " \
                        f"{self.city}: {self.publishing_house}, " \
                        f"{int(self.year)}. {pages}{url}"

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
        FieldInfo("pages", "Введите диапазон страниц (через тире) (опционально)", str),
    )

    author = Text()
    year = PositiveNumber()
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
        pages = f"— С. {self.pages}." if self.pages else ""
        res_transtextual = f"{self.author} ({int(self.year)}) " \
                           f"{self.article_name} // {self.editor} " \
                           f"(Ред.). {self.collection_name}. {self.city}:" \
                           f" {self.publishing_house}. {pages}"
        res_subscript = f"{self.author} " \
                        f"{self.article_name} // {self.editor} " \
                        f"(Ред.). {self.collection_name}. {self.city}:" \
                        f" {self.publishing_house}, {int(self.year)}" \
                        f". {pages}"

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
        FieldInfo("pages", "Введите диапазон страниц (через тире) (опционально)", str),
        FieldInfo("url", "Введите URL (опционально - отображается только "
                         "если еще введена дата обращения)", str),
        FieldInfo("request_date", "Введите дату обращения (опционально)", date),
    )

    author = Text()
    year = PositiveNumber()
    article_name = Text()
    journal_name = Text()
    journal_number = PositiveNumber()
    pages = Pages()
    url = Text()

    def __init__(
            self,
            author: str = "Шлыков П.",
            year: int = 2011,
            article_name: str = "Турецкий национализм в XX веке: "
                                "поиски национальной идентичности",
            journal_name: str = "Вопросы национализма",
            journal_number: int = 5,
            pages: str = "135-155",
            url: str = "https://istina.msu.ru/publications/article/583756/",
            request_date: date = date.today(),
    ):
        self.ref_type = RefType.Transtextual
        self.request_date = request_date
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        pages = f"— С. {self.pages}." if self.pages else ""
        url = ""
        if self.url and self.request_date:
            url = f" [Электронный ресурс]. URL: {self.url} " \
                  f"(дата обращения: {self.request_date.strftime(DATE_FORMAT)})"
        res_transtextual = f"{self.author} ({int(self.year)}) " \
                           f"{self.article_name} // {self.journal_name}." \
                           f" №{int(self.journal_number)}. {pages}{url}"
        res_subscript = f"{self.author} {self.article_name} // " \
                        f"{self.journal_name}, {int(self.year)}. " \
                        f"№{int(self.journal_number)}. {pages}{url}"

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
        FieldInfo("pages", "Введите диапазон страниц (через тире) (опционально)", str),
        FieldInfo("first_publication", "Введите информацию о первой "
                                       "публикации", str),
    )

    author = Text()
    year = PositiveNumber()
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
        pages = f"— С. {self.pages}." if self.pages else ""
        res_transtextual = f"{self.author} ({int(self.year)}) {self.text_name} " \
                           f"// {self.multivolume_author} " \
                           f"{self.multivolume_name} {self.city}: " \
                           f"{self.publishing_house}. {pages} " \
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
        FieldInfo("request_date", "Введите дату обращения", date),
    )

    name = Text()
    url = Text()
    article = Text()

    def __init__(
            self,
            name: str = "Федеральный закон «О воинской обязанности и "
                        "военной службе» от 28.03.1998 N 53-ФЗ",
            url: str = "http://www.consultant.ru/document/cons_doc_LAW_18260/"
                       "fbe9593051ae34e2a8eb27f73b923ffee40296b7/",
            article: str = "ч. 1 ст. 24",
            request_date: date = date.today(),
    ):
        self.ref_type = RefType.Transtextual
        self.request_date = request_date
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        res = f"{self.name}"
        comma = ", " if self.article != "" else ""
        res += comma + f"{self.article} // {self.url} " \
                       f"(дата обращения: {self.request_date.strftime(DATE_FORMAT)})"
        return res


class DigitalArticle(Reference):
    cls_rus = "Online-статья"

    fields = (
        FieldInfo("author", "Введите автора (-ов)", str),
        FieldInfo("year", "Введите год публикации статьи", int),
        FieldInfo("article_name", "Введите название статьи", str),
        FieldInfo("resource_name", "Введите название газеты/портала и т.д.", str),
        FieldInfo("article_number", "Введите номер статьи (опционально)", int),
        FieldInfo("url", "Введите URL", str),
        FieldInfo("request_date", "Введите дату обращения", date),
    )

    author = Text()
    year = PositiveNumber()
    article_name = Text()
    resource_name = Text()
    article_number = PositiveNumber()
    url = Text()

    def __init__(
            self,
            author: str = "Инна Деготькова, Маргарита Мордовина",
            year: int = 2021,
            article_name: str = "Доходы экспортеров ушли под "
                                "контроль правительства",
            resource_name: str = "Газета РБК",
            article_number: int = 77,
            url: str = "https://www.rbc.ru/newspaper/2022/06/10/"
                       "62a201e69a79478f6aa4c51c",
            request_date: date = date.today(),
    ):
        self.ref_type = RefType.Transtextual
        self.request_date = request_date
        for field, value in filter(lambda x: x[0] != 'self', locals().items()):
            setattr(self, field, value)

    def __str__(self):
        article_num = f" № {self.article_number}." if self.article_number else ""
        req_date = self.request_date.strftime(DATE_FORMAT)
        res_transtextual = f"{self.author} ({int(self.year)}) " \
                           f"{self.article_name} " \
                           f"// {self.resource_name}.{article_num} " \
                           f"URL: {self.url} (дата обращения: {req_date})"
        res_subscript = f"{self.author}. {self.article_name} " \
                        f"// {self.resource_name}. {int(self.year)}.{article_num} " \
                        f"URL: {self.url} (дата обращения: {req_date})"

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class ReferenceCreator:
    ref_classes = (
        Monography,
        CollectionArticle,
        JournalArticle,
        TextMultivolume,
        DigitalLegalAct,
        DigitalArticle,
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
            text_handler: Callable,
            number_handler: Callable,
            date_handler: Callable,
            ref_styler=None,
    ):
        self.text_handler = text_handler
        self.number_handler = number_handler
        self.date_handler = date_handler
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
            elif field.type == str:
                val = self.text_handler(
                    label=field.invite,
                    value=getattr(reference, field.name),
                    key=str(i)
                )
            else:
                val = self.date_handler(
                    label=field.invite,
                    value=getattr(reference, field.name),
                    key=str(i)
                )
            setattr(reference, field.name, val)
        reference.ref_type = self.ref_type
        return self.ref_styler.apply(str(reference))
