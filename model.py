import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, AutoModel, Wav2Vec2FeatureExtractor
import numpy as np
from labels import get_label
from exceptions import UncertaintyError


def speech_file_to_array_fn(path, sampling_rate):
    speech_array, _sampling_rate = torchaudio.load(path)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech = resampler(speech_array).squeeze().numpy()
    return speech


def predict(path, sampling_rate):
    speech = speech_file_to_array_fn(path, sampling_rate)
    inputs = feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
    inputs = {key: inputs[key].to(device) for key in inputs}

    with torch.no_grad():
        logits = model_(**inputs).logits

    scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    outputs = [{"Emotion": config.id2label[i], "Score": f"{round(score * 100, 3):.1f}"} for i, score in enumerate(scores)]
    return outputs


def get_emotion(path, sampling_rate):
    prediction = predict(path, sampling_rate)
    prediction_sorted = sorted(prediction, key=lambda x: float(x['Score']), reverse=True)

    if float(prediction_sorted[0]['Score']) < 55:
        raise UncertaintyError('Я Вас не понял, повторите, пожалуйста.')

    return get_label(prediction_sorted[0]['Emotion'])


TRUST = True

config = AutoConfig.from_pretrained('Aniemore/wav2vec2-xlsr-53-russian-emotion-recognition', trust_remote_code=TRUST)
model_ = AutoModel.from_pretrained("Aniemore/wav2vec2-xlsr-53-russian-emotion-recognition", trust_remote_code=TRUST)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("Aniemore/wav2vec2-xlsr-53-russian-emotion-recognition")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_.to(device)