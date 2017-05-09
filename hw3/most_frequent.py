import collections
import functools
import random

from data import *


def most_frequent(counts_dict):
    return max(counts_dict.items(), key=lambda (element, count): count)[0]


def most_frequent_train(train_data):
    """
    Gets training data that includes tagged sentences.
    Returns a dictionary that maps every word in the training set to its most frequent tag.
    """
    ### YOUR CODE HERE
    word2tag_count = collections.defaultdict(functools.partial(collections.defaultdict, int))
    for sentence in train_data:
        for word, tag in sentence:
            word2tag_count[word][tag] += 1
    return {word: most_frequent(tag_count) for word, tag_count in word2tag_count.iteritems()}
    ### END YOUR CODE


def most_frequent_eval(original_sentences, sentences, pred_tags, crafted_only):
    """
    Gets test data and tag prediction map.
    Returns an evaluation of the accuracy of the most frequent tagger.
    """
    ### YOUR CODE HERE
    count_good = 0
    total_count = 0
    for original_sentence, sentence in zip(original_sentences, sentences):
        for (orig_word, _), (word, tag) in zip(original_sentence, sentence):
            if crafted_only and word not in CRAFTED_CATEGORIES:
                continue
            if pred_tags[word] == tag:
                count_good += 1
            elif crafted_only:
                print orig_word, word, tag, pred_tags[word]
            total_count += 1
    return float(count_good) / total_count
    ### END YOUR CODE


if __name__ == "__main__":
    assert most_frequent(collections.Counter([1, 2, 1, 1, 2, 3,])) == 1
    a = read_conll_pos_file("Penn_Treebank/train.gold.conll")
    b = read_conll_pos_file("Penn_Treebank/dev.gold.conll")
    dev_sents1 = random.sample(a + b, len(b))
    train_sents = [x for x in a + b if x not in dev_sents1]
    vocab = compute_vocab_count(train_sents)
    train_sents = preprocess_sent(vocab, train_sents)
    dev_sents = preprocess_sent(vocab, dev_sents1)

    model = most_frequent_train(train_sents)
    print "accuracy on crafted category words (dev): {}".format(most_frequent_eval(dev_sents1, dev_sents, model, True))
    print "dev: most frequent acc: {}".format(most_frequent_eval(dev_sents, dev_sents, model, True))

    if os.path.exists('Penn_Treebank/test.gold.conll'):
        test_sents = read_conll_pos_file("Penn_Treebank/test.gold.conll")
        test_sents = preprocess_sent(vocab, test_sents)
        print "test: most frequent acc: {}".format(most_frequent_eval(test_sents, test_sents, model, False))
