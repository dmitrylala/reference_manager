from abc import ABC, abstractmethod
from enum import Enum

from .fields import TextField, NumberField, Author, Year, Name, Editor, \
    Translator, City, PublishingHouse, Pages, Url, RequestDate


class RefType(Enum):
    Transtextual = 0
    Subscript = 1


class Reference(ABC):
    @property
    @abstractmethod
    def cls_name_rus(self):
        pass

    ref_type = RefType.Transtextual

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Monography(Reference):
    cls_name_rus = "Монография"

    def __init__(self):
        self.author = Author("Корнелиус Х.")
        self.year = Year(1992)
        self.name = Name("Выиграть может каждый: Как разрешать конфликты")
        self.editor = Editor("Х. Корнелиус, З. Фэйр")
        self.translator = Translator("П. Е. Патрушева")
        self.city = City("М.")
        self.publishing_house = PublishingHouse("Стрингер")
        self.pages = Pages("116", invite="Введите количество страниц/номер страниц (-ы)")
        self.url = Url("http://www.philosophy.ru/library/bahtin/rable.html#_ftn1")
        self.request_date = RequestDate()

    def __str__(self):
        editor = f"{self.editor}" if self.editor else ""
        semicolon = "; " if editor else ""
        translator = f"{semicolon}пер. {self.translator}" if self.translator else ""
        backslashes = " // " if editor or translator else ""

        url = ""
        if self.url and self.request_date:
            url = f" [Электронный ресурс]. URL: {self.url} " \
                  f"(дата обращения: {self.request_date})"
        pages = f"— С. {self.pages}." if self.pages else ""

        res_transtextual = f"{self.author} ({self.year}) {self.name}" \
                           f"{backslashes}{editor}{translator}. — " \
                           f"{self.city}: {self.publishing_house}. " \
                           f"{pages}{url}"
        res_subscript = f"{self.author} {self.name}{backslashes}" \
                        f"{editor}{translator}. — " \
                        f"{self.city}: {self.publishing_house}, " \
                        f"{self.year}. {pages}{url}"

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class CollectionArticle(Reference):
    cls_name_rus = "Статья в сборнике"

    def __init__(self):
        self.author = Author("Дмитриев Т. А.", invite="Введите автора (-ов) статьи")
        self.year = Year(2009)
        self.article_name = Name("Антонио Грамши", invite="Введите название статьи")
        self.editor = Editor("В. А. Куренной", invite="Введите редактора (-ов) сборника")
        self.collection_name = Name(
            "История и теория интеллигенции и интеллектуалов",
            invite="Введите название сборника"
        )
        self.city = City("М.")
        self.publishing_house = PublishingHouse("Наследие Евразии")
        self.pages = Pages("207-228")

    def __str__(self):
        pages = f"— С. {self.pages}." if self.pages else ""
        res_transtextual = f"{self.author} ({self.year}) " \
                           f"{self.article_name} // {self.editor} " \
                           f"(Ред.). {self.collection_name}. {self.city}:" \
                           f" {self.publishing_house}. {pages}"
        res_subscript = f"{self.author} " \
                        f"{self.article_name} // {self.editor} " \
                        f"(Ред.). {self.collection_name}. {self.city}:" \
                        f" {self.publishing_house}, {self.year}" \
                        f". {pages}"

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class JournalArticle(Reference):
    cls_name_rus = "Статья в журнале"

    def __init__(self):
        self.author = Author("Шлыков П.", invite="Введите автора (-ов) статьи")
        self.year = Year(2011)
        self.article_name = Name(
            "Турецкий национализм в XX веке: поиски национальной идентичности",
            invite="Введите название статьи"
        )
        self.journal_name = Name(
            "Вопросы национализма",
            invite="Введите название журнала"
        )
        self.journal_number = NumberField(5, invite="Введите номер журнала")
        self.pages = Pages("135-155")
        self.url = Url("https://istina.msu.ru/publications/article/583756/")
        self.request_date = RequestDate()

    def __str__(self):
        pages = f"— С. {self.pages}." if self.pages else ""
        url = ""
        if self.url and self.request_date:
            url = f" [Электронный ресурс]. URL: {self.url} " \
                  f"(дата обращения: {self.request_date})"
        res_transtextual = f"{self.author} ({self.year}) " \
                           f"{self.article_name} // {self.journal_name}." \
                           f" №{self.journal_number}. {pages}{url}"
        res_subscript = f"{self.author} {self.article_name} // " \
                        f"{self.journal_name}, {self.year}. " \
                        f"№{self.journal_number}. {pages}{url}"

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class TextMultivolume(Reference):
    cls_name_rus = "Текст, опубликованный в многотомном издании"

    def __init__(self):
        self.author = Author(
            "Добролюбов Н. А.",
            invite="Введите автора (-ов) текста"
        )
        self.year = Year(1989)
        self.text_name = TextField(
            "Новый кодекс русской практической мудрости",
            invite="Введите название текста"
        )
        self.multivolume_author = Author(
            "П. А. Лебедев (Сост.)",
            invite="Введите автора/составителя тома"
        )
        self.multivolume_name = Name(
            "Антология педагогической мысли России первой половины XIX в. "
            "(до реформ 60-х гг.)",
            invite="Введите название многотомного издания"
        )
        self.city = City("М.")
        self.publishing_house = PublishingHouse("Педагогика")
        self.pages = Pages("486-498")
        self.first_publication = TextField(
            "Современник. 1859. № 6",
            invite="Введите информацию о первой публикации"
        )

    def __str__(self):
        pages = f"— С. {self.pages}." if self.pages else ""
        res_transtextual = f"{self.author} ({self.year}) {self.text_name} " \
                           f"// {self.multivolume_author} " \
                           f"{self.multivolume_name} {self.city}: " \
                           f"{self.publishing_house}. {pages} " \
                           f"Первая публикация: {self.first_publication}."
        res_subscript = f"{self.author} {self.text_name} " \
                        f"// {self.multivolume_author} " \
                        f"{self.multivolume_name} {self.city}: " \
                        f"{self.publishing_house}, {self.year}. {pages} " \
                        f"Первая публикация: {self.first_publication}."

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript


