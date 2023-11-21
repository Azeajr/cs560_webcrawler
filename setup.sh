#!/bin/bash

# Update and Upgrade
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y

# Install Dependencies
sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y


# Install Python Version Manager
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
curl https://pyenv.run | bash


# Setup Python Version Manager to bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"


# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc


# Install Python
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv install 3.11 && pyenv global 3.11