import json
import re
from pprint import pprint
import urllib2
from bs4 import BeautifulSoup

import nltk
from nltk import sent_tokenize, word_tokenize, ne_chunk
from nltk.corpus import stopwords


def get_dict_topn(thedict, n):
	return [v for k,v in enumerate(sorted(thedict.items(), key=lambda x: x[1])[::-1]) if k<n]

def text_to_token_dict(text, stopwords=None, dostem=False):
	tokens = word_tokenize(text)
	token_dict = {}

	if dostem ==True:
		tokens = stem_words(tokens)

	if stopwords !=None:
		tokens = remove_stopwords(stopwords, tokens)

	token_dict = count_tokens(tokens)
	return token_dict

def count_tokens(tokens):
	token_dict = {}
	for t in tokens:
		if t in token_dict:
			token_dict[t]+=1
		else:
			token_dict[t] = 1

	return token_dict

def _lambda(word, token_dict):
	if word in token_dict:
		return True
	else:
		return False

def main():
	filename = '/home/grant/Desktop/golden_globe/goldenglobes2015.json'
	count = 0
	# links = {}

	best_dressed_links = {}

	with open(filename, 'r') as f:
		best_dressed = []
		best_words = [
						["best", "dressed"],
						["Best", "dressed"],
						["best", "Dressed"],
						["Best", "Dressed"],
						["fashion"],
						["Fashion"],
						["Red", "Carpet"],
						["Red", "carpet"],
						["red", "Carpet"],
						["red", "carpet"],
					 ]

		for line in f:
			if count>1000000:
				break

			text  = json.loads(line)['text']
			print text

			token_dict = text_to_token_dict(text, None, False)

			count+=1
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


			for bestlist in best_words:
				if all([_lambda(word,token_dict) for word in bestlist]):
					if urls != []:
						for url in urls:
							if url in best_dressed_links:
								best_dressed_links[url]+=1
							else:
								best_dressed_links[url]=1


	top_best = get_dict_topn(best_dressed_links, 100)
	pprint(top_best)

	def links_to_imgs(links):
		imgdict = {}
		imgdict_tolink ={}
		for link,count in links:
			try:
				html = urllib2.urlopen(link)
			except:
				continue
			soup = BeautifulSoup(html)
			for img in soup.findAll('img'):
				src = img.get('src')
				imgdict_tolink[src] = link
				if src in imgdict:
					imgdict[src]+=1
				else:
					imgdict[src]=1
		return imgdict, imgdict_tolink


	def remove_profile_pics(img_dict):
		new_dict = {}
		for img in img_dict:
			if img != None:
				isprofile = re.findall('profile', img)
				isemoji   = re.findall('abs.twimg', img)
				isgrava   = re.findall('avatar', img)
				isfake    = re.findall('^/', img)
				isdata    = re.findall('^data:', img)
				isspinner = re.findall('spinner', img)
				if isprofile == [] and isemoji == [] and isgrava==[] and isfake==[] and isdata==[] and isspinner==[]:
					new_dict[img] = img_dict[img]

		return new_dict



	best_dressed_images, best_dressed_imgdict_tolink = links_to_imgs(top_best)
	best_dressed_dict   = remove_profile_pics(best_dressed_images)

	def tup_to_list(outerlist):
		final_list = []
		for innerlist in outerlist:
			final_list.append(innerlist[0])
		return final_list

	def _tup_to_list(outerlist,lookup):
		final_list = []
		for innerlist in outerlist:
			final_list.append({"img" : innerlist[0], "link": lookup[innerlist[0]]})
		return final_list

	best_dressed_images_list = _tup_to_list(get_dict_topn(best_dressed_dict,30), best_dressed_imgdict_tolink)
	#best_dressed_images_list = tup_to_list(get_dict_topn(best_dressed_dict,20))

	print best_dressed_images_list

	return best_dressed_images_list


if __name__ == "__main__":
	main()