python -m venv .venv
. .venv/bin/activate

python -m pip install -U pip
python -m pip install -U rich duckduckgo_search yagooglesearch

git clone https://github.com/tasos-py/Search-Engines-Scraper
python Search-Engines-Scraper/setup.py
rm -rf Search-Engines-Scraper

