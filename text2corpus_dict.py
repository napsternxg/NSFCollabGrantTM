from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from getData import *
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

nsf_div_list = getNSFDivisions()
stoplist = stopwords.words('english')
DIR_NAME="corpus_dict_data/"

def convert_doc2corpora(documents, nsfdiv_name):
	logger = logging.getLogger('doc2corpora')
	texts = []
	logger.info("No of Documents: %d", len(documents))
# Remove stoplist words
	texts = [[word for word in unicode(document, errors='replace').lower().split() if word not in stoplist]
		for document in documents]
	logger.info("Stopwords removed")
	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
# Tokenize the documents
	texts = [[word for word in text if word not in tokens_once]
		for text in texts]
	logger.info("Documents tokenized")
# Create dictionary of words
	dictionary = corpora.Dictionary(texts)
	dict_file = nsfdiv_name.replace(' ', '_') # Filenames represent the NSF division name
	dictionary.save(DIR_NAME+dict_file+".dict")
	logger.info("Dictionary Created")
	corpus = [dictionary.doc2bow(text) for text in texts]
	corpora.MmCorpus.serialize(DIR_NAME+dict_file+".mm", corpus) # store to disk, for later use
	logger.info("Corpus Created")
	return "Success"


if __name__ == "__main__":
	logger = logging.getLogger('main')
	for nsfdiv_name in nsf_div_list:
		logger.info("Processing NSFDivision: %s", nsfdiv_name)
		documents = getAbstractForDiv(nsfdiv_name)
		status = convert_doc2corpora(documents, nsfdiv_name)
		logger.info("Coverstion status: %s", status )
