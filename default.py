import nltk
import os
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import networkx as nx
import sys

def homepage():
	return dict(message=T(''))

def form_text():
    db.define_table('concept_info',
    Field('text_in', 'text'),
    Field('how_many_concepts', requires=IS_IN_SET([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])),
    Field('connecting_length_checked', requires=IS_IN_SET([1,2,3,4,5,6,7,8,9,10])),
    Field('concepts_to_add', 'text'),
    Field('concepts_to_remove', 'text'),
    Field('save_format', requires=IS_IN_SET(['PDF', 'TXT', 'NONE'])),
    Field('name_to_save_as', requires=IS_NOT_EMPTY()),
    Field('enter_gold_standard', 'text'))
    form_text = SQLFORM(db.concept_info)
    save_name = request.vars.name_to_save_as
    save_type = request.vars.save_format
    texting = request.vars.text_in
    verb_num = request.vars.connecting_length_checked
    concept_add = request.vars.concepts_to_add
    concept_delete = request.vars.concepts_to_remove
    stored_concepts = request.vars.how_many_concepts
    g_standard = request.vars.enter_gold_standard

    if g_standard:
        pass
    else:
        g_standard = "-"

    if texting:
        pass
    else:
        texting = ""

    if verb_num:
        pass
    else:
        verb_num = 4

    if stored_concepts:
        pass
    else:
        stored_concepts = 15

    try:
        stored_concepts = int(stored_concepts)
    except TypeError:
        pass

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

    tokens = []

    error = ""

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

    try:
        tokens = nltk.word_tokenize(str(texting))  # Creates tokens
    except UnicodeDecodeError:
        error = "ERROR #357: PLEASE ENTER TEXT ONLY"

    try:
        number_of_tokens = len(tokens)  # Counts the number of tokens
    except UnboundLocalError:
        pass

    try:
        tokens_with_tags = nltk.pos_tag(tokens)  # Adds tags to tokens
    except UnicodeDecodeError:
        error = "ERROR #357: PLEASE ENTER TEXT ONLY"

    try:
        for x in range(0, number_of_tokens):
            for y in range(11, 15):
                if tokens_with_tags[x][1] == tags[y]:  # Checks for nouns
                    concepts.append(tokens_with_tags[x][0])  # Adds nouns to a list of concepts
    except UnboundLocalError:
        pass

    number_of_concepts = len(concepts)  # Counts the number of concepts

    for i in range(0, number_of_concepts):
        concepts[i] = concepts[i].lower()  # Need to make all concepts lowercase before the program checks frequency

    try:
        number_of_tokens = len(tokens)
    except UnboundLocalError:
        pass

    try:
        for n in range(0, number_of_tokens):
            tokens[n] = tokens[n].lower()
    except UnboundLocalError:
        pass

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

    try:
        for e in range(number_of_ordered_concepts - stored_concepts):
            ordered_concepts.pop()
    except TypeError:
        pass

    concept_add = nltk.word_tokenize(str(concept_add))

    concept_delete = nltk.word_tokenize(str(concept_delete))

    for x in concept_add:
        if ordered_concepts.count(x) == 0:
            concept_add = x.lower()
            ordered_concepts.append(concept_add)
        else:
            pass

    for x in concept_delete:
        concept_delete = x.lower()
        ordered_concepts.remove(concept_delete)

    concept_connection_counter = 0

    tags_check = [25, 26, 27, 28, 29, 30]

    sensitivity = 0

    try:
        sensitivity = int(verb_num)
    except TypeError:
        pass

    try:
        for h in range(0, 15):  # Repeats once for every concept
            token_location = 0
            for i in (tokens):  # Cycles through the document
                try:
                    if i == ordered_concepts[h]:
                        for j in range(0, sensitivity):  # Checks the next X words for connecting verb
                            for k in tags_check:
                                if (tokens_with_tags[token_location + j][1] == tags[k]) and (
                                    tokens_with_tags[token_location + j][0].lower() != ordered_concepts[h]):
                                    if tokens_with_tags[token_location + j][0].lower() in ordered_concepts:
                                        pass
                                    else:
                                        for l in range(0, sensitivity):  # Checks the next X words for connecting concept
                                            for m in ordered_concepts:
                                                if (tokens[token_location + j + l].lower() == m) and (
                                                    tokens[token_location + j + l].lower() != ordered_concepts[h]) and (
                                                    tokens[token_location + j + l].lower() != tokens[
                                                        token_location + j].lower()):
                                                    if ordered_concepts[h] + tokens[token_location + j] + tokens[
                                                                        token_location + j + l] in concept_duplication:  # Checks for duplicates
                                                        pass
                                                    else:
                                                        concept_connections.append(
                                                            [])  # Creates three lists inside one concept_connections index
                                                        for o in range(0, 4):  # REMOVE 4TH ADDITION IF NOT NEEDED
                                                            concept_connections[concept_connection_counter].append(
                                                                "")  # Adds concepts to "master list"
                                                        concept_connections[concept_connection_counter][0] = \
                                                        ordered_concepts[h]
                                                        concept_connections[concept_connection_counter][1] = tokens[
                                                            token_location + j]
                                                        concept_connections[concept_connection_counter][2] = tokens[
                                                            token_location + j + l]
                                                        concept_connections[concept_connection_counter][
                                                            3] = 1  # Counts the amount of times a group is repeated
                                                        # j = 100
                                                        # l = 100
                                                        # print(str(concept_connections[concept_connection_counter][0]) + " " + str(concept_connections[concept_connection_counter][1]) + " " + str(j) + " " + str(concept_connections[concept_connection_counter][2]) + " " + str(l))
                                                        concept_duplication.add(
                                                            ordered_concepts[h] + tokens[token_location + j] + tokens[
                                                                token_location + j + l])
                                                        concept_connection_counter = concept_connection_counter + 1

                except IndexError:
                    pass
                token_location = token_location + 1  # Tracks index of token

    except UnboundLocalError:
        pass

    nodelistA = []  # This list will hold the concepts
    nodelistB = []  # This list will hold the verbs

    for x in range(0, concept_connection_counter):
        if concept_connections[x][0] in G.nodes():  # Adds a new node
            pass
        else:
            G.add_node(concept_connections[x][0])
            nodelistA.append(concept_connections[x][0])  # Sets node to concept group

        if concept_connections[x][1] in G.nodes():  # Adds a new node
            pass
        else:
            G.add_node(concept_connections[x][1])
            nodelistB.append(concept_connections[x][1])  # Sets node to verb group

        if concept_connections[x][2] in G.nodes():  # Adds a new node
            pass
        else:
            G.add_node(concept_connections[x][2])
            nodelistA.append(concept_connections[x][2])  # Sets node to concept group

        a = G.nodes().index(concept_connections[x][0])  # Stores index of node
        b = G.nodes().index(concept_connections[x][1])

        if str(a) + str(b) in node_duplication:  # Checks if the node is already placed
            for o in range(0, node_connection_counter):
                if node_connections[o][0] == a and node_connections[o][1] == b:
                    node_connections[o][2] = node_connections[o][
                                                 2] + 1  # Adds one to the weight counter of node connections
                    o = node_connection_counter
        else:
            node_connections.append([])  # Adds the node connections to a list
            for c in range(0, 3):
                node_connections[node_connection_counter].append("")
            node_connections[node_connection_counter][0] = a
            node_connections[node_connection_counter][1] = b
            node_connections[node_connection_counter][2] = 1
            node_connection_counter = node_connection_counter + 1
            node_duplication.add(str(a) + str(b))

        a = G.nodes().index(concept_connections[x][1])  # Same as above
        b = G.nodes().index(concept_connections[x][2])

        if str(a) + str(b) in node_duplication:
            for o in range(0, node_connection_counter):
                if node_connections[o][0] == a and node_connections[o][1] == b:
                    node_connections[o][2] = node_connections[o][2] + 1
                    o = node_connection_counter
        else:
            node_connections.append([])
            for c in range(0, 3):
                node_connections[node_connection_counter].append("")
            node_connections[node_connection_counter][0] = a
            node_connections[node_connection_counter][1] = b
            node_connections[node_connection_counter][2] = 1
            node_connection_counter = node_connection_counter + 1
            node_duplication.add(str(a) + str(b))

        G.add_edge(concept_connections[x][0], concept_connections[x][1])
        G.add_edge(concept_connections[x][1], concept_connections[x][2])

    e = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.spring_layout(G, scale=50)

    plt.figure(num=None, figsize=(40, 22.5), dpi=120)

    try:
        nodes = nx.draw_networkx_nodes(G, pos, nodelist=nodelistA, node_size=200, node_color='cyan')

        nodes.set_edgecolor('white')

        nodes = nx.draw_networkx_nodes(G, pos, nodelist=nodelistB, node_size=200, node_color='white')

        nodes.set_edgecolor('white')

        nx.draw_networkx_edges(G, pos, edgelist=e, width=2, edge_color="gray", alpha=0.7)

        nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    except AttributeError:
        pass

    plt.axis('off')
    # plt.show()

    for x in G.nodes():
        node_list.append(x)
    try:
        save_format = str(save_format)

    except UnboundLocalError:
        pass

    save_name = str(save_name)

    if save_type == "PDF":
        new_name = save_name + ".pdf"
        plt.savefig('/home/dre/web2py/applications/concept_map/uploads/' + new_name)  # Creates pdf file
        pathfilename = os.path.join(request.folder,'uploads/',new_name)
        return response.stream(open(pathfilename,'rb'),chunk_size=10**6)

    if save_type == "TXT":
        new_name = save_name + ".txt"
        file = open('/home/dre/web2py/applications/concept_map/uploads/' + new_name, "w")  # Creates txt file
        for x in range(0, concept_connection_counter):  # Adds concepts to file
            file.write(concept_connections[x][0] + chr(9) + concept_connections[x][1] + chr(9) + concept_connections[x][
                2] + "\n")
        file.close()  # Saves and closes the file
        pathfilename = os.path.join(request.folder, 'uploads/', new_name)
        return response.stream(open(pathfilename, 'rb'), chunk_size=10 ** 6)

    gold_out_1 = ""

    gold_out_2 = ""

    gold_out_3 = ""

    gold_out_4 = ""

    if g_standard != "-":

        tokens = nltk.word_tokenize(g_standard)  # Creates tokens

        number_of_tokens = len(tokens)  # Counts the number of tokens

        gold_standard = []

        for x in range(0, number_of_tokens):
            if (x % 3 == 0 or x == 0) and (x < number_of_tokens - 2):
                gold_standard.append(tokens[x] + " " + tokens[x + 1] + " " + tokens[x + 2])
                gold_standard.append(tokens[x + 2] + " " + tokens[x + 1] + " " + tokens[x])

        concept_comparison = []

        for x in range(0, concept_connection_counter):
            if x < concept_connection_counter:
                concept_comparison.append(str(concept_connections[x][0]) + " " + str(concept_connections[x][1]) + " " + str(
                    concept_connections[x][2]))

        concept_comparison = set(concept_comparison)

        concept_comparison = list(concept_comparison)

        number_of_master_prop = number_of_tokens / 3

        similar_prop = 0

        good_prop = []

        for x in gold_standard:
            for y in concept_comparison:
                if x == y:
                    similar_prop = similar_prop + 1
                    good_prop.append(y)

        for x in good_prop:
            try:
                concept_comparison.remove(x)
            except ValueError:
                pass

        all_syn = set()

        for f in concept_comparison:
            for g in gold_standard:
                try:
                    compare_syn = nltk.word_tokenize(f)
                    concept_syn_1 = wn.synsets(compare_syn[0])
                    concept_syn_2 = wn.synsets(compare_syn[1])
                    concept_syn_3 = wn.synsets(compare_syn[2])
                    concept_syn_1 = concept_syn_1[0]
                    concept_syn_2 = concept_syn_2[0]
                    concept_syn_3 = concept_syn_3[0]
                    compare_syn_b = nltk.word_tokenize(g)
                    concept_syn_1_b = wn.synsets(compare_syn_b[0])
                    concept_syn_2_b = wn.synsets(compare_syn_b[1])
                    concept_syn_3_b = wn.synsets(compare_syn_b[2])
                    concept_syn_1_b = concept_syn_1_b[0]
                    concept_syn_2_b = concept_syn_2_b[0]
                    concept_syn_3_b = concept_syn_3_b[0]

                    sim_1 = concept_syn_1.path_similarity(concept_syn_1_b)

                    sim_2 = concept_syn_2.path_similarity(concept_syn_2_b)

                    sim_3 = concept_syn_3.path_similarity(concept_syn_3_b)

                    if (.4 < sim_1 < 1) and (.4 < sim_2 < 1) and (.4 < sim_3 < 1):
                        good_prop.append(f)
                        concept_comparison.remove(f)
                        similar_prop = similar_prop + 1
                        print(f)
                        print("HERE")

                except IndexError:
                    pass
                except UnicodeDecodeError:
                    pass

        similar_prop = float(similar_prop)

        number_of_master_prop = float(number_of_master_prop)

        similarity_percentage = 0

        similarity_percentage = float(similarity_percentage)

        similarity_percentage = ((similar_prop) / (number_of_master_prop)) * 100

        if similarity_percentage>100:
            similarity_percentage = 100
            similar_prop = number_of_master_prop

        num_useless = concept_connection_counter - similar_prop

        if gold_standard:
            gold_out_1 = "The student had " + str(int(similar_prop)) + " propositions in common with the gold standard of " + str(
                int(number_of_master_prop)) + " propositions."

            gold_out_2 = str(int(similar_prop)) + "/" + str(int(number_of_master_prop)) + " = " + str(similarity_percentage) + "%"

            gold_out_3 = "The unnecessary propositions were: "

            gold_out_4 = concept_comparison

        else:
            pass

    return dict(form_text=form_text, error=error, gold_out_1 = gold_out_1, gold_out_2 = gold_out_2, gold_out_3 = gold_out_3, gold_out_4 = gold_out_4)


