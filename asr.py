from datasets import load_dataset, Audio

minds = load_dataset("PolyAI/minds14", name="en-US", split="train[:100]")

print(minds.column_names)

minds = minds.train_test_split(test_size=0.2)

minds = minds.remove_columns(["english_transcription", "intent_class", "lang_id"])

print(minds["train"][0])

minds = minds.cast_column("audio", Audio(sampling_rate=16_000))
print(minds["train"][0])

def upper_case(example):
    return {"transcription": example["transcription"].upper()}

minds = minds.map(upper_case)
