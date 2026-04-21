#!/usr/bin/env python3
"""
WSL2 Ubuntu Setup Script for Node.js/Prisma API with MySQL
Author: Lasse Sali
License: MIT License
Year: 2026
Version: 1.1
Tested on: Ubuntu 22.04 LTS (WSL2)
"""

import subprocess
import os
import sys
import getpass

def run_command(command, cwd=None, allow_fail=False):
    """Executes a shell command. Stops the script if it fails, unless allow_fail is True."""
    print(f"\n[+] Executing: {command}")
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd, executable='/bin/bash')
    except subprocess.CalledProcessError as e:
        if allow_fail:
            print(f"\n[!] Warning: Command failed, but continuing script. (Exit code {e.returncode})")
        else:
            print(f"\n[!] Error: Command failed with exit code {e.returncode}")
            print(f"[!] Command: {command}")
            sys.exit(1)

def main():
    print("--- WSL2 Ubuntu Setup Script for Node.js/Prisma API with MySQL ---")
    print("--- v1.1 | Author: Nova Pax ---")
    
    # --- Ask for user inputs ---
    github_username = input("\n[?] Enter your GitHub username: ").strip()
    if not github_username:
        print("\n[!] GitHub username is required. Exiting.")
        sys.exit(1)

    # Ask for repository name, default to wohi2-course-project
    repo_name = input("[?] Enter repository name [wohi2-course-project]: ").strip()
    if not repo_name:
        repo_name = "wohi2-course-project"

    # Ask for database name, default to MyDb
    db_name = input("[?] Enter database name [MyDb]: ").strip()
    if not db_name:
        db_name = "MyDb"

    mysql_user = input("[?] Enter desired MySQL username: ").strip()
    mysql_pass = getpass.getpass("[?] Enter desired MySQL password: ").strip()
    
    if not mysql_user or not mysql_pass:
        print("\n[!] MySQL user and password are required. Exiting.")
        sys.exit(1)

    # 1. Update and Upgrade System
    run_command("sudo apt update")
    run_command("sudo apt upgrade -y")

    # 2. Install Required Packages
    packages = "nodejs npm net-tools mysql-client mysql-server ufw nano"
    run_command(f"sudo apt install -y {packages}")

    run_command("nodejs -v")
    run_command("npm -v")

    # 3. Configure Firewall (UFW) - Allowed to fail gracefully on WSL2
    print("\n[i] Note: UFW commands may fail on some WSL2 setups. Windows Firewall usually handles ports.")
    run_command("sudo ufw allow 3000/tcp", allow_fail=True)
    run_command("sudo ufw reload", allow_fail=True)
    run_command("sudo ufw status", allow_fail=True)

    # 4. Start MySQL Service - Using 'service' instead of 'systemctl' for WSL2
    run_command("sudo service mysql start")

    # 5. Automate MySQL Secure Installation & Database Creation
    # Injecting the dynamic db_name variable
    mysql_setup_query = f"""
    DROP DATABASE IF EXISTS test;
    DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
    FLUSH PRIVILEGES;
    
    CREATE DATABASE IF NOT EXISTS {db_name};
    CREATE USER IF NOT EXISTS '{mysql_user}'@'localhost' IDENTIFIED BY '{mysql_pass}';
    GRANT ALL PRIVILEGES ON *.* TO '{mysql_user}'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    """
    
    print("\n[+] Configuring MySQL Database and User...")
    subprocess.run(["sudo", "mysql", "-u", "root"], input=mysql_setup_query.encode('utf-8'), check=True)
    print("[+] MySQL configured successfully.")

    # 6. Setup Application Directory
    # Resolves to the current user's home directory (~/src/github.com/username)
    home_dir = os.path.expanduser("~")
    app_base_dir = f"{home_dir}/src/github.com/{github_username}"
    repo_url = f"https://github.com/{github_username}/{repo_name}"
    project_dir = f"{app_base_dir}/{repo_name}"

    # Removed sudo: Safe to create directories in your own home folder
    run_command(f"mkdir -p {app_base_dir}")
    
    if not os.path.exists(project_dir):
        # Removed sudo: Safe to run git clone as standard user here
        run_command(f"git clone {repo_url}", cwd=app_base_dir)
    else:
        print(f"\n[!] Directory {project_dir} already exists. Skipping git clone.")

    # 7. Create the .env file natively with Python
    # Injecting the dynamic db_name into the Prisma connection string
    env_content = f'DATABASE_URL="mysql://{mysql_user}:{mysql_pass}@localhost:3306/{db_name}"\n'
    env_path = f"{project_dir}/.env"
    
    print(f"\n[+] Creating .env file at {env_path}...")
    with open(env_path, "w") as f:
        f.write(env_content)

    # 8. Install Dependencies and Start App
    # Removed sudo: Prevent root ownership issues in node_modules
    run_command("npm install", cwd=project_dir)
    run_command("npx prisma generate", cwd=project_dir)
    run_command("npx prisma migrate deploy", cwd=project_dir)
    run_command("npx prisma db seed", cwd=project_dir)
    
    print(f"\n[+] Setup complete! Starting the application from {project_dir}...")
    run_command("npm run start", cwd=project_dir)

if __name__ == "__main__":
    main()