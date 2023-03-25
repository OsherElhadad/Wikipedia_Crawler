# Osher Elhadad 318969748 Gili Gutfeld 209284512

import requests
import lxml.html


def crawlerQuality(listOfPairs):
    quality = dict()
    if not listOfPairs:
        return quality
    if len(listOfPairs) == 0:
        return quality
    p_total = set()
    p_crawled = set()
    for pair in listOfPairs:
        if len(pair) != 3:
            return quality
        p_total.add(pair[0])
        p_total.add(pair[1])
        if pair[2] == 1:
            p_crawled.add(pair[1])
    quality['precision'] = len(p_crawled) / len(p_total)
    return quality


# Better crawler quality function- explained in the report
# def crawlerQuality(listOfPairs):
#     quality = dict()
#     if not listOfPairs or len(listOfPairs) == 0:
#         return quality
#     sources = set()
#     p_reached = set()
#     p_reached_one = set()
#     for pair in listOfPairs:
#         if len(pair) != 3:
#             return quality
#         sources.add(pair[0])
#         if pair[2] == 0:
#             p_reached.add(pair[1])
#         if pair[2] == 1:
#             p_reached_one.add(pair[1])
#     sources = sources.difference(p_reached_one)
#
#     # Checked already if there is item in [0][0]
#     if len(sources) == 0:
#         sources.add(listOfPairs[0][0])
#     res = requests.get("https://en.wikipedia.org/wiki/British_royal_family")
#     doc = lxml.html.fromstring(res.content)
#     answers = doc.xpath("//div[contains(@aria-labelledby,"
#                         " 'British_princes')]//tr/td//ul//li//a/@href|//div[contains(@aria-labelledby,"
#                         " 'British_princesses')]//tr/td//ul//li//a/@href|//div[contains(@aria-labelledby,"
#                         " 'British_royal_consorts')]//tr/td//ul//li//a/@href|//div[contains(@aria-labelledby,"
#                         " 'British_princesses_by_marriage')]//tr/td//ul//li//a/@href")
#     p = set()
#     for ans in answers:
#         p.add('https://en.wikipedia.org' + ans)
#     p1 = p.difference(sources)
#     quality['precision'] = len(p1.intersection(p_reached)) / len(p_reached)
#     quality['recall'] = len(p1.intersection(p_reached)) / len(p1)
#     quality['F1'] = (2 * quality['precision'] * quality['recall']) / (quality['precision'] + quality['recall'])
#     return quality
