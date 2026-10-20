import os
import sys
import customtkinter as ctk
from app.core.database import DatabaseManager
from app.core.seeds import seed_default_cobit_data
from app.widgets.sidebar import SidebarWidget
from app.modules.dashboard import DashboardView
from app.modules.goal_cascade import GoalCascadeView
from app.modules.raci import RaciView
from app.modules.assessment import AssessmentView
from app.modules.findings import FindingsView
from app.modules.reports import ReportsView
from app.themes.config import ThemeConfig

class CobitAuditApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("COBIT Audit Tool - ISO/IEC 15504 Assessment")
        self.geometry("1180x760")
        self.minsize(1024, 700)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Database Setup
        app_dir = os.path.join(os.path.expanduser("~"), ".cobit_audit_tool")
        os.makedirs(app_dir, exist_ok=True)
        db_path = os.path.join(app_dir, "cobit_audit.db")

        is_new_db = not os.path.exists(db_path)
        self.db = DatabaseManager(db_path)
        self.db.initialize()
        if is_new_db:
            seed_default_cobit_data(self.db)

        self.current_project_id = None
        projects = self.db.get_projects()
        if projects:
            self.current_project_id = projects[0].id

        self._build_layout()
        self.show_module("dashboard")

    def _build_layout(self):
        self.sidebar = SidebarWidget(self, on_navigate=self.show_module)
        self.sidebar.pack(side="left", fill="y")

        self.content_area = ctk.CTkFrame(self, fg_color=ThemeConfig.BG_DARK, corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True)

    def show_module(self, module_id: str):
        for w in self.content_area.winfo_children():
            w.destroy()

        if module_id == "dashboard":
            view = DashboardView(self.content_area, self.db, on_open_project=self._open_project)
            view.pack(fill="both", expand=True)
        elif not self.current_project_id:
            # Need a project
            msg = ctk.CTkLabel(
                self.content_area, text="Silakan pilih atau buat proyek audit terlebih dahulu di Dashboard.",
                font=ctk.CTkFont(size=15), text_color=ThemeConfig.TEXT_MUTED
            )
            msg.pack(pady=50)
        elif module_id == "goal_cascade":
            view = GoalCascadeView(self.content_area, self.db, self.current_project_id, on_saved=self._update_progress)
            view.pack(fill="both", expand=True)
        elif module_id == "raci":
            view = RaciView(self.content_area, self.db, self.current_project_id)
            view.pack(fill="both", expand=True)
        elif module_id == "assessment":
            view = AssessmentView(self.content_area, self.db, self.current_project_id, on_updated=self._update_progress)
            view.pack(fill="both", expand=True)
        elif module_id == "findings":
            view = FindingsView(self.content_area, self.db, self.current_project_id)
            view.pack(fill="both", expand=True)
        elif module_id == "reports":
            view = ReportsView(self.content_area, self.db, self.current_project_id)
            view.pack(fill="both", expand=True)

        self._update_progress()

    def _open_project(self, project_id: int):
        self.current_project_id = project_id
        self.show_module("goal_cascade")

    def _update_progress(self):
        if not self.current_project_id:
            self.sidebar.update_progress(0.0)
            return

        procs = self.db.get_project_processes(self.current_project_id)
        if not procs:
            self.sidebar.update_progress(0.1)  # Just started
            return

        done = sum(1 for p in procs if self.db.get_assessments(self.current_project_id, p["process_id"]))
        ratio = done / len(procs)
        self.sidebar.update_progress(ratio)

if __name__ == "__main__":
    app = CobitAuditApp()
    app.mainloop()
