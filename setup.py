#!/usr/bin/env python3
"""
WSL2 Setup Script for Node.js/Prisma API
Supports: Ubuntu & Debian
Author: Lasse Sali
License: MIT License
Year: 2026
Version: 1.2
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

def get_linux_distro():
    """Reads the OS release file to determine if we are on Ubuntu or Debian."""
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"').lower()
    return "unknown"

def main():
    try:
        print("--- WSL2 Setup Script for Node.js/Prisma API ---")
        print("--- v1.2 | Author: Lasse Sali ---")
        
        # --- Detect OS ---
        distro = get_linux_distro()
        if distro == "ubuntu":
            print("\n[i] Detected OS: Ubuntu. Using MySQL.")
            db_packages = "mysql-client mysql-server"
            db_service = "mysql"
        elif distro == "debian":
            print("\n[i] Detected OS: Debian. Using MariaDB.")
            db_packages = "mariadb-client mariadb-server"
            db_service = "mariadb"
        else:
            print(f"\n[!] Unsupported OS: {distro}. Script supports Ubuntu/Debian.")
            sys.exit(1)

        # --- Ask for user inputs ---
        github_username = input("\n[?] Enter your GitHub username: ").strip()
        if not github_username:
            print("\n[!] GitHub username is required. Exiting.")
            sys.exit(1)

        repo_name = input("[?] Enter repository name [wohi2-course-project]: ").strip() or "wohi2-course-project"
        db_name = input("[?] Enter database name [MyDb]: ").strip() or "MyDb"
        mysql_user = input("[?] Enter desired Database username: ").strip()
        mysql_pass = getpass.getpass("[?] Enter desired Database password: ").strip()
        
        if not mysql_user or not mysql_pass:
            print("\n[!] Database credentials are required. Exiting.")
            sys.exit(1)

        # --- Execution Logic ---
        run_command("sudo apt update")
        run_command("sudo apt upgrade -y")
        run_command(f"sudo apt install -y nodejs npm net-tools {db_packages} ufw nano")

        print("\n[i] Configuring Firewall and Database service...")
        run_command("sudo ufw allow 3000/tcp", allow_fail=True)
        run_command(f"sudo service {db_service} start")

        mysql_setup_query = f"""
        DROP DATABASE IF EXISTS test;
        DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
        CREATE DATABASE IF NOT EXISTS {db_name};
        CREATE USER IF NOT EXISTS '{mysql_user}'@'localhost' IDENTIFIED BY '{mysql_pass}';
        GRANT ALL PRIVILEGES ON *.* TO '{mysql_user}'@'localhost' WITH GRANT OPTION;
        FLUSH PRIVILEGES;
        """
        subprocess.run(["sudo", "mysql", "-u", "root"], input=mysql_setup_query.encode('utf-8'), check=True)

        # --- Folder Setup ---
        home_dir = os.path.expanduser("~")
        app_base_dir = f"{home_dir}/src/github.com/{github_username}"
        project_dir = f"{app_base_dir}/{repo_name}"
        run_command(f"mkdir -p {app_base_dir}")
        
        if not os.path.exists(project_dir):
            run_command(f"git clone https://github.com/{github_username}/{repo_name}", cwd=app_base_dir)

        # --- ENV and Launch ---
        with open(f"{project_dir}/.env", "w") as f:
            f.write(f'DATABASE_URL="mysql://{mysql_user}:{mysql_pass}@localhost:3306/{db_name}"\n')

        run_command("npm install", cwd=project_dir)
        run_command("npx prisma generate", cwd=project_dir)
        run_command("npx prisma migrate deploy", cwd=project_dir)
        run_command("npx prisma db seed", cwd=project_dir)
        
        print(f"\n[+] Setup complete! Starting server from {project_dir}...")
        print("[i] Press CTRL+C to stop the server.")
        run_command("npm run start", cwd=project_dir)

    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user. Exiting cleanly...")
        sys.exit(0)

if __name__ == "__main__":
    main()