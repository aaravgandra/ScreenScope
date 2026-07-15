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
import sys # Import sys to access command-line arguments
import asyncio # Import asyncio for async operations

from playwright.async_api import async_playwright # Change to async_playwright


async def capture_screenshot( # Make function async
    url: str,
    out_path: str,
    viewport_only: bool = True,
    width: int = 1440,
    height: int = 1024,
    wait_ms: int = 2000,
) -> str:
    """
    Capture a screenshot of `url` and save it to `out_path`.

    viewport_only=True captures just the visible viewport, which is usually
    what you want for cookie banners / checkout modals (full-page screenshots
    of long pages make bounding boxes harder to reason about and the eventual
    LLM call more expensive). Set False for full-page capture.
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p: # Use async with and async_playwright
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.goto(url, wait_until="networkidle", timeout=30000)
        # give cookie banners / dynamic content time to render
        await asyncio.sleep(wait_ms / 1000) # Use asyncio.sleep
        await page.screenshot(path=out_path, full_page=not viewport_only)
        await browser.close()

    return out_path


async def batch_capture(url_list_path: str, out_dir: str) -> list[str]: # Make function async
    """
    Capture screenshots for every URL in a text file (one URL per line).
    Filenames are derived from the URL. Skips URLs that fail rather than
    aborting the whole batch — logs failures to stderr.
    """
    saved = []
    with open(url_list_path) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for i, url in enumerate(urls):
        safe_name = url.replace("https://", "").replace("http://", "")
        safe_name = safe_name.replace("/", "_").replace(":", "_")[:80]
        out_path = os.path.join(out_dir, f"{i:03d}_{safe_name}.png")
        try:
            await capture_screenshot(url, out_path) # await the async function
            saved.append(out_path)
            print(f"[ok] {url} -> {out_path}")
        except Exception as e:
            print(f"[fail] {url}: {e}")

    return saved


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Single URL to capture") # Changed from positional to optional flag
    parser.add_argument("--out", default="data/screenshots/capture.png")
    parser.add_argument("--batch", help="Path to a text file of URLs, one per line")
    parser.add_argument("--out-dir", default="data/screenshots")
    parser.add_argument("--full-page", action="store_true")

    # Use parse_known_args to handle unknown arguments passed by the Colab kernel
    # and only parse the arguments defined for the script.
    args, unknown = parser.parse_known_args(sys.argv[1:])

    if args.batch:
        asyncio.run(batch_capture(args.batch, args.out_dir)) # Run async batch_capture
    elif args.url:
        path = asyncio.run(capture_screenshot(args.url, args.out, viewport_only=not args.full_page)) # Run async capture_screenshot
        print(f"Saved: {path}")
    else:
        # If no URL or batch is provided, run a default example for demonstration
        print("No URL or batch file provided. Running a default example capture of Google.com.")
        default_url = "https://www.google.com"
        default_output = "data/screenshots/google_capture.png"
        path = asyncio.run(capture_screenshot(default_url, default_output, viewport_only=True)) # Run async capture_screenshot
        print(f"Default example saved: {path}")
    !apt-get update && apt-get install -y libxcomposite1
    !apt-get update && apt-get install -y libatk-bridge2.0-0
    pip install nest_asyncio
    import nest_asyncio
nest_asyncio.apply()
