# cs560_webcrawler

## Prerequisites

- pyenv
- Python 3.11
- poetry

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
   ```bash
   python main.py
   ```
