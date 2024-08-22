# Use an x86_64 compatible base image
FROM debian:latest

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.11/dist-packages:/usr/lib/python3.11/dist-packages:/op25/op25/gr-op25_repeater/apps/tdma

# Update and install basic dependencies
RUN apt-get update && \
    apt-get install -y \
    sudo \
    cmake \
    git \
    wget \
    rtl-sdr \
    python3-pip \
    build-essential \
    python3-numpy \
    gnuradio \
    swig \
    libtool \
    autoconf \
    automake

# Clone the OP25 repository and switch to the gr310 branch
RUN git clone https://github.com/boatbod/op25 /op25 && \
    cd /op25 && \
    git checkout gr310

# Modify the import in the rx.py script to use op25_repeater
RUN sed -i 's/import gnuradio.op25 as op25/import gnuradio.op25_repeater as op25/' /op25/op25/gr-op25_repeater/apps/rx.py

# Build and install OP25
RUN cd /op25/op25/gr-op25_repeater && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    ldconfig

# Expose the port for the web interface
EXPOSE 8080

# Create a directory for output files
RUN mkdir /op25/output

# Command to run OP25 and start recording
CMD ["/bin/bash", "-c", "\
    /op25/op25/gr-op25_repeater/apps/rx.py \
    --args 'rtl=0' \
    -N 'LNA:47' \
    -f 774.41875e6 \
    -o 24000 \
    -q 1 \
    -T /op25/trunk.tsv \
    -V -U -l http:0.0.0.0:8080 \
    -2 -w /op25/output/output.wav"]