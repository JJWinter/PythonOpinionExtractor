__author__ = 'jw468'
from sussex_nltk.parse import load_parsed_dvd_sentences
from sussex_nltk.parse import load_parsed_example_sentences




def opinion_extractor(aspect_token, parsed_sentence):
    opinions = []

    dependants = parsed_sentence.get_dependants(aspect_token)

    #Checks opinions before aspect word
    for d1 in dependants:
        if d1.deprel == "amod":
            opinions.append(d1.form)

            #Checks for negatives
            negs = parsed_sentence.get_dependants(aspect_token)
            for neg in negs:
                if neg.deprel == "neg":
                    if d1.form in opinions:
                        opinions.remove(d1.form)
                    words = ["not",d1.form]
                    joined_string = "-".join(words)
                    opinions.append(joined_string)

            #Checks for Adverbial Modifiers
            dependants2 = parsed_sentence.get_dependants(d1)
            for d2 in dependants2:
                if d2.deprel == "advmod":
                    #Removes non-adverbial-modified opinion if adverbial-modifier found
                    if d1.form in opinions:
                        opinions.remove(d1.form)
                    words = [d2.form, d1.form]
                    joined_string = "-".join(words)
                    opinions.append(joined_string)


    #Checks opinions after aspect word
    head = parsed_sentence.get_head(aspect_token)
    if head.pos == "JJ" and aspect_token.deprel == "nsubj":
        opinions.append(head.form)

        #Checks for negative
        negs = parsed_sentence.get_dependants(head)
        for neg in negs:
            if neg.deprel == "neg":
                #Removes non-negative opinion if negative opinion found
                if head.form in opinions:
                    opinions.remove(head.form)
                words = ["not", head.form]
                joined_string = "-".join(words)
                opinions.append(joined_string)

        #Checks for Adverbial Modifiers
        dependants4 = parsed_sentence.get_dependants(head)
        for d4 in dependants4:
            if d4.deprel == "advmod":
                #Removes non-adverbial-modified opinion if adverbial-modifier found
                if head.form in opinions:
                    opinions.remove(head.form)
                words = [d4.form, head.form]
                joined_string = "-".join(words)
                opinions.append(joined_string)
                #Forms negated-adverbial-modified opinion if found
                negword = ["not", head.form]
                neg_words = "-".join(negword)
                if neg_words in opinions:
                    opinions.remove(neg_words)
                    words = ["not", d4.form, head.form]
                    joined_string = "-".join(words)
                    opinions.append(joined_string)
                    posword = [d4.form, head.form]
                    pos_words = "-".join(posword)
                    opinions.remove(pos_words)

        #Checks for Conjunction
        token = parsed_sentence.get_head(aspect_token)
        dependants = parsed_sentence.get_dependants(token)
        for dependant in dependants:
            if dependant.deprel == "conj":
                words = []
                words.append(dependant.form)
                joined_string = "-".join(words)
                opinions.append(joined_string)
                #Checks for negative
                negs = parsed_sentence.get_dependants(dependant)
                for neg in negs:
                    if neg.deprel == "neg":
                        #Removes non-negative opinion if negative opinion found
                        if dependant.form in opinions:
                            opinions.remove(dependant.form)
                        words = ["not", dependant.form]
                        joined_string = "-".join(words)
                        opinions.append(joined_string)
                #Checks for Adverbial Modifiers
                dependants3 = parsed_sentence.get_dependants(dependant)
                for d3 in dependants3:
                    if d3.deprel == "advmod":
                        #Removes non-adverbial-modified opinion if adverbial-modifier found
                        if dependant.form in opinions:
                            opinions.remove(dependant.form)
                        words = [d3.form, dependant.form]
                        joined_string = "-".join(words)
                        opinions.append(joined_string)
                        #Forms negated-adverbial-modified opinion if found
                        negword = ["not", dependant.form]
                        neg_words = "-".join(negword)
                        if neg_words in opinions:
                            opinions.remove(neg_words)
                            words = ["not", d3.form, dependant.form]
                            joined_string = "-".join(words)
                            opinions.append(joined_string)
                            posword = [d3.form, dependant.form]
                            pos_words = "-".join(posword)
                            opinions.remove(pos_words)



    return opinions



aspect = "dialogue"   # Set this to the aspect token you're interested in
save_file_path = r"\\smbhome.uscs.susx.ac.uk\jw468\Documents\Course Modules\Year 2\Natural Language Engineering\Lab 8\output.txt"    # Set this to the location of the file you wish to create/overwrite with the saved output.

# Tracking these numbers will allow us to see what proportion of sentences we discovered features in
sentences_with_discovered_features = 0  # Number of sentences we discovered features in
total_sentences = 0  # Total number of sentences

# This is a "with statement", it invokes a context manager, which handles the opening and closing of resources (like files)
with open(save_file_path, "w") as save_file:  # The 'w' says that we want to write to the file

    # Iterate over all the parsed sentences
    for parsed_sentence in load_parsed_dvd_sentences("dialogue"):

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


