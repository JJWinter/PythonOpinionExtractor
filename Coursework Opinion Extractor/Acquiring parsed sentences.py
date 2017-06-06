__author__ = 'jw468'
from sussex_nltk.parse import load_parsed_dvd_sentences


def dependants(aspect):
    parsed_sentences = load_parsed_dvd_sentences(aspect)
    dependants = []
    for parsed_sentence in parsed_sentences:
        aspect_tokens = parsed_sentence.get_query_tokens(aspect)
        for aspect_token in aspect_tokens:
            dependants.append(parsed_sentence.get_dependants(aspect_token))
    return dependants


# def dependants2(aspect):
#     parsed_sentences = load_parsed_dvd_sentences(aspect)
#     dependants = []
#     for parsed_sentence in parsed_sentences:
#         aspect_tokens = parsed_sentence.get_query_tokens(aspect)
#         for aspect_token in aspect_tokens:
#             #pass
#             dependants = parsed_sentence.get_dependants(aspect_token)
#         for dependant in dependants:
#             print dependant
#     return dependants

def heads(aspect):
    parsed_sentences = load_parsed_dvd_sentences(aspect)
    heads = []
    for parsed_sentence in parsed_sentences:
        aspect_tokens = parsed_sentence.get_query_tokens(aspect)
        for aspect_token in aspect_tokens:
            heads.append(parsed_sentence.get_head(aspect_token))
    return heads

print "---------"


print dependants("plot")
heads("plot")