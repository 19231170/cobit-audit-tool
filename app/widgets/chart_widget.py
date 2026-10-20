import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from typing import List, Optional

def generate_radar_chart(labels: List[str], actuals: List[float], targets: List[float], save_path: Optional[str] = None):
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    actual_vals = actuals + actuals[:1]
    target_vals = targets + targets[:1]

    fig, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(polar=True), facecolor="#1A2332")
    ax.set_facecolor("#1A2332")

    # Plot Target
    ax.plot(angles, target_vals, color="#F59E0B", linewidth=1.8, linestyle="dashed", label="Target")
    ax.fill(angles, target_vals, color="#F59E0B", alpha=0.1)

    # Plot Actual
    ax.plot(angles, actual_vals, color="#1E90FF", linewidth=2.2, label="Aktual")
    ax.fill(angles, actual_vals, color="#1E90FF", alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color="#E2E8F0", size=10, weight="bold")
    ax.spines['polar'].set_color('#2A3644')
    ax.grid(color='#2A3644', linestyle=':')

    plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.15), facecolor="#1A2332", edgecolor="#2A3644", labelcolor="#E2E8F0")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    return fig

def generate_bar_chart(codes: List[str], actuals: List[int], targets: List[int], save_path: Optional[str] = None):
    x = np.arange(len(codes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#1A2332")
    ax.set_facecolor("#1A2332")

    ax.bar(x - width/2, actuals, width, label='Aktual', color='#1E90FF')
    ax.bar(x + width/2, targets, width, label='Target', color='#F59E0B', alpha=0.85)

    ax.set_ylabel('Capability Level (0-5)', color='#E2E8F0')
    ax.set_xticks(x)
    ax.set_xticklabels(codes, color='#E2E8F0', rotation=30, ha='right')
    ax.tick_params(colors='#E2E8F0')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#2A3644')
    ax.spines['bottom'].set_color('#2A3644')
    ax.grid(axis='y', color='#2A3644', linestyle=':')
    ax.legend(facecolor="#1A2332", edgecolor="#2A3644", labelcolor="#E2E8F0")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    return fig

class EmbeddedChartWidget(ctk.CTkFrame):
    def __init__(self, master, fig, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
