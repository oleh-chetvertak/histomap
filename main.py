import json
import folium
from cluster import Cluster
from request_gpt import RequestGPT

world_map = folium.Map()

filename = "assets/Хмельниччина.txt"
request_asking = '''
Проаналізуй наступний текст та перерахуй кожну згадану країну разом із конкретними датами або часовими періодами, пов'язаними з кожною згадкою. Там, де у тексті згадується про цю країну, створи контекст. Також надай координати країни, прив'язані до дати. Формат відповіді (JSON):
{"loc_name": "назва", "loc_coords": "{float широта}, {float довгота}", "date": "дата", "context": "контекст"}
Відповідай ВИКЛЮЧНО по наданому формату
Текст: '''


def RequestCluster(cluster):
    request_content = request_asking + cluster
    completion = RequestGPT("gpt-4o-mini", "user", request_content)
    try:
        response = completion.choices[0].message.content.split("\n")
        response = ''.join(response[1:len(response)-1])
        response = json.loads(response)
    except:
        print("request failed")
        response = []
    return response


Cluster(filename)
markers_list = []
with open("output.txt", encoding="UTF-8") as file:
    cluster_list = file.read().split("\n\n")
for cluster in cluster_list:
    cluster_data_list = RequestCluster(cluster)
    for data in cluster_data_list:
        print(data)
        html = f"""
            <h1>{data["loc_name"]}</h1>
            <p>{data["date"]}</p>
            <p>{data["context"]}</p>
        """
        exists = False
        for i in range(len(markers_list)):
            if markers_list[i]["coords"] == data["loc_coords"]:
                markers_list[i]["html"] += "\n" + html
                print(markers_list[i]["html"])
                exists = True
                break
        if not exists:
            marker_data = {"html": html, "coords": data["loc_coords"]}
            markers_list.append(marker_data)
    for marker in markers_list:
        popup = folium.Popup(
            html=marker["html"], max_width=250, max_height=500)
        folium.Marker(list(map(float, marker["coords"].split(", "))),
                      popup=popup).add_to(world_map)
world_map.show_in_browser()
