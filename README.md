# WSL2 Node.js & Prisma Environment Automator

A robust Python script designed to fully automate the setup of a modern Node.js development environment on WSL2. Built to save time for developers by handling everything from system updates to database initialization.

**Author:** Lasse Sali
**Version:** 1.2  
**License:** MIT

## 🌟 Why use this?
Setting up a database, configuring firewalls, and managing Prisma environments in WSL2 is tedious. This script does it all in one command, ensuring:
- **Optimal Speed:** Files are placed in the native Linux filesystem (`~/src/`) to avoid the slow `/mnt/c/` boundary.
- **Auto-Detection:** Works on both **Ubuntu** (installs MySQL) and **Debian** (installs MariaDB).
- **Clean Transitions:** Handles `CTRL+C` gracefully without throwing messy error blocks.

## 🚀 Features

* **Smart Distro Detection:** Automatically detects if you are running **Ubuntu** or **Debian** and installs the appropriate database engine (MySQL for Ubuntu, MariaDB for Debian).
* **Native Performance:** Clones your repository into the native Linux filesystem (`~/src/github.com/...`) for maximum I/O speed.
* **Database Automation:** Starts the database service, creates a custom database and user, and handles security cleanups.
* **Prisma Ready:** Automatically generates the `.env` file with your dynamic credentials and runs `migrate deploy` and `db seed`.
* **Safe Execution:** Gracefully handles WSL2 firewall (UFW) quirks.

## 📋 Prerequisites

* Windows 10/11 with **WSL2** enabled.
* An installed instance of **Ubuntu** or **Debian**.
* Python 3 (pre-installed on most WSL distros).

## 🛠️ How to Use

1.  **Download the script** to your WSL2 home directory:
    ```bash
    wget [https://raw.githubusercontent.com/lassesali/wsl2-node-prisma-setup/main/setup.py](https://raw.githubusercontent.com/lassesali/wsl2-node-prisma-setup/main/setup.py)
    ```

2.  **Make it executable:**
    ```bash
    chmod +x setup.py
    ```

3.  **Run the script:**
    ```bash
    ./setup.py
    ```

4.  **Follow the prompts:** Provide your GitHub username, repository name, desired database name, and credentials when prompted.

## 📁 Directory Structure
The script organizes your work following a professional standard:
`~/src/github.com/{username}/{repository_name}`

## 📄 License
This project is licensed under the MIT License.

---
**Author:** Lasse Sali  
**Version:** 1.2   
**Year:** 2026