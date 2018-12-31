#!/usr/bin/python

import random


def get_words_from_db():
    f = open("slovicka.txt", 'r')
    lines = f.read().split('\n')
    f.close()


    en_words = []
    cz_words = []
    for line in lines:
        if line == '' or line[0] == '#':
            continue
        en_word, cz_word = line.split(' - ')
        en_words.append(en_word)
        cz_words.append(cz_word)

    return zip(en_words, cz_words)


all_words = get_words_from_db()
#print all_words


while len(all_words) > 0:
    print "Zbyva celkem: " + str(len(all_words)) + " slov.\n"

    random_word = random.choice(all_words)
    choice_index = [0, 1]
    rand_index = random.choice([0,1])
    if rand_index == 0:
        print "Prelozte z anglictiny do cestiny:\n"
    else:
        print "Prelozte z cestiny do anglictiny:\n"

    choice_index.remove(rand_index)

    #print random_word[choice_index[0]]
    trans_word = raw_input(random_word[rand_index] + ": ")
    print trans_word

    if (trans_word == "q" or trans_word == "x"):
        print "Predcasne ukonceni."
        break
    if (trans_word == "p"):
        print "Prehravam vyslovnost"
        trans_word = raw_input(random_word[rand_index] + ": ")

    if (trans_word == random_word[choice_index[0]]):
        all_words.remove(random_word)
        print "Spravne"

    else:
        print "Spatne. Spravne je: " + random_word[choice_index[0]]

    print "\n"







