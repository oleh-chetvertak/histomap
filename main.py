import spacy
import re

nlp_spacy = spacy.load("uk_core_news_sm")

filename = "assets/Хмельниччина.txt"
with open(filename, encoding="UTF-8", mode="r") as file:
    raw_text = file.read()
raw_text = re.sub("\n", "", raw_text)

doc = nlp_spacy(raw_text)
sent_list = list(doc.sents)
locations_ukrainian_contexts = []
prev = -1000

doc = nlp_spacy(raw_text)
sent_list = list(doc.sents)
locations_ukrainian_contexts = []
prev = -1000

for i, sent in enumerate(sent_list):
    for ent in sent.ents:
        if ent.label_ == "LOC":
            # Calculate context window indices
            first_pointer = max(0, i - 1)
            second_pointer = min(len(sent_list) - 1, i + 2)

            # If the current location is close to the previous one, extend the last context window
            if i - prev <= 4:
                print(i, prev)
                # Convert range to set to avoid duplicates
                locations_ukrainian_contexts[-1].update(
                    range(first_pointer, second_pointer + 1))
            else:
                # Otherwise, create a new context window with a set
                locations_ukrainian_contexts.append(
                    set(range(first_pointer, second_pointer + 1)))

            prev = i
            break

# Optional: Convert sets back to sorted lists
locations_ukrainian_contexts = [
    sorted(context) for context in locations_ukrainian_contexts]

print(locations_ukrainian_contexts)
with open("output.txt", "w", encoding="UTF-8") as f:
    for loc in locations_ukrainian_contexts:
        text = ""
        for sind in loc:
            text += sent_list[sind].text + " "
        text += "\n\n"
        f.write(text)
