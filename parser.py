import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S Conj S
NP -> N | Det N | NP PP | Det AP N
VP -> V | V NP | V PP | Adv VP | VP Adv
AP -> Adj | Adj AP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Converting all the characters to lowercase
    sentence = sentence.lower()


    words = nltk.wordpunct_tokenize(sentence)
    list_of_words = []

    # Checking if the word has at least one alphabetic character
    for verify in words:
        if any(character.isalpha() for character in verify):
           list_of_words.append(verify)

    return list_of_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # List of noun phrase chuncks
    list_np = [] 

    # Iterate through all subtrees in the sentence tree
    for subtree in tree.subtrees():
        # Check if the subtree has the label 'NP'
        if subtree.label() == 'NP':
            # Initialize a flag to check if the NP contains other NPs within it
            contains_other_np = False
            for subsubtree in subtree.subtrees():
                if subsubtree != subtree and subsubtree.label() == 'NP':
                    # If the subsubtree contains another NP with the label 'NP', set the flag to True and break out of the loop
                    contains_other_np = True
                    break
            # If the NP does not contain other NPs as subtrees, add it to the list of NP chunks
            if not contains_other_np:
                list_np.append(subtree)

    return list_np


if __name__ == "__main__":
    main()