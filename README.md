# cs560_webcrawler

## Prerequisites
- pyenv
- Python 3.11
- poetry
## Optional Prerequisites
- Homebrew
- sqlitebrowser
  - GUI for viewing sqlite databases

## Setup

1. Install pyenv
   ```bash
   brew install pyenv
   ```
   or
   ```bash
   curl https://pyenv.run | bash
   ```
2. Install Python 3.11
   ```bash
   pyenv install 3.11
   ```
3. Set Python 3.11 as the global version
   ```bash
   pyenv global 3.11
   ```
4. Install poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
5. Install dependencies
   ```bash
   cd cs560_webcrawler
   poetry install
   ```
6. Activate the virtual environment
   ```bash
   poetry shell
   ```
7. Run the program
   - Current Method (Uses rich to display results)
   ```bash
   python main.py
   ```
   - Legacy Method (Uses scrapy to crawl but logging is not formatted)
   ```bash
   scrapy runspider zillow_crawler/spiders/books_toscrape.py
   ```

8. View the sqlite database
   ```bash
   sqlitebrowser zillow_crawler.db
   ```
   or
   ```bash
   sqlite3 zillow_crawler.db
   ```
   To list all tables(Omit `sqlite>` when running in sqlite3 shell)
   ```sql
   sqlite> .tables 
   ```
   To view the schema of a table:
   ```sql
   sqlite> .schema <table_name>
   ```
   To view the contents of a table:
   ```sql
   sqlite> select * from books;
   ```

## Project Initialized with
```bash
scrapy startproject zillow_crawler
cd zillow_crawler/
scrapy genspider zillow_houses zillow.com
scrapy genspider books_toscrape books.toscrape.com
```