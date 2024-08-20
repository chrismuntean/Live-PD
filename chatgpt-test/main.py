import os

def run_op25():
    # Set the frequency and other parameters
    frequency = 774.41875e6  # Frequency in Hz
    sample_rate = 960000  # Sample rate in samples per second
    ppm = 0  # Frequency correction (ppm)
    gain = 'auto'  # Gain setting for the RTL-SDR
    
    # Command to run OP25 with the specified parameters
    cmd = (
        f"../op25/rx.py --args 'rtl' "
        f"-f {frequency} "
        f"-o 14 "
        f"-S {sample_rate} "
        f"-q {ppm} "
        f"-T trunk.tsv "
        f"-V -2 -U 2> stderr.2"
    )
    
    # Execute the command
    os.system(cmd)

if __name__ == "__main__":
    run_op25()