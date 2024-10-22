import csv


class CSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        data = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                data.append(row)
        return data