def index():
    return dict(message=T('Hello!'))

def form():
    db.define_table('concept_info',
    Field('choose_a_document', 'upload'),
    Field('choose_a_gold_standard', 'upload'),
    Field('how_many_concepts', requires=IS_IN_SET([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])),
    Field('connecting_length_checked', requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
    Field('concepts_to_add', 'text'),
    Field('concepts_to_remove', 'text'),
    Field('save_format', requires=IS_IN_SET(['PDF','TXT','NONE'])),
    Field('name_to_save_as'))
    up_form = SQLFORM(db.concept_info).process()
    save_name = request.vars.name_to_save_as
    save_type = request.vars.save_format
    verb_num = request.vars.connecting_length_checked
    concept_add = request.vars.concepts_to_add
    concept_delete = request.vars.concepts_to_remove
    stored_concepts = request.vars.how_many_concepts

    #db.define_table('upload_doc',
    #Field('choose_a_document', 'upload'),
    #Field('choose_a_gold_standard', 'upload'))
    #up_form = SQLFORM(db.concept_info).process()
    text_doc = request.vars.choose_a_document
    gold_doc = request.vars.choose_a_gold_standard
    text_name = up_form.vars.choose_a_document
    gold_name = up_form.vars.choose_a_gold_standard

    try:
        imported_document = open('/home/dre/web2py/applications/concept_map/uploads/' + str(text_name), 'r')
        texting = imported_document.read()
        imported_document2 = open('/home/dre/web2py/applications/concept_map/uploads/' + str(gold_name), 'r')
        g_standard = imported_document2.read()
    except IOError:
        pass
    '''if gold_doc:
        imported_document2 = open('/home/dre/web2py/applications/concept_map/uploads/' + str(gold_name), 'r')
        g_standard = imported_document2.read()
    else:
        gold_doc = "-"

    if text_doc:
        imported_document = open('/home/dre/web2py/applications/concept_map/uploads/' + str(text_name), 'r')
        texting = imported_document.read()
    else:
        text_doc = ""
    '''

    if verb_num:
        pass
    else:
        verb_num = 4

    if stored_concepts:
        pass
    else:
        stored_concepts = 15

    try:
        stored_concepts = int(stored_concepts)
    except TypeError:
        pass

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

    tokens = []

    error = ""

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

    try:
        try:
            tokens = nltk.word_tokenize(str(texting))  # Creates tokens
        except UnicodeDecodeError:
            error = "ERROR #357: PLEASE ENTER TEXT ONLY"
    except UnboundLocalError:
        pass

    try:
        number_of_tokens = len(tokens)  # Counts the number of tokens
    except UnboundLocalError:
        pass

    try:
        tokens_with_tags = nltk.pos_tag(tokens)  # Adds tags to tokens
    except UnicodeDecodeError:
        error = "ERROR #357: PLEASE ENTER TEXT ONLY"

    try:
        for x in range(0, number_of_tokens):
            for y in range(11, 15):
                if tokens_with_tags[x][1] == tags[y]:  # Checks for nouns
                    concepts.append(tokens_with_tags[x][0])  # Adds nouns to a list of concepts
    except UnboundLocalError:
        pass

    number_of_concepts = len(concepts)  # Counts the number of concepts

    for i in range(0, number_of_concepts):
        concepts[i] = concepts[i].lower()  # Need to make all concepts lowercase before the program checks frequency

    try:
        number_of_tokens = len(tokens)
    except UnboundLocalError:
        pass

    try:
        for n in range(0, number_of_tokens):
            tokens[n] = tokens[n].lower()
    except UnboundLocalError:
        pass

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

    try:
        for e in range(number_of_ordered_concepts - stored_concepts):
            ordered_concepts.pop()
    except TypeError:
        pass

    concept_add = nltk.word_tokenize(str(concept_add))

    concept_delete = nltk.word_tokenize(str(concept_delete))

    for x in concept_add:
        if ordered_concepts.count(x) == 0:
            concept_add = x.lower()
            ordered_concepts.append(concept_add)
        else:
            pass

    for x in concept_delete:
        concept_delete = x.lower()
        ordered_concepts.remove(concept_delete)

    concept_connection_counter = 0

    tags_check = [25, 26, 27, 28, 29, 30]

    sensitivity = 0

    try:
        sensitivity = int(verb_num)
    except TypeError:
        pass

    try:
        for h in range(0, 15):  # Repeats once for every concept
            token_location = 0
            for i in (tokens):  # Cycles through the document
                try:
                    if i == ordered_concepts[h]:
                        for j in range(0, sensitivity):  # Checks the next X words for connecting verb
                            for k in tags_check:
                                if (tokens_with_tags[token_location + j][1] == tags[k]) and (
                                    tokens_with_tags[token_location + j][0].lower() != ordered_concepts[h]):
                                    if tokens_with_tags[token_location + j][0].lower() in ordered_concepts:
                                        pass
                                    else:
                                        for l in range(0, sensitivity):  # Checks the next X words for connecting concept
                                            for m in ordered_concepts:
                                                if (tokens[token_location + j + l].lower() == m) and (
                                                    tokens[token_location + j + l].lower() != ordered_concepts[h]) and (
                                                    tokens[token_location + j + l].lower() != tokens[
                                                        token_location + j].lower()):
                                                    if ordered_concepts[h] + tokens[token_location + j] + tokens[
                                                                        token_location + j + l] in concept_duplication:  # Checks for duplicates
                                                        pass
                                                    else:
                                                        concept_connections.append(
                                                            [])  # Creates three lists inside one concept_connections index
                                                        for o in range(0, 4):  # REMOVE 4TH ADDITION IF NOT NEEDED
                                                            concept_connections[concept_connection_counter].append(
                                                                "")  # Adds concepts to "master list"
                                                        concept_connections[concept_connection_counter][0] = \
                                                        ordered_concepts[h]
                                                        concept_connections[concept_connection_counter][1] = tokens[
                                                            token_location + j]
                                                        concept_connections[concept_connection_counter][2] = tokens[
                                                            token_location + j + l]
                                                        concept_connections[concept_connection_counter][
                                                            3] = 1  # Counts the amount of times a group is repeated
                                                        # j = 100
                                                        # l = 100
                                                        # print(str(concept_connections[concept_connection_counter][0]) + " " + str(concept_connections[concept_connection_counter][1]) + " " + str(j) + " " + str(concept_connections[concept_connection_counter][2]) + " " + str(l))
                                                        concept_duplication.add(
                                                            ordered_concepts[h] + tokens[token_location + j] + tokens[
                                                                token_location + j + l])
                                                        concept_connection_counter = concept_connection_counter + 1

                except IndexError:
                    pass
                token_location = token_location + 1  # Tracks index of token

    except UnboundLocalError:
        pass

    nodelistA = []  # This list will hold the concepts
    nodelistB = []  # This list will hold the verbs

    for x in range(0, concept_connection_counter):
        if concept_connections[x][0] in G.nodes():  # Adds a new node
            pass
        else:
            G.add_node(concept_connections[x][0])
            nodelistA.append(concept_connections[x][0])  # Sets node to concept group

        if concept_connections[x][1] in G.nodes():  # Adds a new node
            pass
        else:
            G.add_node(concept_connections[x][1])
            nodelistB.append(concept_connections[x][1])  # Sets node to verb group

        if concept_connections[x][2] in G.nodes():  # Adds a new node
            pass
        else:
            G.add_node(concept_connections[x][2])
            nodelistA.append(concept_connections[x][2])  # Sets node to concept group

        a = G.nodes().index(concept_connections[x][0])  # Stores index of node
        b = G.nodes().index(concept_connections[x][1])

        if str(a) + str(b) in node_duplication:  # Checks if the node is already placed
            for o in range(0, node_connection_counter):
                if node_connections[o][0] == a and node_connections[o][1] == b:
                    node_connections[o][2] = node_connections[o][
                                                 2] + 1  # Adds one to the weight counter of node connections
                    o = node_connection_counter
        else:
            node_connections.append([])  # Adds the node connections to a list
            for c in range(0, 3):
                node_connections[node_connection_counter].append("")
            node_connections[node_connection_counter][0] = a
            node_connections[node_connection_counter][1] = b
            node_connections[node_connection_counter][2] = 1
            node_connection_counter = node_connection_counter + 1
            node_duplication.add(str(a) + str(b))

        a = G.nodes().index(concept_connections[x][1])  # Same as above
        b = G.nodes().index(concept_connections[x][2])

        if str(a) + str(b) in node_duplication:
            for o in range(0, node_connection_counter):
                if node_connections[o][0] == a and node_connections[o][1] == b:
                    node_connections[o][2] = node_connections[o][2] + 1
                    o = node_connection_counter
        else:
            node_connections.append([])
            for c in range(0, 3):
                node_connections[node_connection_counter].append("")
            node_connections[node_connection_counter][0] = a
            node_connections[node_connection_counter][1] = b
            node_connections[node_connection_counter][2] = 1
            node_connection_counter = node_connection_counter + 1
            node_duplication.add(str(a) + str(b))

        G.add_edge(concept_connections[x][0], concept_connections[x][1])
        G.add_edge(concept_connections[x][1], concept_connections[x][2])

    e = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.spring_layout(G, scale=50)

    plt.figure(num=None, figsize=(40, 22.5), dpi=120)

    try:
        nodes = nx.draw_networkx_nodes(G, pos, nodelist=nodelistA, node_size=200, node_color='cyan')

        nodes.set_edgecolor('white')

        nodes = nx.draw_networkx_nodes(G, pos, nodelist=nodelistB, node_size=200, node_color='white')

        nodes.set_edgecolor('white')

        nx.draw_networkx_edges(G, pos, edgelist=e, width=2, edge_color="gray", alpha=0.7)

        nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    except AttributeError:
        pass

    plt.axis('off')
    # plt.show()

    for x in G.nodes():
        node_list.append(x)
    try:
        save_format = str(save_format)

    except UnboundLocalError:
        pass

    save_name = str(save_name)

    if save_type == "PDF":
        new_name = save_name + ".pdf"
        plt.savefig('/home/dre/web2py/applications/concept_map/uploads/' + new_name)  # Creates pdf file
        pathfilename = os.path.join(request.folder, 'uploads/', new_name)
        return response.stream(open(pathfilename, 'rb'), chunk_size=10 ** 6)

    if save_type == "TXT":
        new_name = save_name + ".txt"
        file = open('/home/dre/web2py/applications/concept_map/uploads/' + new_name, "w")  # Creates txt file
        for x in range(0, concept_connection_counter):  # Adds concepts to file
            file.write(concept_connections[x][0] + chr(9) + concept_connections[x][1] + chr(9) + concept_connections[x][
                2] + "\n")
        file.close()  # Saves and closes the file
        pathfilename = os.path.join(request.folder, 'uploads/', new_name)
        return response.stream(open(pathfilename, 'rb'), chunk_size=10 ** 6)

    gold_out_1_t = ""

    gold_out_2_t = ""

    gold_out_3_t = ""

    gold_out_4_t = ""

    try:
        if g_standard != "-":

            tokens = nltk.word_tokenize(g_standard)  # Creates tokens

            number_of_tokens = len(tokens)  # Counts the number of tokens

            gold_standard = []

            for x in range(0, number_of_tokens):
                if (x % 3 == 0 or x == 0) and (x < number_of_tokens - 2):
                    gold_standard.append(tokens[x] + " " + tokens[x + 1] + " " + tokens[x + 2])
                    gold_standard.append(tokens[x + 2] + " " + tokens[x + 1] + " " + tokens[x])

            concept_comparison = []

            for x in range(0, concept_connection_counter):
                if x < concept_connection_counter:
                    concept_comparison.append(str(concept_connections[x][0]) + " " + str(concept_connections[x][1]) + " " + str(
                        concept_connections[x][2]))

            concept_comparison = set(concept_comparison)

            concept_comparison = list(concept_comparison)

            number_of_master_prop = number_of_tokens / 3

            similar_prop = 0

            good_prop = []

            for x in gold_standard:
                for y in concept_comparison:
                    if x == y:
                        similar_prop = similar_prop + 1
                        good_prop.append(y)

            for x in good_prop:
                try:
                    concept_comparison.remove(x)
                except ValueError:
                    pass

            all_syn = set()

            for f in concept_comparison:
                for g in gold_standard:
                    try:
                        compare_syn = nltk.word_tokenize(f)
                        concept_syn_1 = wn.synsets(compare_syn[0])
                        concept_syn_2 = wn.synsets(compare_syn[1])
                        concept_syn_3 = wn.synsets(compare_syn[2])
                        concept_syn_1 = concept_syn_1[0]
                        concept_syn_2 = concept_syn_2[0]
                        concept_syn_3 = concept_syn_3[0]
                        compare_syn_b = nltk.word_tokenize(g)
                        concept_syn_1_b = wn.synsets(compare_syn_b[0])
                        concept_syn_2_b = wn.synsets(compare_syn_b[1])
                        concept_syn_3_b = wn.synsets(compare_syn_b[2])
                        concept_syn_1_b = concept_syn_1_b[0]
                        concept_syn_2_b = concept_syn_2_b[0]
                        concept_syn_3_b = concept_syn_3_b[0]

                        sim_1 = concept_syn_1.path_similarity(concept_syn_1_b)

                        sim_2 = concept_syn_2.path_similarity(concept_syn_2_b)

                        sim_3 = concept_syn_3.path_similarity(concept_syn_3_b)

                        if (.4 < sim_1 < 1) and (.4 < sim_2 < 1) and (.4 < sim_3 < 1):
                            good_prop.append(f)
                            concept_comparison.remove(f)
                            similar_prop = similar_prop + 1
                            print(f)
                            print("HERE")

                    except IndexError:
                        pass
                    except UnicodeDecodeError:
                        pass

            similar_prop = float(similar_prop)

            number_of_master_prop = float(number_of_master_prop)

            similarity_percentage = 0

            similarity_percentage = float(similarity_percentage)

            similarity_percentage = ((similar_prop) / (number_of_master_prop)) * 100

            if similarity_percentage>100:
                similarity_percentage = 100
                similar_prop = number_of_master_prop

            num_useless = concept_connection_counter - similar_prop

            if gold_standard:
                gold_out_1_t = "The student had " + str(int(similar_prop)) + " propositions in common with the gold standard of " + str(
                    int(number_of_master_prop)) + " propositions."

                gold_out_2_t = str(int(similar_prop)) + "/" + str(int(number_of_master_prop)) + " = " + str(similarity_percentage) + "%"

                gold_out_3_t = "The unnecessary propositions were: "

                gold_out_4_t = concept_comparison

            else:
                pass
    except UnboundLocalError:
        pass

    return dict(form=form, error=error, up_form = up_form, text_doc = text_doc, gold_doc = gold_doc, text_name = text_name, gold_name = gold_name, gold_out_1_t = gold_out_1_t, gold_out_2_t = gold_out_2_t, gold_out_3_t = gold_out_3_t, gold_out_4_t = gold_out_4_t)


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


