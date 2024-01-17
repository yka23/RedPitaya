# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python3

import sys
import redpitaya_scpi as scpi
import time
import numpy as np
import matplotlib.pyplot as plot
import struct
import random
import math
from collections import Counter


#%%
# =============================================================================
# Define functions
# =============================================================================

def calculate_entropy(binary_string):
    # Count the occurrences of each bit
    bit_counts = Counter(binary_string)

    # Calculate the probability of each bit
    total_bits = len(binary_string)
    probabilities = [count / total_bits for count in bit_counts.values()]

    # Calculate the Shannon entropy
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)

    return entropy



def entropy_amplification(binary_string1, binary_string2):
    # the two strings must have the same size
    if len(binary_string1) != len(binary_string2):
        raise ValueError("The two strings must have the same size")

    # Convert the binary strings to lists of characters
    binary_list1 = list(binary_string1)
    binary_list2 = list(binary_string2)

    # Perform XOR operation between corresponding bits
    amplified_list = [str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(binary_list1, binary_list2)]

    # Join the list back into a string
    amplified_string = ''.join(amplified_list)

    return amplified_string


def float_to_bits(float_list):
    binary_string = ""

    # Convert each float to its binary representation and concatenate to the binary_string
    for num in float_list:
        # Use struct.pack to convert the float to a bytes object
        # 'd' in the format string stands for double-precision floating-point
        binary_representation = struct.pack('d', num)

        # Use binascii.hexlify to convert the bytes object to a hexadecimal string
        hexadecimal_string = binary_representation.hex()

        # Convert the hexadecimal string to a binary string
        binary_string += bin(int(hexadecimal_string, 16))[2:]

    return binary_string


#%%
# =============================================================================
# Configure RedPitaya
# =============================================================================

IP = 'rp-f0b8f4.local'
rp_s = scpi.scpi(IP)


#%%
# =============================================================================
# Read the voltage noise on the RF input and convert it into a string of bits
# =============================================================================

rp_s.tx_txt('ACQ:RST')

rp_s.tx_txt('ACQ:DEC 4')
rp_s.tx_txt('ACQ:START')
rp_s.tx_txt('ACQ:TRIG NOW')

while 1:
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break

while 1:
    rp_s.tx_txt('ACQ:TRIG:FILL?')
    if rp_s.rx_txt() == '1':
        break

rp_s.tx_txt('ACQ:SOUR1:DATA?')
buff_string = rp_s.rx_txt()
buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
buff = list(map(float, buff_string))

binary_representation = float_to_bits(buff)



#%%
# =============================================================================
# Output the bitstream as high and low voltages from the RF output
# =============================================================================

bitstream='101010101010'
rf_output_channel = 1  # RF output channel

# Output the bitstream on the RF output channel
for bit in bitstream:
    voltage_level = 1.0 if bit == '1' else 0.0
    rp_s.tx_txt(f"ANALOG:PIN{rf_output_channel} {voltage_level}")

    # Add a delay if needed (adjust the sleep duration accordingly)
    time.sleep(0.1)

# Disconnect from Red Pitaya
rp_s.close()

#%%

output_channel = 1  # Replace with the desired output channel (1 or 2)
frequency = 1000  # Frequency of the sine wave in Hertz
amplitude = 1.0  # Amplitude of the sine wave in Volts

#rp_s.tx_txt(f"GEN:RST")

rp_s.tx_txt(f"SOUR{output_channel}:FUNC SIN")
rp_s.tx_txt(f"SOUR{output_channel}:FREQ:FIX {frequency}")
rp_s.tx_txt(f"SOUR{output_channel}:VOLT {amplitude}")

#Enable output
rp_s.tx_txt(f"OUTPUT{output_channel}:STATE ON")
rp_s.tx_txt('SOUR1:TRIG:INT')

#%%

output_channel = 1  # Replace with the desired output channel (1 or 2)
frequency = 2000  # Frequency of the sine wave in Hertz
amplitude = 1.0  # Amplitude of the sine wave in Volts

# Connect to Red Pitaya
rp = scpi.scpi(IP)

# Configure the output channel
rp.tx_txt(f"SOUR{output_channel}:FUNC SQU")
rp.tx_txt(f"SOUR{output_channel}:FREQ:FIX {frequency}")
rp.tx_txt(f"SOUR{output_channel}:VOLT {amplitude}")

# Enable the output
rp.tx_txt(f"OUTPUT{output_channel}:STATE ON")

# Wait for some time (you can adjust this based on your needs)
#time.sleep(25)

# Disable the output
#rp.tx_txt(f"OUTPUT{output_channel}:STATE OFF")

# Disconnect from Red Pitaya
#rp.close()

