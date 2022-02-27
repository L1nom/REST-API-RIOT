from bs4 import BeautifulSoup
import requests

# https://tracker.gg/valorant/profile/riot/Pran%23NA1/overview


def getUserURL(name, tag):
    url = "https://tracker.gg/valorant/profile/riot/{}%23{}/overview".format(name, tag)

    stats = {}

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    div_vals = doc.find_all("div", {"class": "value"})
    div_labels = doc.find_all("div", {"class": "label"})

    current_rank = div_vals[0].text.replace("\n ", "").replace(" ", "").rstrip().strip()
    peak_rank = div_vals[1].text.replace("\n ", "").replace(" ", "").rstrip().strip()

    if div_labels[-1].text.replace("\n ", "").replace(" ", "").rstrip().strip() != "Rating":
        current_rank = div_labels[-1].text.replace("\n ", "").replace(" ", "").rstrip().strip() + current_rank

    stats["current_rank"] = current_rank
    stats["peak_rank"] = peak_rank
    print(stats)

    return url


# url = getUserURL("saint", "0816")
url = "https://tracker.gg/valorant/profile/riot/al1eNNNNNNNNNNNN%23SWAGR/overview"
# url = getUserURL("Pran", "NA1")
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
# print(doc.prettify())

div_vals = doc.find_all("div", {"class": "value"})
div_labels = doc.find_all("div", {"class": "label"})
span_stat_vals = doc.find_all("span")
span_vals = doc.find_all("span", {"class": "value"})

# print(span_stat_vals)

for item in span_stat_vals:
    print(item.text.replace("\n ", "").replace(" ", "").rstrip().strip())



# print(span_vals)