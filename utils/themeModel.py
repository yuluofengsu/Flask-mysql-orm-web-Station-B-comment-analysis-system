from utils.getPublicData import getAllVideoCommentsList,getAllVideoList
import gensim
from gensim import corpora
from gensim.models import LdaModel
import jieba
import datetime
def timestamp_to_datetime(t):
    if t >= 86400:
        return datetime.datetime.fromtimestamp(t)
    else:
        return datetime.datetime.fromtimestamp(t, pytz.timezone('UTC')).replace(tzinfo=None)  # 世界标准时间

def stopWordList():
    stopwords = '而|何|之|乎|者|也|则|来|者|不|自|得|的|去|无|一|可|是|已|此|上|中|兮|三|\n|)|\ue85d|\ue85f|:|?|{|}|“|”|。|，|、|【|】|\u3000|◎|.|（|！|：|(|？| |'.split("|")
    return stopwords

def seg_depart(sentence):
        sentence_depart = jieba.cut(" ".join([x[-1] for x in sentence]).strip())
        stopWords = stopWordList()
        outStr = []
        for word in sentence_depart:
            if word not in stopWords:
                if word != '\t' and word != ' ':
                    outStr.append(word)
        return outStr

def main(time):
    commentList =  getAllVideoCommentsList()
    content = ''
    for i in commentList:
        if time == str(timestamp_to_datetime(int(i[-2])))[:7]:
            content += i[4]

    sentences = seg_depart(content)

    dictionary = corpora.Dictionary([sentences])
    corpus = [dictionary.doc2bow([tokens]) for tokens in sentences]

    lda_model = LdaModel(corpus, num_topics=6, id2word=dictionary)

    # 打印主题词汇
    topics = lda_model.print_topics(num_words=10)
    topicsDic = {}
    for topic in topics:
        keyword = topic[1].split(' + ')[-1].split('*')
        topicsDic[str(keyword[1])] = float(keyword[0])
    return list(topicsDic.items()),content

if __name__ == '__main__':
    main('白日依山尽，黄河入海流。欲穷千里目，更上一层楼。')

