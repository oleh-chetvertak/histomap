import spacy
import re
import translators as ts
from geopy.geocoders import Nominatim
import plotly.express as px

nlp_spacy = spacy.load("uk_core_news_sm")
geolocator = Nominatim(user_agent='mapper')

filename = "Хмельниччина.txt"
with open(filename, encoding="UTF-8", mode="r") as file:
    raw_text = file.read()
raw_text = re.sub("\n", ".", raw_text)

doc = nlp_spacy(raw_text)
sent_list = list(doc.sents)
locations_ukrainian_sent_ids = set()
for i in range(len(sent_list)):
    sent = sent_list[i]
    for ent in sent.ents:
        if ent.label_ == "LOC":
            if i == 0:
                upd = [i, i+1]
            elif i == len(sent_list) - 1:
                upd = [i-1, i]
            else:
                upd = [i-1, i, i+1]
            locations_ukrainian_sent_ids.update(upd)
            break
print(locations_ukrainian_sent_ids)
prev = 1000
with open("output.txt", "w", encoding="UTF-8") as f:
    for i in locations_ukrainian_sent_ids:
        text = ""
        if i - prev > 2:
            text += f"\n{i, prev}\n"
        text += f"{i} " + sent_list[i].text + " "
        f.write(text)
        prev = i

# df = {
#     "lat": [],
#     "lon": []
# }
# for location in locations_ukrainian_lemmatized:
#     location_translated = ts.translate_text(location, to_language="en")
#     print(f"{location}\t{location_translated}")

#     location_marked = geolocator.geocode(
#         location_translated, addressdetails=True, exactly_one=True)
#     print(location_marked)
#     if location_marked:
#         df["lat"].append(location_marked.latitude)
#         df["lon"].append(location_marked.longitude)
# print(df)
