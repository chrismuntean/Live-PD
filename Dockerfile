# Use an x86_64 compatible base image
FROM debian:latest

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    wget \
    rtl-sdr \
    python3-pip

# Clone the OP25 repository and switch to the gr310 branch
RUN git clone https://github.com/boatbod/op25 /op25 && \
    cd /op25 && \
    git checkout gr310

# Run the install.sh script to install dependencies and build OP25
RUN cd /op25 && \
    ./install.sh

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