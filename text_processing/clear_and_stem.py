# -*- coding: utf-8 -*-

# greg, 4 August 2014: Stems a text. Original text in the form of a news article.
# The format supported by the function stem_file, parses a *.csv file with two articles per line,
# stems both and then saves them in an output file.
# It calls the function stem from stemming.py. It removes accents, capitalises letters, removes the numbers
# and the english characters.
#
#
# Copyright (C) 2014 Grigorios G. Chrysos
# available under the terms of the Apache License, Version 2.0

import csv
import unicodedata  # for removing accents
import re
import sys
import stemming as stem

# function that removes the accents from strings (including greek characters) from http://stackoverflow.com/a/518232/1716869
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


# check whether a string contains a number
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))


def stem_file(Inputcsv, Outcsv, delim):
    """
    :param Inputcsv: The input file with the original news articles
    :param Outcsv:   The name of the output file that we wish the stemmed articles to be saved to
    :param delim:    The delimeter used in the reading file
    :return:         Does not return any value
    """
    csv.register_dialect('perispwmeni', delimiter=delim)
    fw = open(Outcsv, 'wb')
    fw2 = csv.writer(fw, delimiter=delim)
    f = open(Inputcsv, 'r')
    try:
        reader = csv.reader(f, dialect='perispwmeni')
        cnt_row = 0
        for row in reader:  # reads per line
            #print row
            cmp_two = []                                    # two strings that will be compared
            cnt_row = cnt_row +1                            # row counter
            if len(row)>1:                                  # if len(row) == 1, then it is an empty line, skip it
                for elem in [5, 6]:                         # The text (news articles) is in columns 6,7 in the current format
                    line_out = ''                           # line after the processing
                    line1 = row[elem]
                    words = line1.split()
                    for word in words:                      # loop over each element of list "words"
                        ww = stem.get_decoded_input(word)   # it was 'str' before and becomes 'unicode' from type (ww)
                        last_char_spec =''.encode('utf-8')
                        last_char = ww[-1]                          # if the last character is a special
                        if last_char == ',' or last_char == '.' or last_char == '!' or last_char == ';':    # char (',','.','!',';'), we trim it
                            ww = ww[:-1]
                            last_char_spec = last_char.encode('utf-8')
                        ww = strip_accents(ww)
                        if len(ww)<1:
                            continue
                        english_char = re.search('[a-zA-Z]', ww)    # Check whether the word contains English characters
                        cont_dig = not contains_digits(ww)
                        if (not ww[0].isupper()) and (english_char is None) and cont_dig:
                        # if the first letter is capital, it contains English characters or it is a number,
                        # then we don't want to stem it
                            ww = ww.upper()
                            stemmed = stem.stem(ww)
                            stemmed = stemmed.lower()
                            stemmed = stemmed.encode('utf-8')
                            line_out = line_out + ' ' + stemmed + last_char_spec
                        elif cont_dig:
                            #ww = ww.upper()
                            line_out = line_out + ' ' + ww.encode('utf-8') + last_char_spec
                        else:
                            line_out = line_out + ' NUM' + last_char_spec
                    # programmer comment: if cm_two = [cmp_two,line_out], the encoding does not appear correctly
                    if elem == 5:
                        cmp_two = line_out
                    else:
                        cmp_two = [cmp_two, line_out]
                fw2.writerow(cmp_two)
            else:
                fw2.writerow([' '])
    finally:
        f.close()



# call from terminal with full argument list:
if __name__ == '__main__':
    args = len(sys.argv)
    if args < 3:
        print "Not enough arguments for selecting an option in " + sys.argv[0]
        print "We need three arguments in this function. These are: the input file with the news (csv format), " \
              "the name of the output file and the default delimiter"
        raise Exception()
    stem_file(sys.argv[1], sys.argv[2], sys.argv[3])
