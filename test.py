from bs4 import BeautifulSoup
import requests

# https://tracker.gg/valorant/profile/riot/Pran%23NA1/overview


def getUserURL(name, tag):
    url = "https://tracker.gg/valorant/profile/riot/{}%23{}/overview"
    url = url.format(name, tag)

    return url


url = getUserURL("Pran", "NA1")
url = "https://tracker.gg/valorant/profile/riot/al1eNNNNNNNNNNNN%23SWAGR/overview"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
# print(doc.prettify())
div_vals = doc.find_all("div", {"class": "value"})
span_stat_vals = doc.find_all("span")
span_vals = doc.find_all("span", {"class": "value"})

# print(div_vals[0].text.strip()) # Current Rank
# print(div_vals[1].text.strip()) # Peak Rank
# print(div_vals)
# print(span_stat_vals)
# print(span_vals)