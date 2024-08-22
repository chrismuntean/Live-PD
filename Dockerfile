# Use a Raspberry Pi compatible base image
FROM balenalib/raspberrypi3-debian:latest

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y \
    cmake \
    build-essential \
    libusb-1.0-0-dev \
    libliquid-dev \
    python3-numpy \
    python3-scipy \
    git \
    rtl-sdr \
    wget \
    gnuradio \
    python3-pip \
    sox \
    alsa-utils

# Clone the OP25 repository
RUN git clone https://github.com/boatbod/op25 /op25

# Build OP25
RUN mkdir -p /op25/build && \
    cd /op25/build && \
    cmake ../ && \
    make && \
    make install

# Expose the port for the web interface
EXPOSE 8080

# Create a directory for output files
RUN mkdir /op25/output

# Command to run OP25 and start recording
CMD ["/bin/bash", "-c", "\
    /op25/gr-op25_repeater/apps/rx.py \
    --args 'rtl=0' \
    -N 'LNA:47' \
    -f 774.41875e6 \
    -o 24000 \
    -q 1 \
    -T /op25/trunk.tsv \
    -V -U -l http:0.0.0.0:8080 \
    -2 -w /op25/output/output.wav"]