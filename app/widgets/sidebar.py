import customtkinter as ctk
from typing import Callable
from app.themes.config import ThemeConfig

class SidebarWidget(ctk.CTkFrame):
    def __init__(self, master, on_navigate: Callable[[str], None], **kwargs):
        super().__init__(master, width=ThemeConfig.SIDEBAR_WIDTH, corner_radius=0, 
                         fg_color=ThemeConfig.SIDEBAR_BG_DARK, **kwargs)
        self.on_navigate = on_navigate
        self.buttons = {}
        
        # Logo / Brand
        title_label = ctk.CTkLabel(
            self, text="COBIT AUDIT", font=ctk.CTkFont(family=ThemeConfig.FONT_FAMILY, size=20, weight="bold"),
            text_color=ThemeConfig.PRIMARY
        )
        title_label.pack(pady=(25, 20), padx=20, anchor="w")

        modules = [
            ("dashboard", "📊 Dashboard"),
            ("goal_cascade", "🎯 Goal Cascade"),
            ("raci", "👥 RACI Chart"),
            ("assessment", "📋 Assessment"),
            ("findings", "🔍 Temuan & Gap"),
            ("reports", "📈 Laporan & PDF"),
        ]

        for mod_id, label in modules:
            btn = ctk.CTkButton(
                self, text=label, font=ctk.CTkFont(size=14),
                fg_color="transparent", hover_color=ThemeConfig.SECONDARY,
                anchor="w", height=40,
                command=lambda m=mod_id: self._select_nav(m)
            )
            btn.pack(fill="x", padx=12, pady=4)
            self.buttons[mod_id] = btn

        # Progress Section
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(side="bottom", fill="x", padx=16, pady=20)

        self.progress_label = ctk.CTkLabel(
            self.progress_frame, text="Progress Audit: 0%", font=ctk.CTkFont(size=12),
            text_color=ThemeConfig.TEXT_MUTED
        )
        self.progress_label.pack(anchor="w", pady=(0, 4))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=ThemeConfig.PRIMARY)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x")

    def _select_nav(self, module_id: str):
        for mid, btn in self.buttons.items():
            if mid == module_id:
                btn.configure(fg_color=ThemeConfig.PRIMARY, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=ThemeConfig.TEXT_LIGHT)
        self.on_navigate(module_id)

    def update_progress(self, percentage: float):
        clamped = max(0.0, min(1.0, percentage))
        self.progress_bar.set(clamped)
        self.progress_label.configure(text=f"Progress Audit: {int(clamped * 100)}%")
