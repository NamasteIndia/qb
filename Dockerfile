# Use an official Ubuntu LTS base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-setuptools python3-dev \
    build-essential pkg-config qttools5-dev-tools qttools5-dev qtbase5-dev qtbase5-private-dev qtdeclarative5-dev libqt5svg5-dev \
    libboost-all-dev libssl-dev zlib1g-dev liblzma-dev libgeoip-dev libtorrent-rasterbar-dev git cmake ninja-build \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the Python install script into the container
COPY install_qbittorrent_nox.py /app/install_qbittorrent_nox.py

# Run the Python install script to clone, build, and install qBittorrent-nox
RUN python3 install_qbittorrent_nox.py

# Expose default port for qBittorrent Web UI
EXPOSE 8080

# By default run qbittorrent-nox
CMD ["qbittorrent-nox", "--webui-port=8080", "--profile=/config"]