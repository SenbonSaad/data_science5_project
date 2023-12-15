import streamlit as st
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import io

def get_audio_characteristics(audio_file):
    try:
        audio = AudioSegment.from_file(audio_file, format=audio_file.name.split(".")[-1])
        characteristics = {
            "Channels": audio.channels,
            "Sample Width": audio.sample_width,
            "Frame Rate": audio.frame_rate,
            "Frame Width": audio.frame_width,
            "Length": len(audio),
            "Sample Width (Bytes)": audio.sample_width,
            "Sample Width (Bits)": audio.sample_width * 8,
            "Sample Rate": audio.frame_rate,
        }
    except Exception as e:
        characteristics = {"Error": str(e)}
    return audio, characteristics


def moving_average_plot(data_mono, ns, window_size):
    weights = np.repeat(1.0, window_size) / window_size
    moving_avg = np.convolve(data_mono, weights, 'valid')

    # Plotting
    time_values = np.linspace(0, ns, len(moving_avg))
    plt.plot(time_values, moving_avg)
    plt.xlabel('Time')
    plt.ylabel('Moving Average')
    plt.title('Moving Average Plot')
    st.pyplot(plt)

def apply_filter(data_mono, ns, filter_type, cutoff_freq):
    order = 4
    nyquist_freq = 0.5

    if filter_type == "Low-pass":
        b, a = butter(order, cutoff_freq, btype='low')
    elif filter_type == "High-pass":
        b, a = butter(order, cutoff_freq, btype='high')
    elif filter_type == "Band-pass":
        lowcut, highcut = cutoff_freq
        b, a = butter(order, [lowcut, highcut], btype='band')
    else:
        raise ValueError("Invalid filter type")

    filtered_data = lfilter(b, a, data_mono)
    return filtered_data

def plot_filtered_data(data_mono, filtered_data, filter_type):
    plt.subplot(211)
    plt.plot(data_mono)
    plt.title("Original Signal")

    plt.subplot(212)
    plt.plot(filtered_data)
    plt.title(f"{filter_type} Filtered Signal")

    plt.tight_layout()
    st.pyplot(plt)

##############################
def process_audio(audio_file):
    st.title("Audio Processing")
    st.audio(audio_file, format="audio/" + audio_file.name.split(".")[-1], start_time=0)

    audio, audio_characteristics = get_audio_characteristics(audio_file)
    st.subheader("Audio Characteristics")
    st.table(audio_characteristics)

    data_mono = np.array(audio.get_array_of_samples())
    ns = len(data_mono)

    # Display a selectbox for choosing between moving average and filtering
    display_option = st.selectbox("Choose Plot Type", ["Moving Average Plot", "Filtering Plot"])

    if display_option == "Moving Average Plot":
        st.header("Moving Average Plot")
        moving_average_plot(data_mono, ns, 100)
    elif display_option == "Filtering Plot":
        st.header("Filter Options")
        filter_type = st.radio("Select Filter Type", ["Low-pass", "High-pass", "Band-pass"])
        if filter_type == "Band-pass":
            lowcut = st.slider("Select Lower Cutoff Frequency", min_value=0.01, max_value=0.47, value=0.1)
            highcut = st.slider("Select Higher Cutoff Frequency", min_value=0.02, max_value=0.48, value=0.2)
            if lowcut == highcut or lowcut > highcut:
                st.warning("Invalid parameters : Lower cutoff frequency > higher cutoff frequency ")
                return
            cutoff_freq = [lowcut, highcut]
        else:
            cutoff_freq = st.slider("Select Cutoff Frequency", min_value=0.02, max_value=0.49, value=0.1)

        # Apply and plot the selected filter
        st.header(f"{filter_type} Filtered Signal")
        filtered_data = apply_filter(data_mono, ns, filter_type, cutoff_freq)
        plot_filtered_data(data_mono, filtered_data, filter_type)

        # Add a button to download the filtered audio as a WAV file
        if st.button("New Filtered Audio"):
            filtered_audio = AudioSegment(filtered_data.tobytes(), frame_rate=audio.frame_rate, sample_width=audio.sample_width, channels=audio.channels)
            with io.BytesIO() as buffer:
                filtered_audio.export(buffer, format="wav")
                buffer.seek(0)
                st.download_button(label="Download Filtered Audio", data=buffer, file_name="filtered_audio.wav", mime="audio/wav")