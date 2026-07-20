pip install playwright
import subprocess 
subprocess.run(["playwright", "install"])
"""
Stage 0 — Screenshot capture.

Takes a URL, loads it in a headless browser, and saves a full-page (or
viewport) screenshot to disk. Used both by the manual collection script
and by the live demo app.

Usage:
    python src/capture.py https://example.com --out data/screenshots/example.png
"""
import argparse
import os
import time
from pathlib import Path
import sys 
import asyncio 

from playwright.async_api import async_playwright


async def capture_screenshot(
    url: str,
    out_path: str,
    viewport_only: bool = True,
    width: int = 1440,
    height: int = 1024,
    wait_ms: int = 2000,
) -> str:

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p: 
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(wait_ms / 1000) 
        await page.screenshot(path=out_path, full_page=not viewport_only)
        await browser.close()

    return out_path


async def batch_capture(url_list_path: str, out_dir: str) -> list[str]:

    saved = []
    with open(url_list_path) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for i, url in enumerate(urls):
        safe_name = url.replace("https://", "").replace("http://", "")
        safe_name = safe_name.replace("/", "_").replace(":", "_")[:80]
        out_path = os.path.join(out_dir, f"{i:03d}_{safe_name}.png")
        try:
            await capture_screenshot(url, out_path) 
            saved.append(out_path)
            print(f"[ok] {url} -> {out_path}")
        except Exception as e:
            print(f"[fail] {url}: {e}")

    return saved


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Single URL to capture")
    parser.add_argument("--out", default="data/screenshots/capture.png")
    parser.add_argument("--batch", help="Path to a text file of URLs, one per line")
    parser.add_argument("--out-dir", default="data/screenshots")
    parser.add_argument("--full-page", action="store_true")


    args, unknown = parser.parse_known_args(sys.argv[1:])

    if args.batch:
        asyncio.run(batch_capture(args.batch, args.out_dir))
    elif args.url:
        path = asyncio.run(capture_screenshot(args.url, args.out, viewport_only=not args.full_page))
        print(f"Saved: {path}")
    else:
        print("No URL or batch file provided. Running a default example capture of Google.com.")
        default_url = "https://www.google.com"
        default_output = "data/screenshots/google_capture.png"
        path = asyncio.run(capture_screenshot(default_url, default_output, viewport_only=True)) 
        print(f"Default example saved: {path}")
    !apt-get update && apt-get install -y libxcomposite1
    !apt-get update && apt-get install -y libatk-bridge2.0-0
    pip install nest_asyncio
    import nest_asyncio
nest_asyncio.apply()
