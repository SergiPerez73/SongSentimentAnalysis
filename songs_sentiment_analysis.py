import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pandas as pd
import time

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")


def analyze_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    logits_list = logits.tolist()[0]
    return logits_list[0], logits_list[1]

def analyze_songs(name):
    df = pd.read_csv(name+'.csv')

    score_positive = []
    score_negative = []


    for i in range(df.shape[0]):
        count_sentences = 0
        total_neg = 0
        total_pos = 0
        for sentence in df.loc[i,'lyrics'].split('\n'):
            if sentence != '':
                neg, pos = analyze_sentence(sentence)
                sentiment = torch.softmax(torch.tensor([neg,pos]),dim=0).tolist()
                total_neg += sentiment[0]
                total_pos += sentiment[1]
                count_sentences += 1
        print(i)
        time.sleep(1)
        score_negative.append(total_neg/count_sentences)
        score_positive.append(total_pos/count_sentences)

    scores_data = {
        'score_negative' : score_negative,
        'score_positive' : score_positive,
    }

    scores = pd.DataFrame(scores_data)

    df = pd.concat([df,scores],axis=1)
    df = df.sort_values(by=['year'],  ascending=True)
    df = df.drop(['lyrics','url'], axis=1)
    df.to_csv(name+'-scores.csv')

if __name__ == "__main__":
    group= 'eminem'
    
    analyze_songs(group)

