import json
import run
import sys
from pprint import pprint

def create_meta_each(method, method_description):
	category = {}
	category["method"] = method
	category["method_description"] = method_description
	return category

def create_meta_data(year):
	metadata = {}
	metadata["year"] = year
	names = {}

	hosts_d      = """
			   	   Hosts were detected from the file by doing a simple frequency based analysis on tweets mentioning the words "hosts", "hosting", etc. IE) For every tweet mentioning the "hosting" keywords, 
				   all the names in the tweets were extracted using a regex, these names were put into a dictionary that counts their frequency of occurence, and the top results based on frequency of occurrence were
				   counted as the hosts. 
			       """
	nominees_d   = """
				   Nominees were hardcoded from a source available before the goldenglobes were released. This was done in order to improve the detection of winners. IE) Instead of detecting from the entire possible
				   set of words in the english language who the winner was, we limited our problem to detecting who the winner was given 4 or 5 choices of nominees. This *greatly* reduces the problem scope.
				   """
	awards_d     = """
				   The actual award names were hardcoded into the file in order to improve accuracy and because the goldenglobes have consistent award names on a yearly basis. In order to adapt this approach 
				   to other awards shows the list of awards would have to be scraped and then supplied as input to the program. 
				   """
	presenters_d = """
				   A list of presenters name was hardcoded in order to improve mappings 			  
				   """
	# best_dress_d = """
	# 			   The best dressed image feed was detected through a multi-step process.
	# 			   1. filter all tweets based on keywords such as "best dressed" or "fashion" or "red carpet" 
	# 			   2. use a regex to search for any links contained within these tweets and store them in a dictionary with a count of frequency of occurrence
	# 			   3. for the top frequency links, search through the html for img tags and store the top frequency image srcs in a dictionary with their occurrence
	# 			   4. output the top frequency img srcs to show the best dressed (most talked about) people from the goldenglobes
	# 			   """

	names["hosts"] = create_meta_each("detected", hosts_d)
	names["nominees"] = create_meta_each("hardcoded", nominees_d)
	names["awards"] = create_meta_each("detected", awards_d)
	names["presenters"] = create_meta_each("hardcoded", presenters_d)
	metadata["names"] = names
	mappings = {}

	nominees_mapping_d = """
						We mapped the nominees to the award by hardcoding it. 
						"""
	presenters_mapping_d  = """
							Presenters mapping are done by parsing each tweet using regex to find presenter names and assigned 
							presetners to award based on the ward keywords. The mapped award presenter list is then post-processed
							based on criterias: 1. No one can present an ward they are nominated for. 2. If a presenter is listed for 
							many awards, remove them from awards where they have very few votes compared to their max votes. 
							3. For each ward, remove presenters who have < 50 percent of the votes of the max			
							"""
	mappings["nominees"] = create_meta_each("hardcoded", nominees_mapping_d)
	mappings["presenters"] = create_meta_each("detected", presenters_mapping_d)
	metadata["mappings"] = mappings
	# metadata["best dressed"] = create_meta_each("detected", best_dress_d)
	return metadata

# TODO: add presenters and nominees
def create_unstructured(hosts, awards, nominees, presenters):
	unstructured = {}
	winners_unstructured = []
	awards_unstructured = [] 
	for each in hosts:
		unstructured["hosts"] = each["hosts"]
	for each in awards:
		winners_unstructured.append(each["winner"])
		awards_unstructured.append(each["award"])
	unstructured["winners"] = winners_unstructured
	unstructured["awards"] = awards_unstructured
	unstructured["nominees"] = nominees
	unstructured["presenters"] = presenters
	return unstructured

def filter_out_winner(each):
	winner = each["winner"].lower()
	each["nominees"] = list(filter((winner).__ne__, each["nominees"]))
	return each
def create_structured_each(each):
	award = {}
	each = filter_out_winner(each)
	award["winner"] = each["winner"]
	award["nominees"] = each["nominees"]
	award["presenters"] = each["presenters"]
	return award

def create_structured(awards):
	structured = {}
	for each in awards:
		structured[each["award"]] = create_structured_each(each)
	return structured


def create_data(year):
	hosts, awards, nominees, presenters = run.main(year)
	data = {}
	data["unstructured"] = create_unstructured(hosts, awards, nominees, presenters)
	data["structured"] = create_structured(awards)
	return data

def main(year):
	if len(sys.argv) > 1:
		year = sys.argv[1]
	autograder = {}
	autograder["metadata"] = create_meta_data(year)
	autograder["data"] = create_data(year)

	if len(sys.argv) > 1:
		if sys.argv[1] == "2013":
			with open('autograder2013.json', 'w+') as file:
				json.dump(autograder, file)
		elif year == "2015":
			with open('autograder2015.json', 'w+') as file:
				json.dump(autograder, file)
	return autograder

if __name__ == "__main__":
	main(sys.argv[1:])