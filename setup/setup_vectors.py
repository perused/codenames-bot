import gensim.downloader
import os


def main():
    model = gensim.downloader.load('glove-wiki-gigaword-300')
    model.save(os.path.join("components", "glove300.word_vectors"))


if __name__ == "__main__":
    main()
