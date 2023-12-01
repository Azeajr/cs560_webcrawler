# Setup environment

## Windows

- Activate WSL(also installs Ubuntu by default)

  ```powershell
  wsl --install
  ```

- Install Windows Terminal from the Microsoft Store
- Open Windows Terminal and select Ubuntu
- Run setup script(Directions are the same as for Linux)

  - You will be asked for your sudo password to update, upgrade, and install dependencies

    ```bash
    cd cs560_webcrawler
    chmod +x setup.sh
    ./setup.sh

    source ~/.bashrc
    ```

## Reset WSL Environment

- From Windows Powershell
  ```powershell
  Get-AppxPackage Ubuntu | Reset-AppxPackage
  wsl --unregister Ubuntu
  wsl --install
  ```
