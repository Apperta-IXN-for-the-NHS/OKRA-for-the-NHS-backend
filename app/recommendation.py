import operator
import re
import gensim.models
import numpy as np
import scipy
from nltk.corpus import stopwords


# remove <> tags in the ariticle body
def remove_tags(content):
    return re.sub("<.*?>", " ", content)


# preprocessed the data using
def pre_process(content):
    stop_word = stopwords.words('english')
    words = [word for word in content.split(' ') if word.isalpha()]
    words = [word for word in words if word not in stop_word]
    return words


#  uncomment to run initial model training and prediction on similairty
def cosine_similarity(d1, d2, model):
    d1_vocabs = [word for word in d1 if word in model.vocab]
    d2_vocabs = [word for word in d2 if word in model.vocab]

    d1_vector = np.mean(model[d1_vocabs], axis=0)
    d2_vector = np.mean(model[d2_vocabs], axis=0)
    cosine_score = 1.0 - scipy.spatial.distance.cosine(d1_vector, d2_vector)
    return cosine_score


def update_related(all_article):
    path = 'GoogleNews-vectors-negative300-SLIM.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    knowledge_dict = {}
    knowledge_number_list = []
    for article in all_article:
        if article['short_description'] is not None:
            short_description = article['short_description']
        else:
            short_description = ""
        if article['body'] is not None:
            body = article['body']
        else:
            body = ''
        knowledge_dict[article['sys_id']] = pre_process(remove_tags(short_description + body + "used for remove bug"))
        knowledge_number_list.append(article['sys_id'])

    return sort_knowledge_score(knowledge_dict, knowledge_number_list, model)


def compute_favorite_score(articles):
    knowledge_favorite_score = {}
    sorted_knowledge_favorite = sorted(articles, key=lambda item: item['net_votes'], reverse=True)
    i = 0
    for knowledge in sorted_knowledge_favorite:
        i += 1
        knowledge_favorite_score[knowledge['sys_id']] = (1.0 - (i / len(sorted_knowledge_favorite))) * 0.7

    return knowledge_favorite_score


def compute_view_score(articles):
    knowledge_view_score = {}
    sort_knowledge_view = sorted(articles, key=lambda item: item['view_count'], reverse=True)
    print(sort_knowledge_view)
    i = 0
    for knowledge in sort_knowledge_view:
        i += 1
        knowledge_view_score[knowledge['sys_id']] = (1.0 - (i / len(sort_knowledge_view))) * 0.3
    return knowledge_view_score


def compute_trending_score(knowledge_favorite_score, knowledge_view_score):
    knowledge_trending_score = {}
    for knowledge in knowledge_favorite_score:
        knowledge_trending_score[knowledge] = knowledge_view_score[knowledge] + knowledge_favorite_score[knowledge]
    return knowledge_trending_score


# this method computes the similarity score and then sort article from high to low.
def sort_knowledge_score(knowledge_dict, knowledge_number_list, model):
    all_knowledge_score = {}
    for i in range(len(knowledge_number_list)):
        print(i)
        knowledge_score = {}
        sorted_knowledge_score = {}
        for j in range(len(knowledge_number_list)):
            if i != j:
                score = cosine_similarity(knowledge_dict[knowledge_number_list[i]], knowledge_dict[knowledge_number_list[j]], model)
                knowledge_score[knowledge_number_list[j]] = score
            #     + knowledgeTrendingScore[j]
            sorted_knowledge_score = sorted(knowledge_score.items(), key=operator.itemgetter(1), reverse=True)
        all_knowledge_score[knowledge_number_list[i]] = sorted_knowledge_score
    return all_knowledge_score


def return_trending_score(sorted_favorite, sort_view):
    favorite_score = compute_favorite_score(sorted_favorite)
    view_score = compute_view_score(sort_view)
    trending_score = compute_trending_score(favorite_score, view_score)
    return trending_score
