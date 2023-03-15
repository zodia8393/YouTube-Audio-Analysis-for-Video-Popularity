import os
import pandas as pd
import numpy as np
import librosa

def extract_audio_features(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=True)

    stft = np.abs(librosa.stft(y))
    mel_spectrogram = librosa.feature.melspectrogram(S=stft, sr=sr)
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(mel_spectrogram), sr=sr)
    feature_means = np.mean(mfcc, axis=1)

    return feature_means

def preprocess_data(metadata):
    # Replace 'video_folder' and 'file_extension' with the appropriate values for your dataset
    video_folder = 'videos'
    file_extension = '.mp4'
    audio_features = []

    for index, row in metadata.iterrows():
        file_name = row['title']  # Replace with the appropriate file naming scheme
        file_path = os.path.join(video_folder, file_name + file_extension)

        try:
            features = extract_audio_features(file_path)
            audio_features.append(features)
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            audio_features.append(None)

    metadata['audio_features'] = audio_features
    return metadata
