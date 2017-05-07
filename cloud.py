from wordcloud import WordCloud, STOPWORDS
from os import path
import matplotlib.pyplot as plt

def cloud(textfile):
    d = path.dirname(__file__)
    text = open(path.join(d, textfile + '.txt'), encoding='UTF-8').read()
    filter_title = textfile
    stopwords = set(STOPWORDS)
    stopwords.add("RT")
    stopwords.add("CO")
    stopwords.add("HTTPS")
    stopwords.add("AMP")
    stopwords.add("RETWEET")
    stopwords.add(filter_title)
    wordcloud = WordCloud(max_font_size=60, stopwords=stopwords)
    wordcloud.generate(text)
    stopwords.remove(filter_title)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def main():
    cloud(textfile='ObamaCare')


if __name__ == '__main__':
    main()

