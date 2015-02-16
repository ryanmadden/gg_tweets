import json
import re
from pprint import pprint
import urllib2
from bs4 import BeautifulSoup

import nltk
from nltk import sent_tokenize, word_tokenize, ne_chunk
from nltk.corpus import stopwords
import timer


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

def _tup_to_list(outerlist,lookup):
	final_list = []
	for innerlist in outerlist:
		final_list.append({"img" : innerlist[0], "link": lookup[innerlist[0]]})
	return final_list

def main():
	f_2015_mini = './gg15mini.json'
	f_2015      = './goldenglobes2015.json'
	f_2013      = './gg2013.json'
	count = 0

	best_dressed_links = {}

	#This method only works for the 2015 file as each tweet is on an individual line; use the map(json.loads,f) method in general
	#unfortunately my computer explodes when I try doing that on the 2015 file as it tries to load the ENTIRE data into main memory
	with open(f_2015, 'r') as f:
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
			count+=1
			if count>1000000:
				break

			text  = json.loads(line)['text']
			print text
			token_dict = text_to_token_dict(text, None, False)
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

	best_dressed_images, best_dressed_imgdict_tolink = links_to_imgs(top_best)
	best_dressed_dict   = remove_profile_pics(best_dressed_images)

	best_dressed_images_list = _tup_to_list(get_dict_topn(best_dressed_dict,30), best_dressed_imgdict_tolink)

	print best_dressed_images_list

	return best_dressed_images_list


if __name__ == "__main__":
	main()