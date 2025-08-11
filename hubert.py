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

audio_path = "output.wav"  # Replace with your audio file
waveform, sampling_rate = torchaudio.load(audio_path)
if sampling_rate != 16000:
    # Resample if needed
    resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=16000)
    waveform = resampler(waveform)

print(waveform.shape)  # Should be [1, T] for mono audio

# 3. Prepare Input for Model
input_values = processor(waveform.squeeze(0), sampling_rate=16000, return_tensors="pt").input_values
print(type(input_values))
print(input_values.shape)
input_values = torch.squeeze(input_values)  # Remove the batch dimension

# 4. Get Logits (Model Output)
with torch.no_grad():
    logits = model(input_values[0].reshape(1, -1)).logits

# 5. Decode Logits to Text
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.decode(predicted_ids)

print(transcription)

# retrieve logits
# logits = model(input_values).logits

# take argmax and decode
# predicted_ids = torch.argmax(logits, dim=-1)
# transcription = processor.batch_decode(predicted_ids)

