# cs560_webcrawler

## Prerequisites
- pyenv
- Python 3.11
- poetry
## Optional Prerequisites
- sqlite3 or sqlitebrowser
  - sqlite3 is a command line interface for sqlite databases
    - ```bash
      sudo apt install sqlite3
      ```
  - sqlitebrowser is a GUI for viewing sqlite databases
    - ```bash
      sudo apt install sqlitebrowser
      ```

## Setup
1. Install Python 3.11
   ```bash
   pyenv install 3.11
   ```
2. Set Python 3.11 as the global version
   ```bash
   pyenv global 3.11

3. Install dependencies
   ```bash
   cd cs560_webcrawler
   poetry install
   ```
4. Activate the virtual environment
   ```bash
   poetry shell
   ```
5. Run the program
   - Current Method (Uses rich to display results)
   ```bash
   cd webcrawler
   python main.py
   ```
   - Legacy Method (Uses scrapy to crawl but logging is not formatted)
   ```bash
   scrapy runspider webrawler/spiders/zillow_houses.py
   ```

6. View the sqlite database
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
   sqlite> select * from zillow_listings;
   sqlite> select * from zillow_pages;
   ```

## Project Initialized with
```bash
scrapy startproject zillow_crawler
cd zillow_crawler/
scrapy genspider zillow_houses zillow.com
scrapy genspider books_toscrape books.toscrape.com
```
## Setup Dependencies
- Setup script will install and setup pyenv and poetry if not already installed.
- Script is meant to be run in a linux environment, e.g. WSL2 running Ubuntu 22.04
- You will be asked for your sudo password to update, upgrade, and install dependencies
```bash
cd cs560_webcrawler
chmod +x setup.sh
./setup.sh
```