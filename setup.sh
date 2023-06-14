python3 -m venv .venv
. .venv/bin/activate

python3 -m pip install -U pip
python3 -m pip install -U rich duckduckgo_search yagooglesearch

git clone https://github.com/tasos-py/Search-Engines-Scraper
cd Search-Engines-Scraper
python setup.py install
cd ..
rm -rf Search-Engines-Scraper
