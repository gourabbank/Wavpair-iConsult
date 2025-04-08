import librosa
import numpy as np

def extract_mfcc(file_path, n_mfcc=13):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    # Average MFCCs over time
    mfcc_mean = np.mean(mfcc, axis=1)
    return mfcc_mean.tolist()
