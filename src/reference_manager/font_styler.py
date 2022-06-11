from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Font:
    style: str = "normal"
    family: str = "Times New Roman"
    size: int = 14
    color: str = "white"


class FontStyler:
    def __init__(self, font: Font | None = None) -> None:
        self.font = font if font is not None else Font()

    def apply(self, text) -> str:
        return f'''
            <p style="
                color: {self.font.color};
                font-style: {self.font.style};
                font-family: {self.font.family}; 
                font-size: {self.font.size}px;
            ">{text}</p>
        '''
