import gensim.downloader


def main():
    model = gensim.downloader.load('glove-wiki-gigaword-300')
    model.save("glove300.word_vectors")


if __name__ == "__main__":
    main()
