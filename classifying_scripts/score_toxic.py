from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("sismetanin/rubert-toxic-pikabu-2ch")
model = AutoModelForSequenceClassification.from_pretrained("sismetanin/rubert-toxic-pikabu-2ch")

inputs = tokenizer("привет", return_tensors="pt")

with torch.no_grad():
    logits = model(**inputs).logits[0]

tox_score = logits.softmax(dim=-1).tolist()[1]
print('tox_score: ', tox_score)