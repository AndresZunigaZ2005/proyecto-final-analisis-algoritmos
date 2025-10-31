"""
Downloader con APIs REST completamente abiertas - Sin web scraping.
Bases de datos: OpenAlex, arXiv, PubMed Central
Incluye extracción de país de afiliación/autores
"""

import os
import re
import asyncio
import pandas as pd
from urllib.parse import quote_plus
from tqdm.asyncio import tqdm
import aiohttp
import feedparser
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data/download")
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------ Helper para extraer país ------------------

def extract_country_from_text(text):
    """
    Extrae el país de un texto usando patrones comunes.
    Retorna el primer país encontrado o cadena vacía.
    """
    if not text:
        return ""
    
    # Lista de países comunes (puedes expandirla)
    countries = {
        'United States': ['USA', 'United States', 'U.S.A', 'U.S.', 'US'],
        'United Kingdom': ['UK', 'United Kingdom', 'U.K.', 'England', 'Scotland', 'Wales'],
        'China': ['China', 'P.R. China', 'PR China'],
        'Germany': ['Germany', 'Deutschland'],
        'France': ['France'],
        'Japan': ['Japan'],
        'Canada': ['Canada'],
        'Australia': ['Australia'],
        'India': ['India'],
        'Brazil': ['Brazil', 'Brasil'],
        'Spain': ['Spain', 'España'],
        'Italy': ['Italy', 'Italia'],
        'Netherlands': ['Netherlands', 'Holland'],
        'Switzerland': ['Switzerland', 'Suisse'],
        'South Korea': ['South Korea', 'Korea', 'Republic of Korea'],
        'Sweden': ['Sweden'],
        'Russia': ['Russia', 'Russian Federation'],
        'Mexico': ['Mexico', 'México'],
        'Argentina': ['Argentina'],
        'Colombia': ['Colombia'],
        'Chile': ['Chile'],
        'Peru': ['Peru', 'Perú'],
        'Israel': ['Israel'],
        'South Africa': ['South Africa'],
        'Singapore': ['Singapore'],
        'New Zealand': ['New Zealand'],
        'Belgium': ['Belgium'],
        'Austria': ['Austria'],
        'Poland': ['Poland'],
        'Denmark': ['Denmark'],
        'Finland': ['Finland'],
        'Norway': ['Norway'],
        'Ireland': ['Ireland'],
        'Portugal': ['Portugal'],
        'Greece': ['Greece'],
        'Turkey': ['Turkey', 'Türkiye'],
        'Iran': ['Iran'],
        'Saudi Arabia': ['Saudi Arabia'],
        'Egypt': ['Egypt'],
        'Taiwan': ['Taiwan'],
        'Thailand': ['Thailand'],
        'Malaysia': ['Malaysia'],
        'Indonesia': ['Indonesia'],
        'Pakistan': ['Pakistan'],
        'Vietnam': ['Vietnam'],
        'Czech Republic': ['Czech Republic', 'Czechia'],
        'Hungary': ['Hungary'],
        'Romania': ['Romania'],
        'Ukraine': ['Ukraine']
    }
    
    text_lower = text.lower()
    
    # Buscar países en el texto
    for country, aliases in countries.items():
        for alias in aliases:
            if alias.lower() in text_lower:
                return country
    
    return ""

# ------------------ OpenAlex (API REST) ------------------

