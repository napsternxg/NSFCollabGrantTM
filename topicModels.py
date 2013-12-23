from text2corpus_dict import *

def runTopicModels(nsfdiv_name):
	logger = logging.getLogger('runTopicModel')
	dict_file = nsfdiv_name.replace(' ', '_') # Filenames represent the NSF division name
	dictionary = corpora.Dictionary.load(DIR_NAME+dict_file+".dict")
	logging.info("Dictionary Loaded")
	corpus = corpora.MmCorpus(DIR_NAME+dict_file+".mm")
	logging.info("Corpus Loaded")
	logging.info("Corpus statistics: %s", corpus)

	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	logging.info("TfIdf Transformation done on corpus")
	model = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=10, passes = 10)
#	corpus_lda = model[corpus]
	logging.info("Printing topics")
	model.save(DIR_NAME+dict_file+".lda")
	logging.info("Model saved to file: %s", DIR_NAME+dict_file+".lda")
#	model.show_topics(topics=10, topn=10, log=False, formatted=True)
	
def getTopics(nsfdiv_name):
	dict_file = nsfdiv_name.replace(' ', '_') # Filenames represent the NSF division name
	model = models.LdaModel.load(DIR_NAME+dict_file+".lda")
	print "Topics for: "+dict_file
	return model.show_topics(topics=10, topn=10, log=False, formatted=False)

def printTopics(nsfdiv_name):
	topics = getTopics(nsfdiv_name)
	topic_word_list = []
	count = 1
	for topic in topics:
		topic_words = []
		print "Topic {0}:".format(count),
		for word in topic:
			topic_words.append(word[1])
		topic_word_list.append(topic_words)
		print ';'.join(topic_words)
		count += 1

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("func")
	args = parser.parse_args()
	logger = logging.getLogger('main')
	if args.func == 'tm':
		for nsfdiv_name in nsf_div_list:
			logger.info("Processing NSFDivision: %s", nsfdiv_name)
			runTopicModels(nsfdiv_name)
	elif args.func == 'print':
		for nsfdiv_name in nsf_div_list:
			logger.info("Getting topics for NSFDivision: %s", nsfdiv_name)
			printTopics(nsfdiv_name)
