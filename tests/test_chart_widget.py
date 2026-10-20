import os
import pytest
from app.widgets.chart_widget import generate_radar_chart, generate_bar_chart

def test_generate_radar_chart(tmp_path):
    labels = ["EDM", "APO", "BAI", "DSS", "MEA"]
    actuals = [2.0, 3.0, 1.5, 2.5, 3.0]
    targets = [3.0, 3.0, 3.0, 3.0, 3.0]
    
    out_file = str(tmp_path / "radar.png")
    fig = generate_radar_chart(labels, actuals, targets, out_file)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 1000

def test_generate_bar_chart(tmp_path):
    codes = ["EDM01", "APO01", "APO12", "DSS05"]
    actuals = [2, 3, 1, 1]
    targets = [3, 3, 3, 3]
    
    out_file = str(tmp_path / "bar.png")
    fig = generate_bar_chart(codes, actuals, targets, out_file)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 1000