async def scrape_openalex(query, max_results=10):
    """
    OpenAlex - API pública sin API key.
    https://docs.openalex.org/
    """
    print("\n[OpenAlex] Extrayendo artículos vía API...")
    
    try:
        base_url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per_page": max_results,
            "mailto": "research@example.com"
        }
        
        results = []
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for work in tqdm(data.get("results", []), desc="OpenAlex artículos"):
                        try:
                            title = work.get("title", "")
                            
                            # Autores y países
                            authorships = work.get("authorships", [])
                            authors = ", ".join([
                                auth.get("author", {}).get("display_name", "")
                                for auth in authorships
                            ])
                            
                            # Extraer país de instituciones
                            country = ""
                            for authorship in authorships:
                                institutions = authorship.get("institutions", [])
                                for inst in institutions:
                                    # OpenAlex tiene el país en la institución
                                    country_code = inst.get("country_code", "")
                                    if country_code:
                                        # Convertir código a nombre completo
                                        country_name = get_country_name_from_code(country_code)
                                        if country_name:
                                            country = country_name
                                            break
                                    
                                    # Si no hay código, buscar en el nombre de la institución
                                    if not country:
                                        inst_name = inst.get("display_name", "")
                                        country = extract_country_from_text(inst_name)
                                        if country:
                                            break
                                
                                if country:
                                    break
                            
                            # Abstract desde inverted index
                            abstract = work.get("abstract_inverted_index", {})
                            if abstract:
                                words = {}
                                for word, positions in abstract.items():
                                    for pos in positions:
                                        words[pos] = word
                                abstract_text = " ".join([words[i] for i in sorted(words.keys())])
                            else:
                                abstract_text = ""
                            
                            # DOI
                            doi = work.get("doi", "").replace("https://doi.org/", "")
                            
                            # Año
                            year = str(work.get("publication_year", ""))
                            
                            # Journal
                            journal = ""
                            primary_location = work.get("primary_location", {})
                            if primary_location:
                                source = primary_location.get("source", {})
                                journal = source.get("display_name", "")
                            
                            # URL
                            url = work.get("id", "")
                            
                            if title:
                                results.append({
                                    "title": title,
                                    "authors": authors,
                                    "abstract": abstract_text,
                                    "doi": doi,
                                    "year": year,
                                    "journal": journal,
                                    "url": url,
                                    "country": country,
                                    "source": "OpenAlex"
                                })
                        except Exception as e:
                            print(f"⚠️ Error procesando artículo: {e}")
                            continue
                else:
                    print(f"⚠️ Error en API: {response.status}")
        
        df = pd.DataFrame(results)
        path = os.path.join(DATA_DIR, "openalex.csv")
        df.to_csv(path, index=False, encoding='utf-8')
        print(f"✅ Guardado {len(df)} artículos de OpenAlex")
        print(f"   📍 Artículos con país: {df['country'].notna().sum()}")
        
    except Exception as e:
        print(f"⚠️ OpenAlex falló: {e}")

# ------------------ arXiv (API REST) ------------------

async def scrape_arxiv(query, max_results=10):
    """
    arXiv - API pública sin API key.
    http://arxiv.org/help/api/
    Nota: arXiv no proporciona información de país directamente
    """
    print("\n[arXiv] Extrayendo artículos vía API...")
    
    try:
        base_url = "http://export.arxiv.org/api/query"
        params = f"search_query=all:{quote_plus(query)}&start=0&max_results={max_results}"
        url = f"{base_url}?{params}"
        
        results = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    for entry in tqdm(feed.entries, desc="arXiv artículos"):
                        try:
                            title = entry.title.replace("\n", " ").strip()
                            
                            # Autores
                            authors = ", ".join([author.name for author in entry.authors])
                            
                            # Intentar extraer afiliación de comentarios
                            country = ""
                            if hasattr(entry, 'arxiv_comment'):
                                country = extract_country_from_text(entry.arxiv_comment)
                            
                            # Si no hay país, dejar vacío (arXiv no siempre tiene esta info)
                            if not country:
                                country = ""
                            
                            # Abstract
                            abstract = entry.summary.replace("\n", " ").strip()
                            
                            # DOI
                            doi = entry.get("arxiv_doi", "")
                            
                            # Año
                            published = entry.published
                            year = published.split("-")[0] if published else ""
                            
                            # Journal/Category
                            categories = [tag.term for tag in entry.tags]
                            journal = f"arXiv: {', '.join(categories[:2])}"
                            
                            # URL
                            url = entry.id
                            
                            if title and abstract:
                                results.append({
                                    "title": title,
                                    "authors": authors,
                                    "abstract": abstract,
                                    "doi": doi,
                                    "year": year,
                                    "journal": journal,
                                    "url": url,
                                    "country": country,
                                    "source": "arXiv"
                                })
                        except Exception as e:
                            print(f"⚠️ Error procesando artículo: {e}")
                            continue
                else:
                    print(f"⚠️ Error en API: {response.status}")
        
        df = pd.DataFrame(results)
        path = os.path.join(DATA_DIR, "arxiv.csv")
        df.to_csv(path, index=False, encoding='utf-8')
        print(f"✅ Guardado {len(df)} artículos de arXiv")
        print(f"   📍 Artículos con país: {df['country'].notna().sum()}")
        
    except Exception as e:
        print(f"⚠️ arXiv falló: {e}")

