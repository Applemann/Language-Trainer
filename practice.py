#!/usr/bin/python

import random
import copy
import os
import json
import urllib
import urllib2
from time import sleep

CHOICE_WORDS_NUM = 10
WORDS_NUM = 20


class Word:

    def __init__(self, eng, cze):
        self.eng = eng
        self.cze = cze
        self.en_to_cz_trans = False
        self.cz_to_en_trans = False
        self.en_to_cz_choice = False
        self.cz_to_en_choice = False
        self.accent = ""


def load_words():
    f = open("words.txt", 'r')
    lines = f.read().split('\n')
    f.close()
    return lines


def save_words():
    f = open("words.txt", 'w')
    for word in ALL_WORDS:
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
    f.close()


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def get_words_from_db():

    words = []
    for line in load_words():
        if line == '' or line[0] == '#':
            continue
        line = line.split(' | ')
        word = Word(line[0], line[1])
        word.en_to_cz_choice = str2bool(line[2])
        word.cz_to_en_choice = str2bool(line[3])
        word.en_to_cz_trans = str2bool(line[4])
        word.cz_to_en_trans = str2bool(line[5])
        word.accent = line[6]

        if word.en_to_cz_choice == True && word.cz_to_en_choice == True && word.en_to_cz_trans == True && word.cz_to_en_trans == True word.accent == True:
            continue
        words.append(word)

    return words


def print_trans_question(lang, word):
    if lang == "en-cz":
        print "Prelozte z anglictiny do cestiny slovo '"+word.eng+"':\n"
    elif lang == "cz-en":
        print "Prelozte z cestiny do anglictiny slovo '"+word.cze+"':\n"


def get_random_words(words, num):
    if len(words) < num:
        print "Malo moznych slov ve slovniku!!"
        exit()
    words = copy.copy(words)
    select_words = []
    for i in range(num):
        rand_word = random.choice(words)
        while rand_word in select_words:
            words.remove(rand_word)
            rand_word = random.choice(words)
        select_words.append(rand_word)

    return select_words


def print_choice_question(lang, word):
    word_list = get_random_words(ALL_WORDS, CHOICE_WORDS_NUM)
    if word not in word_list:
        word_list[random.choice(range(len(word_list)))] = word

    if lang == "en-cz":
        print "Vyberte spravne ceske slovo pro slovo '"+str(word.eng)+"' :\n"
        print ", ".join(map(lambda x: x.cze, word_list))

    if lang == "cz-en":
        print "Vyberte spravne anglicke slovo pro slovo '"+str(word.cze)+"':\n"
        print ", ".join(map(lambda x: x.eng, word_list))


def play_sound(word):
    os.system('bash -c \'cvlc "sounds/'+word+'.mp3" vlc://quit &> /dev/null\'')
    #sleep(1)
    


def download_sound(word):
    os.system('./download-sound.sh "' + word+'"')

ALL_WORDS = get_words_from_db()


#for word in ALL_WORDS:
#    print word.eng
#    download_sound(word.eng)
#play_sound(word)


all_words = get_random_words(ALL_WORDS, WORDS_NUM)

