# Datenaquise durch Scrapy


## Nutzung

 ```bash
pip install -r requirements.txt
scrapy crawl [NAME DES SCRAPERS] 
```

## Hinweise 
1. Jeder Scraper erzeugt eine neue DB-Datei, um die alte nicht zu überschreiben, sollte die neue in der settings.py verändert werden
2. Um die Scraper auszuführen bitte die Dependencies unter requirements.txt installieren
3. Um die Wikipedia Daten zu laden, sollte die jeweillige Kategorie verändert werden (unter _smallcategories)

