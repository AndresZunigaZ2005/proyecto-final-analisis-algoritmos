# src/download/downloader.py
"""
Scraper actualizado: obtiene datos reales (título, autores, resumen, año, DOI, journal, url)
de ACM, ScienceDirect y SAGE mediante selectores CSS visibles.
"""

import asyncio
import os
import re
import pandas as pd
from urllib.parse import quote_plus
from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- funciones auxiliares ----------
async def get_text(page, selector):
    try:
        el = await page.query_selector(selector)
        if el:
            text = (await el.inner_text()).strip()
            return re.sub(r"\s+", " ", text)
    except:
        pass
    return ""

async def get_all_texts(page, selector):
    items = await page.query_selector_all(selector)
    results = []
    for el in items:
        try:
            t = (await el.inner_text()).strip()
            if t:
                results.append(re.sub(r"\s+", " ", t))
        except:
            pass
    return results

# ---------- scrapers por sitio ----------
async def scrape_acm(playwright, query, max_results=10):
    print("\n[ACM] Extrayendo artículos...")
    browser = playwright
    page = await browser.new_page()
    url = f"https://dl.acm.org/action/doSearch?AllField={quote_plus(query)}"
    await page.goto(url)
    await page.wait_for_selector("li.search__item", timeout=60000)

    # Extraer los enlaces de los títulos
    links = await page.eval_on_selector_all(
        "h5.issue-item__title a", "els => els.map(e => e.href)"
    )
    links = links[:max_results]

    results = []
    for link in tqdm(links, desc="ACM artículos"):
        try:
            p = await browser.new_page()
            await p.goto(link, timeout=60000)
            await p.wait_for_timeout(1500)

            title = await get_text(p, "h1.citation__title")
            authors = ", ".join(await get_all_texts(p, "a.author-name"))
            abstract = await get_text(p, "div.abstractInFull p")
            doi = await get_text(p, "a.doi__text")
            year = await get_text(p, "span.epub-section__date")
            journal = await get_text(p, "a.epub-section__title")

            results.append({
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "doi": doi,
                "year": year,
                "journal": journal,
                "url": link,
                "source": "ACM",
            })
            await p.close()
        except Exception as e:
            print(f"Error ACM: {e}")

    df = pd.DataFrame(results)
    path = os.path.join(DATA_DIR, "acm.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"✅ Guardado {len(df)} artículos en {path}")
    await page.close()
    return path


async def scrape_sciencedirect(playwright, query, max_results=20):
    print("\n[ScienceDirect] Extrayendo artículos...")
    browser = playwright
    page = await browser.new_page()
    url = f"https://www.sciencedirect.com/search?qs={quote_plus(query)}"
    await page.goto(url)
    await page.wait_for_selector(".result-item-content", timeout=60000)

    links = await page.eval_on_selector_all(
        "a.result-list-title-link", "els => els.map(e => e.href)"
    )
    links = links[:max_results]

    results = []
    pbar = tqdm(links, desc="ScienceDirect artículos")
    for link in pbar:
        try:
            p = await browser.new_page()
            await p.goto(link, timeout=60000)
            await p.wait_for_timeout(1500)

            title = await get_text(p, "h1")
            authors = ", ".join(await get_all_texts(p, "a.author"))
            abstract = await get_text(p, "div.Abstracts div.abstract.author p")
            doi = await get_text(p, "a.doi")
            year = await get_text(p, "div.text-xs")
            journal = await get_text(p, "a.publication-title-link")

            results.append(
                {
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "doi": doi,
                    "year": year,
                    "journal": journal,
                    "url": link,
                    "source": "ScienceDirect",
                }
            )
            await p.close()
        except Exception as e:
            print(f"Error SD: {e}")
    df = pd.DataFrame(results)
    path = os.path.join(DATA_DIR, "sciencedirect.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"✅ Guardado {len(df)} artículos en {path}")
    await page.close()
    return path


async def scrape_sage(playwright, query, max_results=10):
    print("\n[SAGE] Extrayendo artículos...")
    browser = playwright
    page = await browser.new_page()
    url = f"https://journals.sagepub.com/action/doSearch?AllField={quote_plus(query)}"
    await page.goto(url)
    await page.wait_for_selector("div.item__body", timeout=60000)

    links = await page.eval_on_selector_all(
        "div.item__body h5 a", "els => els.map(e => e.href)"
    )
    links = links[:max_results]

    results = []
    for link in tqdm(links, desc="SAGE artículos"):
        try:
            p = await browser.new_page()
            await p.goto(link, timeout=60000)
            await p.wait_for_timeout(1500)

            title = await get_text(p, "h1.article-title")
            authors = ", ".join(await get_all_texts(p, "a.entryAuthor"))
            abstract = await get_text(p, "section.abstract p")
            doi = await get_text(p, "a.ref-link")
            year = await get_text(p, "span.epub-section__date")
            journal = await get_text(p, "a.epub-section__title")

            results.append({
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "doi": doi,
                "year": year,
                "journal": journal,
                "url": link,
                "source": "SAGE",
            })
            await p.close()
        except Exception as e:
            print(f"Error SAGE: {e}")

    df = pd.DataFrame(results)
    path = os.path.join(DATA_DIR, "sage.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"✅ Guardado {len(df)} artículos en {path}")
    await page.close()
    return path

# ---------- ejecutor principal ----------
async def run_all(query="generative artificial intelligence", max_results=10, headless=False, delay_between_requests=1.0):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, slow_mo=delay_between_requests * 1000)
        context = await browser.new_context()

        scrapers = [
            ("ACM", scrape_acm),
            ("ScienceDirect", scrape_sciencedirect),
            ("SAGE", scrape_sage),
        ]

        for name, scraper_func in scrapers:
            try:
                print(f"\n🚀 Iniciando scraping en {name}...")
                await scraper_func(context, query, max_results)
            except Exception as e:
                print(f"⚠️ Error en {name}: {e}")
                print("→ Continuando con la siguiente base de datos...")

        await context.close()
        await browser.close()
        print("\n✅ Scraping completado en todas las bases de datos disponibles.")
        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", default="generative artificial intelligence")
    parser.add_argument("--max", "-m", type=int, default=10)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    asyncio.run(run_all(args.query, args.max, args.headless))
