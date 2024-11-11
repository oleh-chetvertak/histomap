import json
from cluster import Cluster
from request_gpt import RequestGPT
filename = "assets/Хмельниччина.txt"
request_asking = '''
Проаналізуй наступний текст та перерахуй кожну згадану країну разом із конкретними датами або часовими періодами, пов'язаними з кожною згадкою. Там, де у тексті згадується про цю країну, створи контекст. Також надай координати країни, прив'язані до дати. Формат відповіді (JSON):
{"loc_name": "назва", "loc_coords": "координати", "date": "дата", "context": "контекст"}
Текст: '''


def RequestCluster(cluster):
    request_content = request_asking + cluster
    completion = RequestGPT("gpt-4o-mini", "user", request_content)
    response = completion.choices[0].message.content.split("\n")
    response = ''.join(response[1:len(response)-1])
    response = json.loads(response)
    return response


Cluster(filename)
with open("output.txt", encoding="UTF-8") as file:
    cluster_list = file.read().split("\n\n")
print(RequestCluster(cluster_list[2]))
