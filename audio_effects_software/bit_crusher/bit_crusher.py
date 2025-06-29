import numpy as np
import sounddevice as sd
import time
import pyaudio

def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2*np.pi*frequency*t)
    return tone

def play_tone(tone, sample_rate=44100):
    sd.play(tone, samplerate=sample_rate)
    sd.wait()

def bit_crusher(audio, bit_depth=8):
    #### Copilot's Version ####
    # max_val = 2 ** (bit_depth - 1) - 1
    # min_val = -max_val
    # #scaling
    # tone_scaled = np.clip(tone * max_val, min_val, max_val)
    # # quantization
    # tone_quantized = np.round(tone_scaled) / max_val
    # return tone_quantized

    #### Claude's Version ####
    # Calculate the number of quantization levels
    levels = 2 ** bit_depth
    
    # Quantize the audio
    # Scale to use full range of quantization levels
    scaled = audio * (levels // 2 - 1)
    quantized = np.round(scaled)
    
    # Scale back to [-1, 1] range
    crushed = quantized / (levels // 2 - 1)
    
    # Clamp to prevent overflow
    crushed = np.clip(crushed, -1.0, 1.0)
    
    return crushed

def main():
    # set parameters
    #frequency = float(input("Enter frequency to play in (Hz): "))
    #duration = float(input("Enter duration to play for (seconds): "))
    sample_rate = 22e3
    frequency = 440.0  # A4 note
    duration = 2.0  # seconds

    # generate and play tone
    tone = generate_tone(frequency, duration, sample_rate)
    tone_crushed = bit_crusher(tone, bit_depth=4)
    print("Playing original tone...")
    play_tone(tone, sample_rate)
    print("Done...\nTerminating...")

    print("Playing original tone...")
    play_tone(tone_crushed, sample_rate)
    print("Done...\nTerminating...")

if __name__="__main__"