# ------------------ PubMed Central (API REST) ------------------

async def scrape_pubmed(query, max_results=10):
    """
    PubMed Central - API pública sin API key (E-utilities).
    https://www.ncbi.nlm.nih.gov/books/NBK25501/
    """
    print("\n[PubMed] Extrayendo artículos vía API...")
    
    try:
        # Paso 1: Buscar IDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pmc",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "tool": "bibliometria_app",
            "email": "research@example.com"
        }
        
        results = []
        async with aiohttp.ClientSession() as session:
            # Obtener IDs
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    ids = data.get("esearchresult", {}).get("idlist", [])
                    
                    if not ids:
                        print("⚠️ No se encontraron resultados")
                        return
                    
                    print(f"📋 Encontrados {len(ids)} artículos")
                    
                    # Paso 2: Obtener detalles de cada artículo
                    for pmid in tqdm(ids, desc="PubMed artículos"):
                        try:
                            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                            fetch_params = {
                                "db": "pmc",
                                "id": pmid,
                                "retmode": "xml"
                            }
                            
                            async with session.get(fetch_url, params=fetch_params) as fetch_response:
                                if fetch_response.status == 200:
                                    import xml.etree.ElementTree as ET
                                    xml_text = await fetch_response.text()
                                    root = ET.fromstring(xml_text)
                                    
                                    # Extraer campos
                                    title = ""
                                    title_elem = root.find(".//article-title")
                                    if title_elem is not None:
                                        title = "".join(title_elem.itertext()).strip()
                                    
                                    # Autores y país
                                    authors_list = []
                                    country = ""
                                    
                                    for contrib in root.findall(".//contrib[@contrib-type='author']"):
                                        surname = contrib.find(".//surname")
                                        given = contrib.find(".//given-names")
                                        if surname is not None:
                                            name = surname.text or ""
                                            if given is not None and given.text:
                                                name = f"{given.text} {name}"
                                            authors_list.append(name)
                                        
                                        # Buscar afiliación del autor
                                        if not country:
                                            aff = contrib.find(".//aff")
                                            if aff is not None:
                                                aff_text = "".join(aff.itertext()).strip()
                                                country = extract_country_from_text(aff_text)
                                    
                                    # Si no se encontró en autores, buscar en afiliaciones generales
                                    if not country:
                                        for aff in root.findall(".//aff"):
                                            aff_text = "".join(aff.itertext()).strip()
                                            country = extract_country_from_text(aff_text)
                                            if country:
                                                break
                                    
                                    authors = ", ".join(authors_list)
                                    
                                    # Abstract
                                    abstract = ""
                                    abstract_elem = root.find(".//abstract")
                                    if abstract_elem is not None:
                                        abstract = " ".join(abstract_elem.itertext()).strip()
                                    
                                    # DOI
                                    doi = ""
                                    doi_elem = root.find(".//article-id[@pub-id-type='doi']")
                                    if doi_elem is not None:
                                        doi = doi_elem.text or ""
                                    
                                    # Año
                                    year = ""
                                    year_elem = root.find(".//pub-date/year")
                                    if year_elem is not None:
                                        year = year_elem.text or ""
                                    
                                    # Journal
                                    journal = ""
                                    journal_elem = root.find(".//journal-title")
                                    if journal_elem is not None:
                                        journal = journal_elem.text or ""
                                    
                                    # URL
                                    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmid}/"
                                    
                                    if title:
                                        results.append({
                                            "title": title,
                                            "authors": authors,
                                            "abstract": abstract,
                                            "doi": doi,
                                            "year": year,
                                            "journal": journal,
                                            "url": url,
                                            "country": country,
                                            "source": "PubMed"
                                        })
                                
                                await asyncio.sleep(0.4)  # Rate limit: 3 req/sec
                                
                        except Exception as e:
                            print(f"⚠️ Error procesando artículo {pmid}: {e}")
                            continue
                else:
                    print(f"⚠️ Error en búsqueda: {response.status}")
        
        df = pd.DataFrame(results)
        path = os.path.join(DATA_DIR, "pubmed.csv")
        df.to_csv(path, index=False, encoding='utf-8')
        print(f"✅ Guardado {len(df)} artículos de PubMed")
        print(f"   📍 Artículos con país: {df['country'].notna().sum()}")
        
    except Exception as e:
        print(f"⚠️ PubMed falló: {e}")

