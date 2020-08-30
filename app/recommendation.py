"""
This module contains method of computing articles' similarity and article trending scores
"""
import operator
import re
import gensim.models
import numpy as np
import scipy
from nltk.corpus import stopwords


def remove_tags(content):
    """remove the html tag in article for better a precision

    :param content: the article content(title + body)
    :return: String with removed article contents
    """
    return re.sub("<.*?>", " ", content)


def pre_process(content):
    """preprocess the content, includes remove stop word, remove non-alphabet in the content.

    :param content: the article content(title + body)
    :return: List of String with pre-processed words.
    """
    stop_word = stopwords.words('english')
    words = [word for word in content.split(' ') if word.isalpha()]
    words = [word for word in words if word not in stop_word]
    return words


def cosine_similarity(d1, d2, model):
    """compare similarity between two documents,

    This method convert documents content into vectors using word2vec model,
    then compare the vector using cosine similarity.

    :param d1: document 1's content in list of word
    :param d2: document 2's content in list of word
    :param model: the word2vec model loaded.
    :return: different in score between d1 and d2
    """
    d1_vocabs = [word for word in d1 if word in model.vocab]
    d2_vocabs = [word for word in d2 if word in model.vocab]

    d1_vector = np.mean(model[d1_vocabs], axis=0)
    d2_vector = np.mean(model[d2_vocabs], axis=0)
    cosine_score = 1.0 - scipy.spatial.distance.cosine(d1_vector, d2_vector)
    return cosine_score


def update_related(all_article):
    """this method update the related_article table

    pre-process includes remove html tag, delete english stop words,
    remove non-alphabet and add dummy string to help the produce a valid vectors

    :param all_article: a list of articles with short description, body(content) and sys_id, [{articles: {sys_id:...}}]
    :return: sorted_knowledge_score(method for computes similarity of documents and sort from high to low)
    """
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
    """this method computes favorites score of articles, which contributes 70% of trending score

    favorite score use a ranking that is based on net_votes of articles,
    is if rank = 1, then score = 1 - 1(rank)/ article amounts

    :param articles: a list of articles with net_votes [{article:net_votes}]
    :return: list of articles with favorite score. [{article:favorite_score}]
    """
    knowledge_favorite_score = {}
    sorted_knowledge_favorite = sorted(articles, key=lambda item: item['net_votes'], reverse=True)
    i = 0
    for knowledge in sorted_knowledge_favorite:
        i += 1
        knowledge_favorite_score[knowledge['sys_id']] = (1.0 - (i / len(sorted_knowledge_favorite))) * 0.7

    return knowledge_favorite_score


def compute_view_score(articles):
    """this method computes view score of articles, which contributes 30% of trending score

    view score use a ranking that is based on net_view of articles,
    is if rank = 1, then score = 1 - 1(rank)/ article amounts

    :param articles: a list of articles with view_count [{article:view_count}]
    :return: list of articles with view score. [{article:viewScore}]
    """
    knowledge_view_score = {}
    sort_knowledge_view = sorted(articles, key=lambda item: item['view_count'], reverse=True)
    print(sort_knowledge_view)
    i = 0
    for knowledge in sort_knowledge_view:
        i += 1
        knowledge_view_score[knowledge['sys_id']] = (1.0 - (i / len(sort_knowledge_view))) * 0.3
    return knowledge_view_score


def compute_trending_score(knowledge_favorite_score, knowledge_view_score):
    """this method computes trending score of articles,
    made use of compute_view_score and compute_favorite_score methods.


    :param knowledge_favorite_score: a list of articles with view_count
    :param knowledge_view_score: a list of articles with view_count
    :return: list of articles with trending score.[{article:trendingScore}]
    """
    knowledge_trending_score = {}
    for knowledge in knowledge_favorite_score:
        knowledge_trending_score[knowledge] = knowledge_view_score[knowledge] + knowledge_favorite_score[knowledge]
    return knowledge_trending_score


def sort_knowledge_score(knowledge_dict, knowledge_number_list, model):
    """this method computes the similarity score of articles to all articles
    and then sort articles using similarity score from high to low.

    :param knowledge_dict: a list of articles with words in list, [{knowledge: [words...]}]
    :param knowledge_number_list: list of knowledge Numbers [knowldgeNumber,....]
    :param model: the word2vec model loaded.
    :return: list of articles with list of similarity score of all articles
    """
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
    """this method used by the knowledge_service function to compute list of article with trending score

    :param sorted_favorite: list of articles with net_votes sorted by date.
    :param sort_view: list of articles with view_count sorted by date.
    :return: list of article with trending score
    """
    favorite_score = compute_favorite_score(sorted_favorite)
    view_score = compute_view_score(sort_view)
    trending_score = compute_trending_score(favorite_score, view_score)
    return trending_score
