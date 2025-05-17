from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from datasets import load_dataset

model_name = "facebook/wav2vec2-base"
Wav2Vec2Processor.from_pretrained(model_name)

#timit = load_dataset("timit_asr")
ds = load_dataset("lhoestq/demo1")
