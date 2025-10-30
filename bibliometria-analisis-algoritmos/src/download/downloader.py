"""
Downloader actualizado con selección de base de datos y protección anti-bot.
Extrae título, autores, abstract, DOI, año, journal y URL reales.
"""

"""
Downloader actualizado y robusto.
Compatible con ACM, ScienceDirect y SAGE.
Usa sesión persistente para evitar captcha y bloqueos.
"""

import os, re, random, asyncio, pandas as pd
from urllib.parse import quote_plus
from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
PERSIST_DIR = os.path.join(BASE_DIR, "playwright_user_data")

# ------------------ Helpers ------------------

async def get_text(page, selector):
    try:
        el = await page.query_selector(selector)
        return (await el.inner_text()).strip() if el else ""
    except:
        return ""

async def get_all_texts(page, selector):
    els = await page.query_selector_all(selector)
    return [await el.inner_text() for el in els if el]

async def random_human_delay():
    await asyncio.sleep(random.uniform(1.5, 3.5))

# ------------------ ACM ------------------

async def scrape_acm(context, query, max_results=10):
    print("\n[ACM] Extrayendo artículos...")
    page = await context.new_page()
    await page.set_viewport_size({"width":1280,"height":900})
    await page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    })

    try:
        url = f"https://dl.acm.org/action/doSearch?AllField={quote_plus(query)}"
        await page.goto(url, wait_until="networkidle", timeout=90000)
        for _ in range(3):
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(random.uniform(0.8, 2.0))


        # Esperar resultados (nuevo selector)
        await page.wait_for_selector("h5.hlFld-Title a, li.search__item a, div.search__item h5 a", timeout=20000)
        links = await page.eval_on_selector_all("h5.hlFld-Title a, li.search__item a", "els => els.map(e => e.href)")
        links = list(dict.fromkeys(links))[:max_results]

        results = []
        for link in tqdm(links, desc="ACM artículos"):
            try:
                p = await context.new_page()
                await p.goto(link, timeout=60000)
                await random_human_delay()
                title = await get_text(p, "h1.citation__title")
                authors = ", ".join(await get_all_texts(p, "a.author-name"))
                abstract = await get_text(p, "div.abstractSection p, div.abstractInFull p")
                doi = await get_text(p, "a.doi__text")
                year = await get_text(p, "span.epub-section__date, span.year")
                journal = await get_text(p, "a.epub-section__title, a.publication-title")

                if title and abstract:
                    results.append({
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "doi": doi,
                        "year": year,
                        "journal": journal,
                        "url": link,
                        "source": "ACM"
                    })
                await p.close()
            except Exception as e:
                print(f"⚠️ Error en artículo ACM: {e}")

        df = pd.DataFrame(results)
        path = os.path.join(DATA_DIR, "acm.csv")
        df.to_csv(path, index=False)
        print(f"✅ Guardado {len(df)} artículos de ACM")
    except Exception as e:
        print(f"⚠️ ACM falló: {e}")
    finally:
        await page.close()

# ------------------ ScienceDirect ------------------

async def scrape_sciencedirect(context, query, max_results=10):
    print("\n[ScienceDirect] Extrayendo artículos...")
    page = await context.new_page()
    try:
        url = f"https://www.sciencedirect.com/search?qs={quote_plus(query)}"
        await page.goto(url, timeout=90000)
        await page.wait_for_selector("a.result-list-title-link", timeout=60000)
        links = await page.eval_on_selector_all("a.result-list-title-link", "els => els.map(e => e.href)")
        links = links[:max_results]

        results = []
        for link in tqdm(links, desc="ScienceDirect artículos"):
            try:
                p = await context.new_page()
                await p.goto(link)
                await random_human_delay()
                title = await get_text(p, "h1")
                authors = ", ".join(await get_all_texts(p, "a.author"))
                abstract = await get_text(p, "div.Abstracts p, div.abstract.author p")
                doi = await get_text(p, "a.doi")
                year = await get_text(p, "div.text-xs")
                journal = await get_text(p, "a.publication-title-link")
                results.append({
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "doi": doi,
                    "year": year,
                    "journal": journal,
                    "url": link,
                    "source": "ScienceDirect"
                })
                await p.close()
            except Exception as e:
                print(f"⚠️ Error SD: {e}")

        pd.DataFrame(results).to_csv(os.path.join(DATA_DIR, "sciencedirect.csv"), index=False)
        print(f"✅ Guardado {len(results)} artículos de ScienceDirect")
    except Exception as e:
        print(f"⚠️ ScienceDirect falló: {e}")
    finally:
        await page.close()

# ------------------ SAGE ------------------

async def scrape_sage(context, query, max_results=10):
    print("\n[SAGE] Extrayendo artículos...")
    page = await context.new_page()
    await page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    })

    try:
        url = f"https://journals.sagepub.com/action/doSearch?AllField={quote_plus(query)}"
        await page.goto(url, wait_until="domcontentloaded", timeout=90000)
        for _ in range(3):
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(random.uniform(0.8, 2.0))

        await page.wait_for_selector("h5.hlFld-Title a, li.search__item a, div.search__item h5 a", timeout=20000)
        links = await page.eval_on_selector_all("div.search__item h5 a", "els => els.map(e => e.href)")
        links = list(dict.fromkeys(links))[:max_results]

        results = []
        for link in tqdm(links, desc="SAGE artículos"):
            try:
                p = await context.new_page()
                await p.goto(link)
                await random_human_delay()
                title = await get_text(p, "h1.article-title")
                authors = ", ".join(await get_all_texts(p, "a.entryAuthor"))
                abstract = await get_text(p, "section.abstract p, div.abstractSection p")
                doi = await get_text(p, "a.ref-link, span.epub-doi")
                year = await get_text(p, "span.epub-section__date, span.year")
                journal = await get_text(p, "a.epub-section__title, a.publication-title")
                if title and abstract:
                    results.append({
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "doi": doi,
                        "year": year,
                        "journal": journal,
                        "url": link,
                        "source": "SAGE"
                    })
                await p.close()
            except Exception as e:
                print(f"⚠️ Error SAGE artículo: {e}")

        pd.DataFrame(results).to_csv(os.path.join(DATA_DIR, "sage.csv"), index=False)
        print(f"✅ Guardado {len(results)} artículos de SAGE")
    except Exception as e:
        print(f"⚠️ SAGE falló: {e}")
    finally:
        await page.close()

# ------------------ Controlador Principal ------------------

async def run_all(query, sources, max_results=10, headless=True, use_persistent=True):
    async with async_playwright() as p:
        if use_persistent:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PERSIST_DIR,
                headless=headless,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                ],
                viewport={"width": 1280, "height": 900},
                ignore_https_errors=True,
                # slow_mo = 50  # opcional: puedes establecer slow_mo para ralentizar todas las acciones
            )
        else:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()

        # medidas anti-detección: override navigator.webdriver y lenguaje
        await context.add_init_script(
            """() => {
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            }"""
        )

        try:
            # aquí llamas a tus scrapers: scrape_acm(context, ...), scrape_sciencedirect(...), ...
            for src in sources:
                if src == "acm":
                    await scrape_acm(context, query, max_results)
                elif src == "sciencedirect":
                    await scrape_sciencedirect(context, query, max_results)
                elif src == "sage":
                    await scrape_sage(context, query, max_results)
        finally:
            if use_persistent:
                await context.close()
            else:
                await browser.close()
# ------------------ Fin del Módulo ------------------