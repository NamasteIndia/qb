import subprocess
import sys
import os

def run_command(command, cwd=None, shell=False):
    print(f"Running command: {' '.join(command) if isinstance(command, list) else command}")
    result = subprocess.run(command, cwd=cwd, shell=shell)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(command) if isinstance(command, list) else command}")
        sys.exit(1)

def install_dependencies():
    print("Updating package lists...")
    run_command(['sudo', 'apt-get', 'update'])
    
    print("Installing build dependencies...")
    deps = [
        'build-essential',
        'pkg-config',
        'qttools5-dev-tools',
        'qttools5-dev',
        'qtbase5-dev',
        'qtbase5-private-dev',
        'qtdeclarative5-dev',
        'libqt5svg5-dev',
        'libboost-all-dev',
        'libssl-dev',
        'zlib1g-dev',
        'liblzma-dev',
        'libgeoip-dev',
        'libtorrent-rasterbar-dev',
        'git',
        'cmake',
        'ninja-build',
    ]
    run_command(['sudo', 'apt-get', 'install', '-y'] + deps)

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        print(f"Directory {clone_dir} already exists. Pulling latest changes...")
        run_command(['git', 'pull'], cwd=clone_dir)
    else:
        print(f"Cloning repository {repo_url} into {clone_dir}...")
        run_command(['git', 'clone', repo_url, clone_dir])

def build_and_install_qbittorrent(clone_dir):
    build_dir = os.path.join(clone_dir, "build")

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    print("Configuring build with CMake...")
    # Use cmake with ninja generator for faster build
    run_command([
        'cmake',
        '-G', 'Ninja',
        '-DRUN_UNITTESTS=OFF',
        '-DENABLE_GUI=OFF',
        '..'
    ], cwd=build_dir)

    print("Building qBittorrent-nox...")
    run_command(['ninja'], cwd=build_dir)

    print("Installing qBittorrent-nox...")
    run_command(['sudo', 'ninja', 'install'], cwd=build_dir)

def main():
    repo_url = "https://github.com/qbittorrent/qBittorrent.git"
    clone_dir = os.path.expanduser("~/qBittorrent")

    install_dependencies()
    clone_repo(repo_url, clone_dir)
    build_and_install_qbittorrent(clone_dir)

    print("qBittorrent-nox installation completed successfully.")
    print("You can now run 'qbittorrent-nox' from the terminal.")

if __name__ == "__main__":
    main()