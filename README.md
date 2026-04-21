# WSL2 Ubuntu Setup Script for Node.js & Prisma

This repository contains a Python script designed to fully automate the tedious setup of a modern Node.js development environment on WSL2 (Ubuntu). 

Instead of manually running dozens of commands to configure databases and firewalls, this script handles everything in one go.

## ✨ What it does

1. **Updates & Upgrades** the Ubuntu system packages.
2. **Installs Dependencies:** Node.js, npm, net-tools, MySQL (client/server), UFW, and nano.
3. **Configures the Firewall:** Opens port 3000 (gracefully handles WSL2 network quirks).
4. **Automates MySQL:** Starts the service, cleans up test databases, creates a new database, and securely sets up a new user with custom credentials.
5. **Sets up the Workspace:** Clones your specified GitHub repository into the high-performance native Linux directory (`~/src/github.com/`).
6. **Generates Environment Variables:** Automatically creates a `.env` file with the correct Prisma database connection string based on your inputs.
7. **Initializes the App:** Runs `npm install`, generates Prisma client, deploys migrations, seeds the database, and starts the development server.

## 📋 Prerequisites

* Windows Subsystem for Linux (WSL2) installed.
* Ubuntu running as your WSL2 distribution.
* Python 3 (comes pre-installed on modern Ubuntu).

## 🚀 How to Use

1. **Download the script** directly to your WSL2 terminal:
   ```bash
   wget [https://raw.githubusercontent.com/lassesali/wsl2-node-prisma-setup/main/setup.py](https://raw.githubusercontent.com/lassesali/wsl2-node-prisma-setup/main/setup.py)

2. **Make it executable:**
   ```bash
   chmod +x setup.py

3. **Run the script:**
   ```bash
   ./setup.py

4. **Follow the prompts:**
 
   The script will ask for your GitHub username, the target repository name, the database name, and the MySQL credentials you want to use.

## ⚠️ Disclaimer

Because this script automates system-level installations and database configurations, it requires sudo privileges. You will be prompted for your Ubuntu user password when it runs. Always review automation scripts before executing them on your machine.

## 📄 License

This project is licensed under the MIT License.
