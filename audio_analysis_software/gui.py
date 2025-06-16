import analyzer
import nicegui
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft

################################################# analyzer object #################################################

audio_analyzer = analyzer.AudioAnalyzer()
plot_container = None

############################################## Functions ##################################################

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

def update_seconds(event: ValueChangeEventArguments):
    try:
        audio_analyzer.seconds = int(event.value)
        ui.notify(f'Capture time set to: {event.value} seconds')
    except ValueError:
        ui.notify('Please enter a valid number for seconds')

def update_sample_rate(event: ValueChangeEventArguments):
    audio_analyzer.fs = event.value
    ui.notify(f'Sample rate set to: {event.value} Hz')

def update_plot():
    global plot_container
    
    ui.notify('Generating plots...')

    plt.close('all')
    
    try:
        # Check if data exists
        if not hasattr(audio_analyzer, 'data') or audio_analyzer.data is None:
            ui.notify('No audio data available. Please capture and extract data first.')
            return
        
        # Clear the previous plot container content
        plot_container.clear()
        
        mono_data = audio_analyzer.data[:, 0]
        
        # Create matplotlib plot inside the existing container
        with plot_container:
            with ui.matplotlib(figsize=(12, 10)).figure as fig:
                ax = fig.subplots(3, 1)

                # Plot the time domain signal
                ax[0].plot(np.arange(0, len(mono_data)), mono_data)
                ax[0].set_title("Time Domain Signal")
                ax[0].set_xlabel("Sample Number")
                ax[0].set_ylabel("Amplitude")
                ax[0].grid()

                print("Plotting the frequency spectrum...")
                # Get the FFT
                data_fft = fft.fft(mono_data)
                # Get the frequencies
                frequencies = fft.fftfreq(len(data_fft), 1/audio_analyzer.fs)

                # Plot the FFT (only positive frequencies for clarity)
                positive_freq_idx = frequencies >= 0
                ax[1].plot(frequencies[positive_freq_idx], np.abs(data_fft[positive_freq_idx]))
                ax[1].set_title("FFT of Recorded Audio")
                ax[1].set_xlabel("Frequency (Hz)")
                ax[1].set_ylabel("Magnitude")
                ax[1].grid()
                ax[1].set_xlim(0, 20e3)

                print("Spectrogram of the audio signal...")
                ax[2].specgram(mono_data, Fs=audio_analyzer.fs, NFFT=1024, noverlap=512)
                ax[2].set_title("Spectrogram of Recorded Audio")
                ax[2].set_xlabel("Time (s)")
                ax[2].set_ylabel("Frequency (Hz)")
                
                fig.tight_layout()
        
        ui.notify('Plots generated successfully!')
        
    except Exception as e:
        ui.notify(f'Error generating plots: {str(e)}')
        print(f"Plot error details: {e}")

def capture_with_notification():
    ui.notify('Recording...')
    try:
        audio_analyzer.capture_audio()
        ui.notify('Recording completed!')
    except Exception as e:
        ui.notify(f'Recording failed: {str(e)}')

def extract_with_notification():
    ui.notify('Extracting wave data...')
    try:
        audio_analyzer.extract_data()
        ui.notify('Wave data extracted successfully!')
    except Exception as e:
        ui.notify(f'Data extraction failed: {str(e)}')

def play_with_notification():
    ui.notify('Playing back...')
    try:
        audio_analyzer.play_audio()
        ui.notify('Playback started!')
    except Exception as e:
        ui.notify(f'Playback failed: {str(e)}')

################################################# GUI ####################################################
ui.label("Audio Analyzer").style('font-size: 24px; font-weight: bold;')  

with ui.row():
    # Instructions for user
    with ui.card():
        ui.label("Instructions").style('font-size: 18px; font-weight: bold;')
        ui.label("1. Set your desired capture time and sample rate")
        ui.label("2. Click 'Capture Audio' to record")
        ui.label("3. Click 'Extract Data' to process the recording")
        ui.label("4. Click 'Plot Data' to visualize the results")
        ui.label("5. Click 'Play Audio' to hear the recording")
    # Settings for capture time and sample rate
    with ui.card():
        ui.label("Settings").style('font-size: 18px; font-weight: bold;')
        ui.input('Capture Time (seconds)', value=str(audio_analyzer.seconds), on_change=update_seconds)
        ui.select([8000, 16000, 44100, 48000], value=audio_analyzer.fs, on_change=update_sample_rate, label='Sample Rate (Hz)')      


with ui.row():
    # Main controls for audio analysis
    with ui.column():  
        with ui.card():
            ui.label("Controls").style('font-size: 18px; font-weight: bold;')
            ui.button("Capture Audio", on_click=capture_with_notification).props('color=primary')
            ui.button("Extract Data", on_click=extract_with_notification).props('color=secondary')
            ui.button("Play Audio", on_click=play_with_notification).props('color=positive')
            ui.button("Plot Data", on_click=update_plot).props('color=accent')

# Create a dedicated container for plots
ui.label("Audio Analysis Plots").style('font-size: 18px; font-weight: bold; margin-top: 20px;')
plot_container = ui.column()

# Run the GUI
ui.run()