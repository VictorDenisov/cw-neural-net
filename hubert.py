# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
#
# from datasets import load_dataset
#
# model_name = "facebook/wav2vec2-base"
# Wav2Vec2Processor.from_pretrained(model_name)
#
# #timit = load_dataset("timit_asr")
# ds = load_dataset("lhoestq/demo1")

from transformers import AutoProcessor, HubertForCTC
from datasets import load_dataset
import torch
import torchaudio

# load model and tokenizer
model = HubertForCTC.from_pretrained("facebook/hubert-large-ls960-ft")
processor = AutoProcessor.from_pretrained("facebook/hubert-large-ls960-ft")
 
# load dummy dataset and read soundfiles
# ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
# ds = load_dataset("lhoestq/demo1", split="test")
#
# print(ds)

# tokenize
#input_values = processor(ds[0]["audio"]["array"], return_tensors="pt", padding="longest").input_values  # Batch size 1

audio_path = "M_0025_11y10m_1.wav"  # Replace with your audio file
waveform, sampling_rate = torchaudio.load(audio_path)
if sampling_rate != 16000:
    # Resample if needed
    resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=16000)
    waveform = resampler(waveform)

print(waveform.shape)  # Should be [1, T] for mono audio

# 3. Prepare Input for Model
input_values = processor(waveform.squeeze(0), sampling_rate=16000, return_tensors="pt", padding="longest").input_values
print(f"Type of input values: {type(input_values)}")
print(f"Input values shape: {input_values.shape}")
input_values = torch.squeeze(input_values)  # Remove the batch dimension

input_values_reshaped = input_values.reshape(1, -1)  # Reshape to add batch dimension back
print(f"Reshaped input values shape: {input_values_reshaped.shape}")

# 4. Get Logits (Model Output)
with torch.no_grad():
    logits = model(input_values_reshaped).logits

# 5. Decode Logits to Text
print(f"Logits shape: {logits.shape}")
predicted_ids = torch.argmax(logits, dim=-1)
print(f"Predicted IDs shape: {predicted_ids.shape}")
squeezed_predicted_ids = torch.squeeze(predicted_ids)  # Remove batch dimension for decoding
print(f"Squeed Predicted IDs shape: {squeezed_predicted_ids.shape}")
transcription = processor.decode(squeezed_predicted_ids)

print(f"Transcription: {transcription}")

# retrieve logits
# logits = model(input_values).logits

# take argmax and decode
# predicted_ids = torch.argmax(logits, dim=-1)
# transcription = processor.batch_decode(predicted_ids)

