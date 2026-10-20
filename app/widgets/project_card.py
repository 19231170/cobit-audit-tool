import customtkinter as ctk
from typing import Callable
from app.core.models import Project
from app.themes.config import ThemeConfig

class ProjectCardWidget(ctk.CTkFrame):
    def __init__(self, master, project: Project, progress: float, on_open: Callable[[int], None], **kwargs):
        super().__init__(master, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=12, **kwargs)
        self.project = project

        title = ctk.CTkLabel(
            self, text=project.name, font=ctk.CTkFont(size=16, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT, anchor="w"
        )
        title.pack(fill="x", padx=16, pady=(16, 4))

        badge = ctk.CTkLabel(
            self, text=f"Framework: {project.cobit_version}", font=ctk.CTkFont(size=12),
            text_color=ThemeConfig.PRIMARY, anchor="w"
        )
        badge.pack(fill="x", padx=16, pady=(0, 10))

        prog_bar = ctk.CTkProgressBar(self, progress_color=ThemeConfig.PRIMARY, height=8)
        prog_bar.set(max(0.0, min(1.0, progress)))
        prog_bar.pack(fill="x", padx=16, pady=4)

        prog_txt = ctk.CTkLabel(
            self, text=f"Progress: {int(progress * 100)}%", font=ctk.CTkFont(size=11),
            text_color=ThemeConfig.TEXT_MUTED, anchor="w"
        )
        prog_txt.pack(fill="x", padx=16, pady=(0, 12))

        btn = ctk.CTkButton(
            self, text="Buka Audit →", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER,
            command=lambda: on_open(project.id)
        )
        btn.pack(fill="x", padx=16, pady=(0, 16))
