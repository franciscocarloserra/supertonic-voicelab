"""Playwright screenshot of the panel (sets a few sliders first). Output: docs/screenshot.png"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
P = json.load(open(Path(__file__).resolve().parent.parent / "params.json"))["panel"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome"); pg = b.new_page(viewport={"width": 820, "height": 900}, device_scale_factor=2)
    pg.goto(f"http://localhost:{P['port']}"); pg.wait_for_selector("[data-a]"); pg.wait_for_timeout(300)
    pg.select_option("#target", "M5"); pg.evaluate("()=>{pt.value=0.75;ptv.textContent='0.75'}")
    for a, v in {"gender": -1.5, "mix_age": 1.5, "mix_deep": 2, "speed_dp_only": 0.5}.items():
        pg.evaluate(f"()=>{{const e=document.querySelector('[data-a={a}]');e.value={v};e.nextElementSibling.textContent='{v}'}}")
    pg.evaluate("()=>render()"); pg.wait_for_function("()=>document.getElementById('au').src.length>1000", timeout=120000); pg.wait_for_timeout(500)
    pg.screenshot(path=str(Path(__file__).resolve().parent.parent / "docs" / "screenshot.png"), full_page=True); b.close(); print("ok")
