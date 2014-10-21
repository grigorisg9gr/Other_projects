# greg, 20 August 2014: Compares each pair news articles to extract several similarity measures.
# The articles should be already stemmed by clear_and_stem function. 
# The similarity measures computed, require the GENSIM library, which has GNU license. 
#
#
# Copyright (C) 2014 Grigorios G. Chrysos
# available under the terms of the Apache License, Version 2.0

import gensim
from gensim import corpora, models, similarities
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
from gensim.models import LsiModel, LogEntropyModel

import csv
import sys

background_corpus = TextCorpus('text_files/lemmas.dict')
background_corpus.dictionary.save("text_files/my_dict.dict")
dictionary = corpora.Dictionary.load("text_files/my_dict.dict")


def compute_jaccard_index(set_1, set_2):
    n = len(set(set_1).intersection(set(set_2)))
    return n / float(len(set_1) + len(set_2) - n)


def text_similarities(Inputcsv, Outcsv, delim):
    csv.register_dialect('perispwmeni', delimiter=delim)
    f = open(Inputcsv, 'r')
    fw = open(Outcsv, 'wb')
    fw2 = csv.writer(fw, delimiter=delim)

    tfidf = models.TfidfModel(background_corpus)
    lsi = LsiModel(tfidf[background_corpus], num_topics=100)
    lda = models.ldamodel.LdaModel(tfidf[background_corpus], id2word=dictionary, num_topics=90)
    hdp = models.hdpmodel.HdpModel(background_corpus, id2word=dictionary)
    try:
        reader = csv.reader(f, dialect='perispwmeni')

        fw2.writerow(['tfidf','cosine','jaccard','cosine_lsi','cosine_lda'])
        for row in reader:  # reads per line
            if len(row) <= 1:                                  # if len(row) == 1, then it is an empty line, skip it
                fw2.writerow([' '])
                continue
            line1 = row[0]
            line2 = row[1]
            l1_vector = dictionary.doc2bow(line1.split())
            l2_vector = dictionary.doc2bow(line2.split())
            if (len(l1_vector) < 1) | (len(l2_vector) < 1):
                continue
            #print l1_vector
            jaccard_sim = compute_jaccard_index(line1.split(), line2.split())
            cos_sim = gensim.matutils.cossim(l1_vector, l2_vector)
            hdp_sim = gensim.matutils.cossim(hdp[l1_vector], hdp[l2_vector])
            tfidf1 = tfidf[l1_vector]
            tfidf2 = tfidf[l2_vector]
            tfidf1.append((len(dictionary)-1, 0.00001))   # because otherwise, potential exception: IndexError: index %% out of bounds
            index = similarities.MatrixSimilarity([tfidf1], len(dictionary))
            sim = index[tfidf2]
            if len(sim)<1:                                  # in case there is no similarity it returns an empty list
                sim.append((0,0))
            cos_sim_lsi = gensim.matutils.cossim(lsi[tfidf1], lsi[tfidf2])    # similarity based on cosine (lsi vector)
            cos_sim_lda = gensim.matutils.cossim(lda[tfidf1], lda[tfidf2])    # similarity based on cosine (lda vector)

            '''print str(round(sim[0][1]*100, 2))+'% similar (tf-idf)'+', '+str(round(cos_sim*100, 2))+'% similar (cosine)'+', '\
                  +str(round(jaccard_sim*100, 2))+'% similar (jaccard)'+', '+str(round(cos_sim_lsi*100, 2))+\
                  '% similar (cosine_lsi)'+', '+str(round(cos_sim_lda*100, 2))+'% similar (cosine_lda)'+', '+str(round(hdp_sim*100, 2))+'% similar (cosine_hdp)'
                  '''
            fw2.writerow([round(sim[0][1]*100, 2),round(cos_sim*100, 2), round(jaccard_sim*100, 2),
                          round(cos_sim_lsi*100, 2), round(cos_sim_lda*100, 2), round(hdp_sim*100, 2)])
    finally:
        f.close()
        fw.close()


# call from terminal with full argument list:
if __name__ == '__main__':
    args = len(sys.argv)
    if args < 3:
        print "Not enough arguments for selecting an option in " + sys.argv[0]
        print "We need three arguments in this function. These are: the input file with the news (csv format), " \
              "the name of the output file and the default delimiter"
        raise Exception()
    text_similarities(sys.argv[1], sys.argv[2], sys.argv[3])



# Sources of information for text similarity:
# http://stackoverflow.com/questions/18183810/gensim-dictionary-implementation
# http://radimrehurek.com/gensim/corpora/dictionary.html
# http://www.williamjohnbert.com/2012/05/relatively-quick-and-easy-gensim-example-code/
# http://graus.nu/thesis/string-similarity-with-tfidf-and-python/

