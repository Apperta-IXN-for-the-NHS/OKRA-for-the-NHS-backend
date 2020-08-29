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
    d1Vocabs = [word for word in d1 if word in model.vocab]
    d2Vocabs = [word for word in d2 if word in model.vocab]

    d1Vector = np.mean(model[d1Vocabs], axis=0)
    d2Vector = np.mean(model[d2Vocabs], axis=0)
    cosine_score = 1.0 - scipy.spatial.distance.cosine(d1Vector, d2Vector)
    return cosine_score


def update_related(all_article):
    path = 'GoogleNews-vectors-negative300-SLIM.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    knowledgeDict = {}
    knowledgeNumberList = []
    for article in all_article:
        if article['short_description'] is not None:
            short_description = article['short_description']
        else:
            short_description = ""
        if article['body'] is not None:
            body = article['body']
        else:
            body = ''
        knowledgeDict[article['sys_id']] = pre_process(remove_tags(short_description
                                                                   + body + "used for remove bug"))
        knowledgeNumberList.append(article['sys_id'])

    return sort_knowledgeScore(knowledgeDict, knowledgeNumberList, model)


def compute_favoriteScore(articles):
    knowledgeFavoriteScore = {}
    sortedKnowledgeFavorite = sorted(articles, key=lambda item: item['net_votes'], reverse=True)
    i = 0
    for knowledge in sortedKnowledgeFavorite:
        i += 1
        knowledgeFavoriteScore[knowledge['sys_id']] = (1.0 - (i / len(sortedKnowledgeFavorite))) * 0.7

    return knowledgeFavoriteScore


def compute_viewScore(articles):
    knowledgeViewScore = {}
    sortKnowledgeView = sorted(articles, key=lambda item: item['view_count'], reverse=True)
    print(sortKnowledgeView)
    i = 0
    for knowledge in sortKnowledgeView:
        i += 1
        knowledgeViewScore[knowledge['sys_id']] = (1.0 - (i / len(sortKnowledgeView))) * 0.3
    return knowledgeViewScore


def compute_trendingScore(knowledge_favorite_score, knowledge_view_score):
    knowledgeTrendingScore = {}
    for knowledge in knowledge_favorite_score:
        knowledgeTrendingScore[knowledge] = knowledge_view_score[knowledge] + knowledge_favorite_score[knowledge]
    return knowledgeTrendingScore


# this method computes the similarity score and then sort article from high to low.
def sort_knowledgeScore(knowledge_dict, knowledge_number_list,model):
    allKnowledgeScore = {}
    for i in range(len(knowledge_number_list)):
        print(i)
        knowledgeScore = {}
        sortedKnowledgeScore = {}
        for j in range(len(knowledge_number_list)):
            score = 0.0
            if i == j:
                b = 0
            else:
                score = cosine_similarity(knowledge_dict[knowledge_number_list[i]], knowledge_dict[knowledge_number_list[j]],model)
                knowledgeScore[knowledge_number_list[j]] = score
            #     + knowledgeTrendingScore[j]
            sortedKnowledgeScore = sorted(knowledgeScore.items(), key=operator.itemgetter(1), reverse=True)
        allKnowledgeScore[knowledge_number_list[i]] = sortedKnowledgeScore
    return allKnowledgeScore


def return_trending_score(sorted_favorite, sort_view):
    favoriteScore = compute_favoriteScore(sorted_favorite)
    viewScore = compute_viewScore(sort_view)
    TrendingScore = compute_trendingScore(favoriteScore, viewScore)
    return TrendingScore

