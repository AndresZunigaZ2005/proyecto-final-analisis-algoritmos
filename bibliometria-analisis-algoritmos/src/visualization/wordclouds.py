from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def generate_wordcloud(texts, out_path):
    wc = WordCloud(width=1200, height=600, background_color='white', collocations=False).generate(" ".join(texts))
    plt.figure(figsize=(12,6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
