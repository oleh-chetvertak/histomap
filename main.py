import spacy
import re

nlp_spacy = spacy.load("uk_core_news_sm")

filename = "assets/Омріяний Рим.txt"
with open(filename, encoding="UTF-8", mode="r") as file:
    raw_text = file.read()
raw_text = re.sub("\n", "", raw_text)

doc = nlp_spacy(raw_text)
sent_list = list(doc.sents)
locations_ukrainian_contexts = []
prev = -3
for i in range(len(sent_list)):
    sent = sent_list[i]
    for ent in sent.ents:
        if ent.label_ == "LOC":
            length = len(locations_ukrainian_contexts)
            if i - prev <= 2:
                second_pointer = i + 2 if i != length-1 else length-1
                locations_ukrainian_contexts[length -
                                             2].extend(sent_list[prev + 1:second_pointer])
            else:
                first_pointer = i-1 if i != 0 else 0
                second_pointer = i+2 if i != length-1 else length-1
                locations_ukrainian_contexts.append(
                    sent_list[first_pointer:second_pointer])
                prev = i
            break

with open("output.txt", "w", encoding="UTF-8") as f:
    for loc in locations_ukrainian_contexts:
        text = ""
        unique = set(loc)
        i = 0
        for s in unique:
            text += f"{i + 1} " + s.text + " "
            i += 1
        text += "\n\n"
        f.write(text)
