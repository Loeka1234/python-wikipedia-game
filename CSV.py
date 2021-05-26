import csv


class CSV:
    def __init__(self, data: list):
        self.data = data

    def export(self):
        with open("wikipedia.csv", 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            for a in self.data:
                wr.writerow([a.text])