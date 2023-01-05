from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import csv

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2-cedr-emotion-detection")
model = AutoModelForSequenceClassification.from_pretrained("cointegrated/rubert-tiny2-cedr-emotion-detection")


def get_sadness(input):
    inputs = tokenizer(input, return_tensors="pt")
    
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    tox_score = logits.softmax(dim=-1).tolist()[2]
    return round(tox_score, 3)


with open('dialogues/raw/chan_dialogues.txt', encoding="utf8") as f:
    with open('dialogues/scored/chan_dialogues_scored_sad.csv', 'w', encoding="utf8") as csv_f:
        
        writer = csv.writer(csv_f)
        dialogue = f.read().split('\n\n\n\n')
        
        for lines_list in dialogue:
            
            lines_list = [line.strip() for line in lines_list.split('- ')[1:]]
            sad_score = get_sadness(lines_list[1])
                
            if sad_score > 0.8:
                writer.writerow(lines_list[:2])
                               
print('Done')
