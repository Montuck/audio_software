import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
from numpy import fft
import numpy as np
import matplotlib.pyplot as plt

class AudioAnalyzer:
    def __init__(self):
        self.fs = 44100  # Sample rate
        self.seconds = 3  # Duration of recording
        self.data = None # placeholder for audio data


    def capture_audio(self):
        print("Recording...")
        myrecording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', self.fs, myrecording)  # Save as WAV file
        print("Recording finished")

    def extract_data(self):
        filename = 'output.wav'
        # Extract data and sampling rate from file
        self.data, self.fs = sf.read(filename, dtype='float32')  

    def play_audio(self):
        print("Playing back...")
        sd.play(self.data, self.fs)
        status = sd.wait()  # Wait until file is done playing
        print("Playback finished")
        return status

    def plot_data(self):
        mono_data = self.data[:, 0]

        fig, ax = plt.subplots(3, 1, figsize=(10, 8))
        print("Analyzing the audio data...")

        print("Plotting the time domain signal...")
        # plot the time domain signal
        ax[0].plot(np.arange(0,len(mono_data)), mono_data)
        ax[0].set_title("Time Domain Signal")
        ax[0].set_xlabel("Sample Number")
        ax[0].set_ylabel("Amplitude")
        ax[0].grid()

        print("Plotting the frequency spectrum...")
        # get the fft
        data_fft = fft.fft(mono_data)
        # get the frequencies
        frequencies = fft.fftfreq(len(data_fft), 1/self.fs)

        # plot the fft
        ax[1].plot(frequencies, np.abs(data_fft))
        ax[1].set_title("FFT of Recorded Audio")
        ax[1].set_xlabel("Frequency(Hz)")
        ax[1].set_ylabel("Magnitude")
        ax[1].grid()

        print("Spectrogram of the audio signal...")
        ax[2].specgram(mono_data, Fs=self.fs, NFFT=1024, noverlap=512)
        ax[2].set_title("Spectrogram of Recorded Audio")
        ax[2].set_xlabel("Time (s)")
        ax[2].set_ylabel("Frequency (Hz)")

        # plt.tight_layout()
        # plt.savefig('audio_analysis.png')
        # plt.show()
        print("Plotting finished")
        return fig, ax



# Only run this if the script is executed directly (not imported)
if __name__ == "__main__":
    # This code only runs when you run analyzer.py directly
    print("Running analyzer in standalone mode...")
    analyzer = AudioAnalyzer()
    analyzer.capture_audio()
    analyzer.extract_data()
    analyzer.play_audio()
    analyzer.plot_data()
    print("Analysis complete!")