__author__ = 'jw468'
from sussex_nltk.parse import load_parsed_dvd_sentences
from sussex_nltk.parse import load_parsed_example_sentences

##########EXAMPLES TEST SET##########
# parsed_example_sentences = load_parsed_example_sentences()
#
# # To inspect the sentences, you could print them straight out
# for parsed_sentence in parsed_example_sentences:
#     print "--- Sentence ---"
#     print parsed_sentence


def opinion_extractor(aspect_token, parsed_sentence):

    # Your function will have 3 steps:

    # i. Initialise a list of opinions
    opinions = []

    # ii. Find opinions (as an example we get all the dependants of the aspect token that have the relation "det")
    #opinions += [dependant.form for dependant in parsed_sentence.get_dependants(aspect_token) if dependant.pos == "JJ" if dependant.deprel == "nsubj"]
    head = parsed_sentence.get_head(aspect_token)
    if head.pos == "JJ" and aspect_token.deprel == "nsubj":
        opinions.append(head.form)
    # You can continue to add to "opinions". Remember you can get the head of a token, and filter by PoS tag or Deprel too!

    # iii. Return the (possibly empty) list of opinions
    return opinions



aspect = "plot"   # Set this to the aspect token you're interested in
save_file_path = r"\\smbhome.uscs.susx.ac.uk\jw468\Documents\Course Modules\Year 2\Natural Language Engineering\Lab 8\output2.txt"    # Set this to the location of the file you wish to create/overwrite with the saved output.

# Tracking these numbers will allow us to see what proportion of sentences we discovered features in
sentences_with_discovered_features = 0  # Number of sentences we discovered features in
total_sentences = 0  # Total number of sentences

# This is a "with statement", it invokes a context manager, which handles the opening and closing of resources (like files)
with open(save_file_path, "w") as save_file:  # The 'w' says that we want to write to the file

    # Iterate over all the parsed sentences
    for parsed_sentence in load_parsed_example_sentences():

        total_sentences += 1  # We've seen another sentence

        opinions = [] # Make a list for holding any opinions we extract in this sentence

        # Iterate over each of the aspect tokens in the sentences (in case there is more than one)
        for aspect_token in parsed_sentence.get_query_tokens(aspect):

            # Call your opinion extractor
            opinions += opinion_extractor(aspect_token, parsed_sentence)

        # If we found any opinions, write to the output file what we know.
        if opinions:
            # Currently, the sentence will only be printed if opinions were found. But if you want to know what you're missing, you could move the sentence printing outside the if-statement

            # Print a separator and the raw unparsed sentence
            save_file.write("--- Sentence: %s ---\n" % parsed_sentence.raw())  # "\n" starts a new line
            # Print the parsed sentence
            save_file.write("%s\n" % parsed_sentence)
            # Print opinions extracted
            save_file.write("Opinions: %s\n" % opinions)

            sentences_with_discovered_features += 1  # We've found features in another sentence

print "%s sentences out of %s contained features" % (sentences_with_discovered_features, total_sentences)


