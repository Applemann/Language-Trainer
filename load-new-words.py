#!/usr/bin/python


class Word:

    def __init__(self, eng, cze):
        self.eng = eng
        self.cze = cze
        self.en_to_cz_trans = False
        self.cz_to_en_trans = False
        self.en_to_cz_choice = False
        self.cz_to_en_choice = False
        self.accent = "/home/martin/accent/accent-example.mp3"


def load_words():
    f = open("new-words.txt", 'r')
    lines = f.read().split('\n')
    f.close()
    return lines


def download_sound(word):
    os.system('./download-sound.sh "' + word + '"')


def save_words(words):
    f = open("words.txt", 'a')
    for word in words:
        w = [
                word.eng, 
                word.cze, 
                word.en_to_cz_choice, 
                word.cz_to_en_choice, 
                word.en_to_cz_trans, 
                word.cz_to_en_trans,
                word.accent
            ]
        f.write(" | ".join(map(lambda x: str(x), w)) + "\n")
        download_sound(word.eng)
    f.close()


def get_words_from_db():

    words = []
    for line in load_words():
        if line == '' or line[0] == '#':
            continue
        en_word, cz_word = line.split(' - ')
        words.append(Word(en_word, cz_word))

    return words



all_words = get_words_from_db()
save_words(all_words)
