from datetime import date
from typing import Callable

from .references import Monography, CollectionArticle, JournalArticle, \
    TextMultivolume, DigitalLegalAct, DigitalArticle
from .references import RefType


class ReferenceCreator:
    ref_classes = (
        Monography,
        CollectionArticle,
        JournalArticle,
        TextMultivolume,
        DigitalLegalAct,
        DigitalArticle,
    )
    ref_names = tuple(ref.cls_name_rus for ref in ref_classes)
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
        self.callbacks = {
            str: text_handler,
            int: number_handler,
            date: date_handler,
        }
        self.ref_styler = ref_styler
        self.ref_type = self.reference_types[ref_type]

    def process(self, ref_name: str):
        reference = self.references[ref_name]()
        for i, (name, attr) in enumerate(vars(reference).items()):
            callback = self.callbacks[attr.callback_type]
            val = callback(
                label=attr.invite,
                value=attr.value,
                key=str(i),
            )
            setattr(vars(reference)[name], 'value', val)
        reference.ref_type = self.ref_type
        return self.ref_styler.apply(str(reference))
