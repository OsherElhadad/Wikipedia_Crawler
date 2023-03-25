# Osher Elhadad 318969748 Gili Gutfeld 209284512

import requests
import lxml.html
import time


class PriorityQueue:

    def __init__(self, descendantsGradeFunc=lambda y: y):
        self.heap = []
        self.descendantsGradeFunc = descendantsGradeFunc

    def push(self, item):
        if item not in self.heap:
            self.heap.append(item)

    def pop(self, urlDescendants):
        if self.heap:
            min_item = self.heap[0]
            min_grade = descendantsGradeFunc(min_item, urlDescendants)
            for i in range(1, len(self.heap)):
                new_grade = descendantsGradeFunc(self.heap[i], urlDescendants)

                # The tie-breaker is the order of the urls in our heap
                if new_grade < min_grade:
                    min_item = self.heap[i]
                    min_grade = new_grade
            self.heap.remove(min_item)
            return min_item
        else:
            raise Exception('Cannot pop from empty PriorityQueue')

    def __len__(self):
        return len(self.heap)

    def __contains__(self, key):
        if len([item for item in self.heap if item == key]) > 0:
            return True
        return False

    def __getitem__(self, key):
        item = [item for item in self.heap if item == key]
        if len(item) == 0:
            raise KeyError(str(key) + " is not in the priority queue")
        return item[0]


class UrlDescendants:

    def __init__(self):
        self.dictUrlPerDescendants = dict()

    def add(self, url, descendant):
        if url in self.dictUrlPerDescendants.keys():
            if descendant not in self.dictUrlPerDescendants[url]:
                self.dictUrlPerDescendants[url].add(descendant)
        else:
            self.dictUrlPerDescendants[url] = set()
            self.dictUrlPerDescendants[url].add(descendant)
        if descendant in self.dictUrlPerDescendants.keys():
            for desOfDes in self.dictUrlPerDescendants[descendant]:
                self.add(url, desOfDes)

    def remove(self, url, descendant):
        if url in self.dictUrlPerDescendants.keys():
            if descendant in self.dictUrlPerDescendants[url]:
                self.dictUrlPerDescendants[url].remove(descendant)

    def urlGrade(self, url):
        if url not in self.dictUrlPerDescendants.keys():
            return 0
        return len(self.dictUrlPerDescendants.keys())

    def __len__(self):
        return len(self.dictUrlPerDescendants)


def isEmpty(s):
    return s is None or s == ""


def descendantsGradeFunc(url, urlDescendants):
    return urlDescendants.urlGrade(url)


def changeToVisitedOutput(outputs, url):
    if not outputs:
        return outputs
    for output in outputs:
        if output[1] == url:
            output[2] = 1
    return outputs


def discardUrl(outputs, url):
    if not outputs:
        return outputs
    new_outputs = []
    for output in outputs:
        if output[1] != url:
            new_outputs.append(output)
    return new_outputs


def britishCrawler(url, verifyXpath, descendantXpaths, ancestorXpaths, royaltyXpaths):
    urlDescendants = UrlDescendants()
    urls = PriorityQueue(descendantsGradeFunc)
    urls.push(url)
    closedList = set()
    outputs = []
    visitedAndVerified = set()
    visitedAndNotVerified = set()
    for _ in range(30):
        if len(urls) == 0:
            break
        url = urls.pop(urlDescendants)
        while not url.__contains__('en.wikipedia.org'):
            url = urls.pop(urlDescendants)
        while url in closedList:
            url = urls.pop(urlDescendants)
        closedList.add(url)
        res = requests.get(url)
        doc = lxml.html.fromstring(res.content)
        if not isEmpty(verifyXpath):
            answer = doc.xpath(verifyXpath)
            if len(answer) == 0:
                visitedAndNotVerified.add(url)
                time.sleep(3)
                continue
        visitedAndVerified.add(url)
        links = set()
        if descendantXpaths:
            for xpath in descendantXpaths:
                for descendant in doc.xpath(xpath):
                    descendantLink = 'https://en.wikipedia.org' + descendant
                    urls.push(descendantLink)
                    urlDescendants.add(url, descendantLink)
                    if descendantLink not in links:
                        outputs.append([url, descendantLink, 0])
                    links.add(descendantLink)
        if ancestorXpaths:
            for xpath in ancestorXpaths:
                for ancestor in doc.xpath(xpath):
                    ancestorLink = 'https://en.wikipedia.org' + ancestor
                    urls.push(ancestorLink)
                    urlDescendants.add(ancestorLink, url)
                    if ancestorLink not in links:
                        outputs.append([url, ancestorLink, 0])
                    links.add(ancestorLink)
        if royaltyXpaths:
            for xpath in royaltyXpaths:
                for royalty in doc.xpath(xpath):
                    royaltyLink = 'https://en.wikipedia.org' + royalty
                    urls.push(royaltyLink)
                    if royaltyLink not in links:
                        outputs.append([url, royaltyLink, 0])
                    links.add(royaltyLink)
        time.sleep(3)
    for notVerified in visitedAndNotVerified:
        outputs = discardUrl(outputs, notVerified)
    for verified in visitedAndVerified:
        outputs = changeToVisitedOutput(outputs, verified)
    return list(outputs)


if __name__ == '__main__':
    pass
    from crawlerQuality import crawlerQuality
    out = britishCrawler("https://en.wikipedia.org/wiki/Charles_III",
                   "//div[contains(@id, 'British_princes') or contains(@id, 'British_princesses') or contains(@id, 'British_royal_consorts') or contains(@id, 'British_princesses_by_marriage')]|//p[position() < 8]//a[contains(@title, 'Succession to the British throne') or contains(@title, 'British royal family') or contains(@title, 'Line of succession to the British throne') or contains(@title, 'Queen of the United Kingdom') or contains(@title, 'King of the United Kingdom') or contains(@title, 'British throne')]|//p[position() < 8 and (contains(., 'member of the royal family') or contains(., 'member of the British royal') or contains(., 'King of England'))]",
                         ["//table//th[contains(text(), 'Issue')]/following-sibling::td//a[not(contains(@href,'http'))]/@href"],
                         ["//table//th[contains(text(), 'Mother')]/following-sibling::td//a[not(contains(@href,'http'))]/@href",
                          "//table//th[contains(text(), 'Father')]/following-sibling::td//a[not(contains(@href,'http'))]/@href"],
                         ["//table/tbody/tr/th/a[@title='British royal family']/../../../tr/td/ul//li/a[not(contains(@href,'http'))]/@href",
                          "//table//th[contains(text(), 'Spouse')]/following-sibling::td//a[not(contains(@href,'http'))]/@href",
                          "//table//th[contains(text(), 'Predecessor')]/following-sibling::td//a[not(contains(@href,'http'))]/@href",
                          "//div[contains(@aria-labelledby, 'British_princes')]//tr/td//ul//li//a/@href|//div[contains(@aria-labelledby, 'British_princesses')]//tr/td//ul//li//a/@href|//div[contains(@aria-labelledby, 'British_royal_consorts')]//tr/td//ul//li//a/@href|//div[contains(@aria-labelledby, 'British_princesses_by_marriage')]//tr/td//ul//li//a/@href"])
    print(out)
    print(crawlerQuality(out))

