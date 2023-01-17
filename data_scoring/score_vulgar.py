from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import csv

tokenizer = AutoTokenizer.from_pretrained("apanc/russian-sensitive-topics")
model = AutoModelForSequenceClassification.from_pretrained("apanc/russian-sensitive-topics")


def get_vulgarity(input):
    inputs = tokenizer(input, return_tensors="pt")
    
    with torch.no_grad():
        logits = model(**inputs).logits[0]
        
    vulgarity_scores = [logits.softmax(dim=-1).tolist()[5], logits.softmax(dim=-1).tolist()[6], logits.softmax(dim=-1).tolist()[31]]
    return [round(score, 3) for score in vulgarity_scores]


with open('dialogues/raw/chan_dialogues.txt', encoding="utf8") as f:
    with open('dialogues/scored/chan_dialogues_scored_vulgar.csv', 'w', encoding="utf8") as csv_f:
        
        writer = csv.writer(csv_f)
        dialogue = f.read().split('\n\n\n\n')
        for lines_list in dialogue:
            
            lines_list = [line.strip() for line in lines_list.split('- ')[1:]]
            vulgarity_scores = get_vulgarity(lines_list[1])   
            
            #choose line if at least one of 3 labels is > 0.4
            if any(score > 0.4 for score in vulgarity_scores):
                writer.writerow(lines_list[:2])
                                              
print('Done')