def main():
    while len(all_words) > 0:
        save_words()
        print "Zbyva celkem: " + str(len(all_words)) + " slov.\n"

        random_word = random.choice(all_words)

        if random_word.en_to_cz_choice == False:
            print_choice_question("en-cz", random_word)
            play_sound(random_word.eng)
            trans_word = raw_input()

            while trans_word == "p":
                play_sound(random_word.eng)
                trans_word = raw_input()


            print(chr(27) + "[2J")
            print str(random_word.eng) + " -> " + str(trans_word)
            if trans_word == random_word.cze:
                random_word.en_to_cz_choice = True
                print "Spravne"
                all_words.remove(random_word)
            else:
                print "Spatne. Spravne je: " + random_word.cze
                right = raw_input("Nebo si myslite neco jineho?? (N/y) ")
                if right == 'y': 
                    random_word.en_to_cz_choice = True
                    print "Spravne"
                    all_words.remove(random_word)
                    print "\n"
                    continue
                print "Spatne. Spravne je: " + random_word.cze
            print "\n"
            continue

        elif random_word.cz_to_en_choice == False:
            print_choice_question("cz-en", random_word)
            trans_word = raw_input()

            while trans_word == "p":
                play_sound(random_word.eng)
                trans_word = raw_input()

            print(chr(27) + "[2J")
            print str(random_word.cze) + " -> " + str(trans_word)
            if trans_word == random_word.eng:
                random_word.cz_to_en_choice = True
                print "Spravne"
                play_sound(random_word.eng)
                all_words.remove(random_word)
            else:
                print "Spatne. Spravne je: " + random_word.eng
                play_sound(random_word.eng)
                right = raw_input("Nebo si myslite neco jineho?? (N/y) ")
                if right == 'y': 
                    random_word.cz_to_en_choice = True
                    print "Spravne"
                    all_words.remove(random_word)
                    print "\n"
                    continue
                print "Spatne. Spravne je: " + random_word.eng
            print "\n"
            continue

        elif random_word.en_to_cz_trans == False:
            print_trans_question("en-cz", random_word)
            play_sound(random_word.eng)
            trans_word = raw_input()

            while trans_word == "p":
                play_sound(random_word.eng)
                trans_word = raw_input()

            print(chr(27) + "[2J")
            print str(random_word.eng) + " -> " + str(trans_word)
            if trans_word == random_word.cze:
                random_word.en_to_cz_trans = True
                print "Spravne"
                all_words.remove(random_word)
            else:
                print "Spatne. Spravne je: " + random_word.cze
                all_words.remove(random_word)
                right = raw_input("Nebo si myslite neco jineho?? (N/y) ")
                if right == 'y': 
                    random_word.en_to_cz_trans = True
                    print "Spravne"
                    print "\n"
                    continue
                print "Spatne. Spravne je: " + random_word.cze
                #random_word.en_to_cz_choice = False
            print "\n"
            continue

        elif random_word.cz_to_en_trans == False:
            print_trans_question("cz-en", random_word)
            trans_word = raw_input()

            #while trans_word == "p":
            #    play_sound(random_word.eng)
            #    trans_word = raw_input()

            print(chr(27) + "[2J")
            print str(random_word.cze) + " -> " + str(trans_word)
            if trans_word == random_word.eng:
                random_word.cz_to_en_trans = True
                print "Spravne"
                play_sound(random_word.eng)
                all_words.remove(random_word)
            else:
                print "Spatne. Spravne je: " + random_word.eng
                play_sound(random_word.eng)
                right = raw_input("Nebo si myslite neco jineho?? (N/y) ")
                if right == 'y': 
                    random_word.cz_to_en_trans = True
                    print "Spravne"
                    all_words.remove(random_word)
                    print "\n"
                    continue
                print "Spatne. Spravne je: " + random_word.eng
                #random_word.cz_to_en_choice = False
            print "\n"
            continue
        elif random_word.according != True:
            print "Napiste co slysite:"
            trans_word = raw_input()

            while trans_word == "p":
                play_sound(random_word.eng)
                trans_word = raw_input()

            print(chr(27) + "[2J")
            #print str(random_word.cze) + " -> " + str(trans_word)
            if trans_word == random_word.eng:
                print "Spravne"
                print "A ted napiste co to znamena v cestine:"
                trans_word = raw_input()
                if trans_word == random_word.cze:
                    print "Opet spravne."
                    print "Vypada to, ze toto slovicko uz umis ;-)"
                    random_word.according = True
                    play_sound(random_word.eng)
                    all_words.remove(random_word)
                else:
                    print "Spatne. Spravne je: " + random_word.cze
                    play_sound(random_word.eng)
                    random_word.en_to_cz_choice = False
                    continue

            else:
                print "Spatne. Spravne je: " + random_word.eng
                play_sound(random_word.eng)

            print "\n"
            continue
        else:
            all_words.remove(random_word)



if __name__ == "__main__":
    main()
    save_words()
    print "Gratuluji. Uspesne jste se naucili prelozit celkem: ", WORDS_NUM, "slov. :-)"
