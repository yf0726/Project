import pandas as pd
import os
import re
from os import walk
import numpy as np
import nltk
from nltk.corpus import brown

# This is a fast and simple noun phrase extractor (based on NLTK)


# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='lore')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;|\')$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.(optional|fresh|unsalted|ground)$', 'ADJ'),
     (r'.*', 'NN')
     ])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG;
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"  #olive oil
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"  
cfg["JJ+NN"] = "NNI" #black paper
cfg["NUMB+IN"] = "NUMA" #a cup of 
cfg["CD+CNT"] = "NUMB" #a cup
cfg["TO+NN"] = "AIM" #a cup
# cfg["IN+NNI"] = "INN"
cfg["(+NN"] = "("
cfg["(+ADJ"] = "("
cfg["(+C"] = "("
cfg["(+NNI"] = "("
cfg["(+NNP"] = "("
cfg["(+JJ"] = "("
# cfg["NN+CNT"] = "OUT"
cfg["IN+NN"] = "PP"
cfg["NN+CNT"] = "NUMB"
cfg["CNT+IN"] = "NUMC"
#############################################################################


class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(unigram_tagger.tag(tokens))#bigram_tagger.tag(tokens))
        merge = True
        while merge:
            merge = False
            for x in range(-1, len(tags) - 1):
                t = tags[x+1]
                if re.search(r'(?i)^(tsp|\%|oz|wedges|tbsp|squares|tbs|square|loaf|cup|lbs|jar|jars|half|halves|degrees|flakes|degree|teaspoon|dash|dashes|strips|packet|tablespoon|cups|notes|teaspoons|tablespoons|g|kg|slices|slice|lb|ounce|inch|inches|package|packages|quarts|quart|pound|pounds|medium|ounces|pieces)$', t[0]):
                    t = tags[x+1]
                    tags.pop(x+1)
                    tags.insert(x+1, (t[0], 'CNT'))
                if re.search(r'(optional|new|hot|half|C|purpose|long|all\-purpose|dice|coarse|fine|crunchy|semisweet|pure|warm|virgin|skinless|dry|cold|sharp|baby|fresh|unsalted|ground|dried|lengthwise|large|small|thin|median|pinch|total)$', t[0]):
                    t = tags[x+1]
                    tags.pop(x+1)
                    tags.insert(x+1, (t[0], 'ADJ'))
                if re.search(r'(cloves|clove|cubes|cube)$', t[0]):
                    t = tags[x+1]
                    tags.pop(x+1)
                    tags.insert(x+1, (t[0], 'CNTB'))
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break
        matches = []
        flag_NN=1
        for t in tags:
            if  t[1] == "NNI" or t[1] == "NN" or t[1] == "NNP":
                flag_NN = 0
                matches.append(t[0])
        if flag_NN:
            for t in tags:
                if t[1] == "CNTB":
                    matches.append(t[0])
        return matches
