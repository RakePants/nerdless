from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import csv

tokenizer = AutoTokenizer.from_pretrained("sismetanin/rubert-toxic-pikabu-2ch")
model = AutoModelForSequenceClassification.from_pretrained("sismetanin/rubert-toxic-pikabu-2ch")


def get_toxicity(input):
    inputs = tokenizer(input, return_tensors="pt")
    
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    tox_score = logits.softmax(dim=-1).tolist()[1]
    return round(tox_score, 3)


with open('dialogues/raw/chan_dialogues.txt', encoding="utf8") as f:
    with open('dialogues/scored/chan_dialogues_scored_tox.csv', 'w', encoding="utf8") as csv_f:
        
        writer = csv.writer(csv_f)
        dialogue = f.read().split('\n\n\n\n')
        
        for lines_list in dialogue:
            
            lines_list = [line.strip() for line in lines_list.split('- ')[1:]]
            tox_score = round(get_toxicity(lines_list[1]), 3)
                
            if tox_score > 0.93:
                writer.writerow(lines_list[:2])
                               
print('Done')
