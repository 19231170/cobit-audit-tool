import customtkinter as ctk
from typing import Callable, Optional
from app.themes.config import RATING_COLORS, ThemeConfig

class RatingSelectorWidget(ctk.CTkFrame):
    def __init__(self, master, current_rating: Optional[str] = None, 
                 on_change: Optional[Callable[[str], None]] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_change = on_change
        self.buttons = {}
        self.current_rating = current_rating

        ratings = [
            ("N", "N (0-15%)"),
            ("P", "P (15-50%)"),
            ("L", "L (50-85%)"),
            ("F", "F (85-100%)"),
        ]

        for code, label in ratings:
            btn = ctk.CTkButton(
                self, text=label, width=90, height=32, font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=RATING_COLORS[code] if current_rating == code else ThemeConfig.SECONDARY,
                hover_color=RATING_COLORS[code],
                command=lambda c=code: self._set_rating(c)
            )
            btn.pack(side="left", padx=4)
            self.buttons[code] = btn

    def _set_rating(self, code: str):
        self.current_rating = code
        for c, btn in self.buttons.items():
            if c == code:
                btn.configure(fg_color=RATING_COLORS[c], text_color="white")
            else:
                btn.configure(fg_color=ThemeConfig.SECONDARY, text_color=ThemeConfig.TEXT_LIGHT)
        if self.on_change:
            self.on_change(code)
