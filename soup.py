import sys
from typing import Optional

import requests
from bs4 import BeautifulSoup, element


class Soup:
    source: str
    destination: str
    amount_crawled: int = 0

    def __init__(self, source, destination):
        self.source = requests.get(source).url
        self.destination = requests.get(destination).url

    def calculate_clicks(self, amount: int) -> Optional[list[element.Tag]]:
        initial_anchors = list(self.get_all_page_anchors(self.get_soup(self.source)))

        # First layer
        result = self.find_destination_in_anchors(initial_anchors)
        if result is not None:
            return [result]

        # Initializing variables
        combinations = []
        anchors_done = []
        for a in initial_anchors:
            combinations.append([a])
            anchors_done.append(a)

        founded_route = None
        try:
            # Looping over amount layers
            for i in range(1, amount):
                new_combinations = []
                new_anchors_done = []
                for combination in combinations:
                    a = combination[len(combination) - 1]  # getting the last anchor
                    anchors_to = list(self.get_all_page_anchors(self.get_soup("https://nl.wikipedia.com" + a['href'])))
                    # Checking if the destination is found
                    result = self.find_destination_in_anchors(anchors_to)
                    if result is not None:
                        founded_route = [*combination, result]
                        raise StopIteration

                    # Adding all combinations
                    for a_to in anchors_to:
                        if a_to not in anchors_done:
                            new_combination = []
                            for item in combination:
                                new_combination.append(item)
                            new_combination.append(a_to)
                            new_combinations.append(new_combination)
                            new_anchors_done.append(a_to)
                combinations = new_combinations
                anchors_done = new_anchors_done
        except StopIteration:
            pass

        sys.stdout.flush()

        return founded_route

    def get_all_page_anchors(self, soup):
        for a in soup.find_all('a', href=True):
            if self.is_valid_anchor(a):
                yield a
        self.increment_and_log_crawled()

    def find_destination_in_anchors(self, anchors) -> Optional[element.Tag]:
        for a in anchors:
            if a['href'] in self.destination:
                return a
        return None

    def increment_and_log_crawled(self):
        sys.stdout.write("\rAmount pages crawled: %i" % self.amount_crawled)
        sys.stdout.flush()
        self.amount_crawled += 1

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, "html.parser")

    @staticmethod
    def is_valid_anchor(a) -> bool:
        excluded_anchors = ["Categorieën", "Overleg", "Bijdragen", "Artikel", "Overleg", "Lezen", "Hoofdpagina",
                            "Vind een artikel", "Vandaag", "Vandaag", "Etalage", "Categorieën", "Recente wijzigingen",
                            "Nieuwe artikelen", "Willekeurige pagina", "Gebruikersportaal", "Snelcursus",
                            "Hulp en contact", "Doneren", "Links naar deze pagina", "Gerelateerde wijzigingen",
                            "Gerelateerde wijzigingen", "Speciale pagina's", "Over Wikipedia", "Disclaimers"]
        return a['href'].startswith(
            "/wiki/") and a.text != "" and a.text is not None and '[' not in a.text and ']' not in a.text and 'Wikipedia:' not in a.text and a.text not in excluded_anchors
