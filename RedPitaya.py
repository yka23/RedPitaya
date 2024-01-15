# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
import redpitaya_scpi as scpi
import time
import numpy as np

IP = 'rp-f0b8f4.local'
rp = scpi.scpi(IP)

# Configure the analog input channel
rp.tx_txt(f"ACQ:SOUR{analog_input_channel}:GAIN LV")
rp.tx_txt(f"ACQ:SOUR{analog_input_channel}:DATA:START?")
start_idx = int(rp.rx_txt())
rp.tx_txt(f"ACQ:SOUR{analog_input_channel}:DATA:STOP?")
stop_idx = int(rp.rx_txt())

# Read noise from the analog input channel
rp.tx_txt(f"ACQ:SOUR{analog_input_channel}:DATA?")
data_str = rp.rx_txt()
data = np.fromstring(data_str, dtype=np.int16, sep=',')

# Extract a segment of the data as random numbers
random_numbers = data[start_idx:stop_idx]

# Print the random numbers
print("Random Numbers:", random_numbers)

# Disconnect from Red Pitaya
rp.close()
