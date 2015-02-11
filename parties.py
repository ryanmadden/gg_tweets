from timer import timeit
import json
import run
import re

def filter_special_words(word):
	if "Globe" in word:
		return False
	if "After" in word:
		return False
	if "The" in word:
		return False
	if "Along" in word:
		return False
	if "GG" in word:
		return False
	return True

def find_party(tweet):
	party_arr = re.findall("((\w+ ){1})party", tweet)
	party_arr.extend(re.findall("((\w+ ){1})after party", tweet))
	filtered_arr = []
	for each in party_arr:
		word = each[0]
		if word[0].isupper():
			if filter_special_words(word):
				filtered_arr.append(word)
	return filtered_arr

def insert_to_dictionary(party, parties_dict):
	if party in parties_dict:
		parties_dict[party] += 1
	else:
		parties_dict[party] = 1 
	return parties_dict


def insert_name_to_dictionary(party, name, parties_dict):
	if party in parties_dict:
		if name not in parties_dict[party]:
			parties_dict[party].append(name)
	else:
		parties_dict[party] = [name]
	return parties_dict

def find_at_name(sentence):
	return re.findall("@\S*", sentence)

@timeit
def main():
	f_2015_mini = './gg15mini.json'
	parties = {}
 	with open(f_2015_mini, 'r') as f:
 		tweets = map(json.loads, f)[0]
 		print "Tweet collection created..."

 		for tweet in tweets: 
 			text = tweet['text']
 			if "party" not in text: continue 

 			party_arr = find_party(text)
 			for party in party_arr:
 				parties = insert_to_dictionary(party, parties)

 		parties_sorted = sorted(parties.items(), key=lambda x:x[1])
 		end = len(parties_sorted) - 1
 		count = 0
 		parties_list = []
 		while count < 10:
 			parties_list.append(parties_sorted[end])
 			end -= 1
 			count += 1

 		print parties_list
 		final_parties_dictionary = {}

 		for tweet in tweets:
 			text = tweet['text']
 			if "party" not in text: continue 

 			at_tags = find_at_name(text)
 			# print at_tags
 			for party in parties_list:
 				party_word = party[0]
 				if party_word in text:
 					print party_word
		 			for at_tag in at_tags:
		 				print at_tag
		 				final_parties_dictionary = insert_name_to_dictionary(party,at_tag,final_parties_dictionary)
 			
 		print final_parties_dictionary

if __name__ == "__main__":
	main()