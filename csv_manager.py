import csv
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class CsvManager:
    def __init__(self, csvfile):
        self.allwords = os.path.join(basedir, csvfile)

    def add_word(self, text):
        with open(self.allwords, "a") as wordlist:
            writer = csv.writer(wordlist, delimiter=";")
            writer.writerow(text)

    def get_all_words(self):
        verben = []
        with open(self.allwords, newline='') as wordlist:
            lines = csv.reader(wordlist, delimiter=';')
            for line in lines:
                verben.append(line)

        return verben







