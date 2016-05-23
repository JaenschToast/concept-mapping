import nltk
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import networkx as nx
import sys

def homepage():
	return dict(message=T(''))

def form_text():
    db.define_table('concept_info',
    Field('text_in', 'text'),
    Field('how_many_concepts', requires=IS_NOT_EMPTY()),
    Field('verb_length', requires=IS_NOT_EMPTY()),
    Field('save_format', requires=IS_IN_SET(['PDF', 'TXT', 'NONE'])))
    SQLFORM(db.concept_info)
    form_text = SQLFORM(db.concept_info)
    texting = request.vars.text_in

    G = nx.Graph()  # Creates the graph

    tags = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT",
            "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT",
            "WP", "WP$", "WRB"]

    stop_words = ['!', '$', '%', '&', ',', '-', '.', '0', '1', '10', '100', '11', '12', '13', '14', '15', '16', '17',
                  '18', '19', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2', '20',
                  '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                  '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '21', '22', '23', '24', '25',
                  '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '4', '40',
                  '41', '42', '43', '44', '45', '46', '47', '48', '49', '5', '50', '51', '52', '53', '54', '55', '56',
                  '57', '58', '59', '6', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '7', '70', '71',
                  '72', '73', '74', '75', '76', '77', '78', '79', '8', '80', '81', '82', '83', '84', '85', '86', '87',
                  '88', '89', '9', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', ':', ';', '<', '>', '@',
                  '\(', '\)', '\*', '\+', '\?', '\[', '\]', '\^', '\{', '\}', 'a', 'about', 'above', 'across', 'after',
                  'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although',
                  'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow',
                  'anyone', 'anything', 'anyway', 'anywhere', 'around', 'as', 'at', 'b', 'back', 'before', 'beforehand',
                  'between', 'both', 'bottom', 'but', 'c', 'call', 'co', 'con', 'd', 'de', 'done', 'down', 'due',
                  'during', 'e', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'enough', 'etc',
                  'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'f', 'few', 'fifteen',
                  'fify', 'fill', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'four', 'front',
                  'full', 'further', 'g', 'go', 'h', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein',
                  'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if',
                  'inc', 'indeed', 'into', 'it', 'its', 'itself', 'j', 'k', 'keep', 'l', 'last', 'latter', 'latterly',
                  'least', 'less', 'ltd', 'm', 'many', 'me', 'meanwhile', 'mill', 'mine', 'more', 'moreover', 'most',
                  'mostly', 'much', 'my', 'myself', 'n', 'name', 'neither', 'nevertheless', 'next', 'nine', 'no',
                  'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'o', 'of', 'off', 'on', 'once',
                  'one', 'onto', 'or', 'other', 'others', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'p', 'part',
                  'per', 'perhaps', 'please', 'put', 'q', 'r', 're', 's', 'same', 'see', 'serious', 'several', 'she',
                  'since', 'six', 'sixty', 'some', 'somehow', 'someone', 'something', 'sometime', 'somewhere', 'still',
                  'such', 'system', 't', 'ten', 'than', 'that', 'the', 'thee', 'their', 'them', 'themselves', 'then',
                  'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they',
                  'thing', 'third', 'this', 'those', 'thou', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
                  'thy', 'to', 'together', 'too', 'twelve', 'twenty', 'two', 'u', 'un', 'under', 'up', 'upon', 'us',
                  'v', 'very', 'w', 'we', 'well', 'what', 'whatever', 'whence', 'whenever', 'where', 'whereafter',
                  'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither',
                  'who', 'whoever', 'whole', 'whom', 'whose', 'within', 'x', 'y', 'yet', 'you', 'your', 'yours',
                  'yourself', 'yourselves', 'z', '|']

    stop_word_length = len(stop_words)  # Calculates the amount of items in the list "stop_words"

    concepts = []  # This list will hold the initial concepts

    weighted_concepts = {}  # This list will hold the initial concepts with a frequency

    frequency_of_concepts = []  # This list will hold the frequency of all the concepts

    ordered_concepts = []  # This list will hold the weight of all of the concepts from most frequent to least frequent

    synonyms = []  # This list will hold all of the synonyms

    concept_connections = []  # This list will hold the concept connections

    concept_connection_counter = 0  # This will count the concept connections

    concept_duplication = set()  # Creates set to store final concept map information

    node_connections = []  # This list will hold the node connections and weight

    node_connection_counter = 0  # This will count the node connections

    node_duplication = set()  # Creates set to prevent creation of additional lists

    node_list = []  # This list will hold all of the nodes with an index

    tokens = nltk.word_tokenize(texting)  # Creates tokens

    number_of_tokens = len(tokens)  # Counts the number of tokens

    tokens_with_tags = nltk.pos_tag(tokens)  # Adds tags to tokens

    for x in range(0, number_of_tokens):
        for y in range(11, 15):
            if tokens_with_tags[x][1] == tags[y]:  # Checks for nouns
                concepts.append(tokens_with_tags[x][0])  # Adds nouns to a list of concepts

    number_of_concepts = len(concepts)  # Counts the number of concepts

    for i in range(0, number_of_concepts):
        concepts[i] = concepts[i].lower()  # Need to make all concepts lowercase before the program checks frequency

    number_of_tokens = len(tokens)

    for n in range(0, number_of_tokens):
        tokens[n] = tokens[n].lower()

    for a in range(0, number_of_concepts):
        frequency = concepts.count(concepts[a])  # Determines frequency of a particular concept
        frequency_of_concepts.append(frequency)
        weighted_concepts[concepts[a]] = frequency  # Adds the concept and frequency to a dictionary

    concepts = set(concepts)  # Turns concepts into a set to get rid of duplicates
    concepts = list(concepts)  # Turns concepts back into a list in order for it to be indexed

    number_of_concepts = len(concepts)  # Recounts the number of concepts

    for f in range(0, number_of_concepts):
        for g in range(f + 1, number_of_concepts):
            try:
                concept_a = wn.synsets(concepts[f])  # Turns the strings into a WordNet format (Synset)
                concept_b = wn.synsets(concepts[g])
                concept_a = concept_a[0]  # Sets the synsets equal to first noun definition
                concept_b = concept_b[0]
                concept_similarity = concept_a.path_similarity(
                    concept_b)  # Checks the similarity between concept a and concept b
                if .4 < concept_similarity < 1:  # Change the first value higher for lower sensitivity
                    weighted_concepts[concepts[f]] = weighted_concepts[
                                                         concepts[f]] + 1  # Adds one to the value of the concept
                    frequency_of_concepts.append(weighted_concepts[concepts[f]])
                    weighted_concepts[concepts[g]] = 0  # Makes the synonym have a weight of 0
                    synonyms.append(concepts[g])
                elif concept_similarity == 1:
                    if concepts[f] == concepts[g]:  # If the concepts are the same word the program will do nothing
                        pass
                    else:
                        weighted_concepts[concepts[f]] = weighted_concepts[concepts[f]] + 1  # Same as above
                        frequency_of_concepts.append(weighted_concepts[concepts[f]])
                        weighted_concepts[concepts[g]] = 0
                        synonyms.append(concepts[g])
            except IndexError:
                pass
            except UnicodeDecodeError:
                pass

    frequency_of_concepts = set(
        frequency_of_concepts)  # Turns frequency_of_concepts into a set to get rid of duplicates and to order it
    frequency_of_concepts = list(
        frequency_of_concepts)  # Turns frequency_of_concepts back into a list in order for it to be indexed

    number_of_concepts = len(weighted_concepts)  # Recounts the number of concepts

    for c in reversed(frequency_of_concepts):
        for d in range(0, number_of_concepts):
            if weighted_concepts[
                weighted_concepts.keys()[d]] == c:  # Checks to see if concept is repeated c amount of times
                ordered_concepts.append(
                    weighted_concepts.keys()[d])  # Adds concept to a list in order of most frequent to least frequent

    number_of_ordered_concepts = len(ordered_concepts)

    return dict(form_text=form_text, concepts=concepts)

def index():
    return dict(message=T('Hello!'))

def form():
    db.define_table('info',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('married', 'boolean'),
    Field('gender', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
    Field('profile', 'text'),
    Field('image', 'upload'))
    SQLFORM(db.info)
    form = SQLFORM(db.info)
    if form.process().accepted:
	    response.flash = 'form accepted'
    elif form.errors:
	    response.flash = 'form has errors'
    else:
	    response.flash = 'please fill out the form'
    test = form.vars.name
    return dict(form=form, test=test)
"""
    form = FORM(TABLE(
        TR('Your first name:', INPUT(_type='text', _name='firstname',
           requires=IS_NOT_EMPTY())),
        TR('Your last name:', INPUT(_type='text', _name='lastname',
           requires=IS_NOT_EMPTY())),
	TR('', INPUT(_type='submit', _value='SUBMIT')),
    ))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form is invalid'
    else:
        response.flash = 'please fill the form'
    return dict(form=form, vars=form.vars)"""


def user():
    return dict(form=auth())


@cache.action()

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    return service()


