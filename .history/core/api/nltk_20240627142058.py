import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn


class NLTK:
	nltk.download('punkt')
	nltk.download('averaged_perceptron_tagger')
	nltk.download('wordnet')

	def __init__(self):
		pass

	# Download the necessary NLTK data

	@staticmethod
	def convert_text_infinitive(text: str) -> dict:
		# Tokenize the text
		tokens = word_tokenize(text)

		# POS tagging
		tagged_tokens = nltk.pos_tag(tokens)

		# Function to get the infinitive form of a verb
		def get_infinitive(word):
			lemma = wn.morphy(word, wn.VERB)
			return lemma if lemma else word

		# Extract verbs and convert to infinitive
		verbs_infinitive = {}
		for word, tag in tagged_tokens:
			if tag.startswith('VB'):
				verbs_infinitive[word] = get_infinitive(word)

		# Save the verbs and their infinitives to a JSON file
		output_file = "mnt/data/verbs_infinitive.json"
		with open(output_file, 'w') as f:
			json.dump(verbs_infinitive, f)

		return verbs_infinitive
