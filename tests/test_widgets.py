import pytest
from app.themes.config import ThemeConfig, RATING_COLORS

def test_theme_config():
    assert ThemeConfig.PRIMARY == "#1E90FF"
    assert ThemeConfig.BG_DARK == "#121820"
    assert ThemeConfig.SIDEBAR_WIDTH == 230

def test_rating_colors():
    assert "F" in RATING_COLORS
    assert "L" in RATING_COLORS
    assert "P" in RATING_COLORS
    assert "N" in RATING_COLORS