class DigitalLegalAct(Reference):
    cls_name_rus = "Нормативно-правовой акт, электронный ресурс"

    def __init__(self):
        self.name = Name("Федеральный закон «О воинской обязанности и "
                         "военной службе» от 28.03.1998 N 53-ФЗ")
        self.url = Url("http://www.consultant.ru/document/cons_doc_LAW_18260/"
                       "fbe9593051ae34e2a8eb27f73b923ffee40296b7/")
        self.article = TextField(
            "ч. 1 ст. 24",
            invite="Введите статью",
            optional=True
        )
        self.request_date = RequestDate()

    def __str__(self):
        res = f"{self.name}"
        comma = ", " if self.article else ""
        res += comma + f"{self.article} // {self.url} " \
                       f"(дата обращения: {self.request_date})"
        return res


class DigitalArticle(Reference):
    cls_name_rus = "Online-статья"

    def __init__(self):
        self.author = Author("Инна Деготькова, Маргарита Мордовина")
        self.year = Year(2021)
        self.article_name = Name(
            "Доходы экспортеров ушли под контроль правительства",
            invite="Введите название статьи"
        )
        self.resource_name = Name(
            "Газета РБК",
            invite="Введите название ресурса"
        )
        self.article_number = NumberField(77, invite="Введите номер статьи")
        self.url = Url("https://www.rbc.ru/newspaper/2022/06/10/"
                       "62a201e69a79478f6aa4c51c")
        self.request_date = RequestDate()

    def __str__(self):
        article_num = f" № {self.article_number}." if self.article_number else ""
        res_transtextual = f"{self.author} ({self.year}) " \
                           f"{self.article_name} " \
                           f"// {self.resource_name}.{article_num} " \
                           f"URL: {self.url} (дата обращения: {self.request_date})"
        res_subscript = f"{self.author}. {self.article_name} " \
                        f"// {self.resource_name}. {self.year}.{article_num} " \
                        f"URL: {self.url} (дата обращения: {self.request_date})"

        if self.ref_type == RefType.Transtextual:
            return res_transtextual
        return res_subscript