# ------------------ Helper para códigos de país ------------------

def get_country_name_from_code(code):
    """
    Convierte código de país ISO a nombre completo.
    """
    country_codes = {
        'US': 'United States',
        'GB': 'United Kingdom',
        'CN': 'China',
        'DE': 'Germany',
        'FR': 'France',
        'JP': 'Japan',
        'CA': 'Canada',
        'AU': 'Australia',
        'IN': 'India',
        'BR': 'Brazil',
        'ES': 'Spain',
        'IT': 'Italy',
        'NL': 'Netherlands',
        'CH': 'Switzerland',
        'KR': 'South Korea',
        'SE': 'Sweden',
        'RU': 'Russia',
        'MX': 'Mexico',
        'AR': 'Argentina',
        'CO': 'Colombia',
        'CL': 'Chile',
        'PE': 'Peru',
        'IL': 'Israel',
        'ZA': 'South Africa',
        'SG': 'Singapore',
        'NZ': 'New Zealand',
        'BE': 'Belgium',
        'AT': 'Austria',
        'PL': 'Poland',
        'DK': 'Denmark',
        'FI': 'Finland',
        'NO': 'Norway',
        'IE': 'Ireland',
        'PT': 'Portugal',
        'GR': 'Greece',
        'TR': 'Turkey',
        'IR': 'Iran',
        'SA': 'Saudi Arabia',
        'EG': 'Egypt',
        'TW': 'Taiwan',
        'TH': 'Thailand',
        'MY': 'Malaysia',
        'ID': 'Indonesia',
        'PK': 'Pakistan',
        'VN': 'Vietnam',
        'CZ': 'Czech Republic',
        'HU': 'Hungary',
        'RO': 'Romania',
        'UA': 'Ukraine'
    }
    
    return country_codes.get(code.upper(), "")

# ------------------ Controlador Principal ------------------

async def run_all(query, sources, max_results=10, headless=False, use_persistent=True):
    """
    Ejecuta la descarga de artículos de las fuentes seleccionadas.
    Todas las fuentes usan APIs REST - No requiere Playwright.
    """
    print(f"\n🔍 Buscando: '{query}'")
    print(f"📚 Fuentes seleccionadas: {', '.join(sources)}")
    print(f"📊 Artículos por fuente: {max_results}")
    
    for src in sources:
        if src == "openalex":
            await scrape_openalex(query, max_results)
        elif src == "arxiv":
            await scrape_arxiv(query, max_results)
        elif src == "pubmed":
            await scrape_pubmed(query, max_results)
        else:
            print(f"⚠️ Fuente desconocida: {src}")

# ------------------ Fin del Módulo ------------------