import json
import operator
import re
import sys
from nltk import word_tokenize
from timer import timeit
from pprint import pprint


class Award(object):

	def __init__(self, t, f, s, n):
		self.title      = t
		self.filters    = f
		self.stoplist   = s
		self.nominees   = {nominee: 0 for nominee in n}
		self.presenters = {}

	def get_title(self):
		return self.title

	def get_filters(self):
		return self.filters

	def get_stoplist(self):
		return self.stoplist

	def get_nominees(self):
		return self.nominees.keys()

	def get_presenters(self):
		return self.presenters.keys()

	def set_title(self, t):
		self.title = t

	def set_filters(self, f):
		self.filters = f

	def set_stoplist(self, s):
		self.stoplist = s

	def set_nominees(self, n):
		self.nominees = {nominee: 0 for nominee in n}

	def add_presenter(self, p):
		self.presenters[p] = 1

	def increment_nominee(self, n):
		self.nominees[n] += 1

	def increment_presenter(self, p):
		self.presenters[p] += 1

	def remove_presenter(self, p):
		if p in self.presenters:
			self.presenters.pop(p, None)

	def show(self):
		winner     = dict(sorted(self.nominees.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
		presenters = dict(sorted(self.presenters.iteritems(), key=operator.itemgetter(1), reverse=True)[:3])
		print "\n-- Award: " + self.title
		# print "     Presented by: " + str(sorted(self.presenters.iteritems(), key=operator.itemgetter(1), reverse=True))
		presenter_string = "     Presented by: "
		# for presenter in presenters.keys():
		# TODO Uncomment this for pretty printing
		# 	presenter_string += presenter.title() + " & "
		print presenters
		print presenter_string
		print "     Winner: " + winner.keys()[0].title()

	def show_api(self):
		winner =  dict(sorted(self.nominees.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
		return {"award" : self.title, "winner" : winner.keys()[0].title(), "nominees" : self.nominees.keys(), "presenters" : self.presenters.keys()}



def find_names(tweet):
	return re.findall("([A-Z][-'a-zA-Z]+\s[A-Z][-'a-zA-Z]+)", tweet)



def find_presenter_names(tweet):
	tweet = tweet.replace("golden", "")
	tweet = tweet.replace("globe", "")
	tweet = tweet.replace("globes", "")
	tweet = tweet.replace("Golden", "")
	tweet = tweet.replace("Globe", "")
	tweet = tweet.replace("Globes", "")
	return re.findall("([A-Z][-'a-zA-Z]+\s[A-Z][-'a-zA-Z]+)", tweet)



def determine_results(awards, hosts):
	hosts = dict(sorted(hosts.iteritems(), key=operator.itemgetter(1), reverse=True)[:2])
	print "\n\nOutcome of the 2015 Golden Globes"
	print "  Hosted by: " + str(hosts.keys()[0]).title() + " & " + str(hosts.keys()[1]).title() + "\n"
	for award in awards:
		award.show()



def hosts_api(hosts):
	hosts = dict(sorted(hosts.iteritems(), key=operator.itemgetter(1), reverse=True)[:2])
	return [{'hosts': hosts.keys()}]



def awards_api(awards):
	return [award.show_api() for award in awards]



def nominees_api(nominees):
	nominee_compiled = []
	for mov in nominees:
		nominee_compiled.extend(mov)
	return nominee_compiled


@timeit
def main():
	f_2015_mini = './gg15mini.json'
	f_2015      = './goldenglobes2015.json'
	f_2013      = './gg2013.json'

	# Tweet Parsing Filters
	host_filters      = ["host", "hosting", "hosts", "hosted"]
	presenter_filters = ["presented", "presenting", "presenter"]
	award_filters     = [[["best"],             ["picture"],          ["drama"]],
						 [["best"],             ["picture"],          ["musical", "comedy"]],
						 [["best"],             ["actor"],            ["drama"]],
						 [["best"],             ["actress"],          ["drama"]],
						 [["best"],             ["actor"],            ["musical", "comedy"]],
						 [["best"],             ["actress"],          ["musical", "comedy"]],
						 [["best"],             ["supporting"],       ["actor"]],
						 [["best"],             ["supporting"],       ["actress"]],
						 [["best"],             ["director"]],
						 [["best"],             ["screenplay"]],
						 [["best"],             ["score"]],
						 [["best"],             ["song"]],
						 [["best"],             ["animated"]],
						 [["best"],             ["foreign"]],
						 [["best"],             ["television", "tv"], ["drama"]],
						 [["best"],             ["actress"],          ["television", "tv"],   ["drama"]],
						 [["best"],             ["actor"],            ["television", "tv"],   ["drama"]],
						 [["best"],             ["television", "tv"], ["comedy", "musical"]],
						 [["best"],             ["actress"],          ["television", "tv"],   ["comedy", "musical"]],
						 [["best"],             ["actor"],            ["television", "tv"],   ["comedy", "musical"]],
						 [["best"],             ["series"],           ["television", "tv"]],
						 [["best"],             ["actress"],          ["series"],             ["television", "tv"]],
						 [["best"],             ["actor"],            ["series"],             ["television", "tv"]],
						 [["best"],             ["actress"],          ["supporting"],         ["series"],             ["television", "tv"]],
						 [["best"],             ["actor"],            ["supporting"],         ["series"],             ["television", "tv"]],
						 [["cecil", "demille"]]]
	award_stoplists =   [["television", "tv"],
						 ["television", "tv"],
						 ["television", "tv"],
						 ["television", "tv"],
						 ["television", "tv"],
						 ["television", "tv"],
						 ["television", "tv"],
						 ["television", "tv"],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 [],
						 []]

	# Hardcoded Info
	nominees          = [["boyhood", "foxcatcher", "the imitation game", "selma", "the theory of everything"],
						 ["the grand budapest hotel", "birdman", "into the woods", "pride", "st. vincent"],
						 ["eddie redmayne", "steve carell", "benedict cumberbatch", "jake gyllenhaal", "david oyelowo"],
						 ["julianne moore", "jennifer aniston", "felicity jones", "rosamund pike", "reese witherspoon"],
						 ["michael keaton", "ralph fiennes", "bill murray", "joaquin phoenix", "christoph waltz"],
						 ["amy adams", "emily blunt", "helen mirren", "julianne moore", "quvenzhane wallis"],
						 ["j. k. simmons", "robert duvall", "edward norton", "mark ruffalo"],
						 ["patricia arquette", "jessica chastain", "keira knightley", "emma stone", "meryl streep"],
						 ["richard linklater", "wes anderson", "ava duvernay", "david fincher", "alejandro inarritu gonzalez"],
						 ["birdman", "the grand budapest hotel", "gone girl", "the imitation game", "boyhood"],
						 ["the imitation game", "birdman", "gone girl", "interstellar", "the theory of everything"],
						 ["noah", "annie", "the hunger games: mockingjay - part 1", "selma" "big eyes"],
						 ["how to train your dragon 2", "big hero 6", "the book of life", "the boxtrolls", "the lego movie"],
						 ["leviathan", "force majeure", "gett: the trial of viviane amsalem", "ida", "tangerines"],
						 ["downton abbey (masterpiece)", "game of thrones", "the good wife", "house of cards", "the affair"],
						 ["claire danes", "viola davis", "julianna margulies", "robin wright", "ruth wilson"],
						 ["clive owen", "liev schreiber", "james spader", "dominic west", "kevin spacey"],
						 ["girls", "jane the virgin", "orange is the new black", "silicon valley", "transparent"],
						 ["lena dunham", "edie falco", "julia louis-dreyfus", "taylor schilling", "gina rodriguez"],
						 ["louis c.k.", "don cheadle", "ricky gervais", "william h. macy", "jeffrey tambor"],
						 ["the missing", "the normal heart", "olive kitteridge", "true detective", "fargo"],
						 ["jessica lange", "frances mcdormand", "frances o'connor", "allison tolman", "maggie gyllenhaal"],
						 ["martin freeman", "woody harrelson", "matthew mcconaughey", "mark ruffalo", "billy bob thornton"],
						 ["uzo aduba", "kathy bates", "allison janney", "michelle monaghan", "joanne froggatt"],
						 ["alan cumming", "colin hanks", "bill murray", "jon voight", "matt bomer"],
						 ["george clooney"]]	
	award_titles 	  = ["Best Motion Picture - Drama",
				         "Best Motion Picture - Comedy Or Musical",
						 "Best Performance by an Actor in a Motion Picture - Drama",
						 "Best Performance by an Actress in a Motion Picture - Drama",
						 "Best Performance by an Actor in a Motion Picture - Comedy Or Musical",
						 "Best Performance by an Actress in a Motion Picture - Comedy Or Musical",
						 "Best Performance by an Actor In A Supporting Role in a Motion Picture",
						 "Best Performance by an Actress In A Supporting Role in a Motion Picture",
						 "Best Director - Motion Picture",
						 "Best Screenplay - Motion Picture",
						 "Best Original Score - Motion Picture",
						 "Best Original Song - Motion Picture",
						 "Best Animated Feature Film",
						 "Best Foreign Language Film",
						 "Best Television Series - Drama",
						 "Best Performance by an Actress in a Television Series - Drama",
						 "Best Performance by an Actor in a Television Series - Drama",
						 "Best Television Series - Comedy Or Musical",
						 "Best Performance by an Actress In A Television Series - Comedy Or Musical",
						 "Best Performance by an Actor In A Television Series - Comedy Or Musical",
						 "Best Mini-Series or Motion Picture Made for Television",
						 "Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television",
						 "Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television",
						 "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television",
						 "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television",
						 "Cecil B. DeMille Award"]
	presenter_list	  = ["vince vaughn",
						 "kate beckinsale", 
						 "harrison ford",
						 "chris pratt", 
						 "lupita nyong'o",
						 "colin farrell",
						 "gwyneth paltrow",
						 "katherine heigl", 
						 "don cheadle", 
						 "jane fonda", 
						 "jennifer aniston", 
						 "kristen wiig", 
						 "adrien brody", 
						 "david duchovny", 
						 "prince", 
						 "adam levine", 
						 "kevin hart", 
						 "jeremy renner", 
						 "bryan cranston", 
						 "matthew mcconaughey", 
						 "sienna miller", 
						 "benedict cumberbatch", 
						 "katie holmes", 
						 "salma hayek", 
						 "meryl streep", 
						 "jennifer lopez", 
						 "anna faris", 
						 "lily tomlin", 
						 "amy adams", 
						 "jamie dornan", 
						 "jared leto", 
						 "kerry washington", 
						 "ricky gervais", 
						 "robert downey, jr.", 
						 "bill hader", 
						 "paul rudd", 
						 "dakota johnson", 
						 "seth meyers", 
						 "julianna margulies"]

	# Create Award object for each award
	print "Creating awards..."
	awards = [Award(award_titles[x], award_filters[x], award_stoplists[x], nominees[x]) for x in range(len(award_titles))]

	# Read and parse through tweets
	potential_hosts      = {}
	count = 0
	curr_percent = -5
 	with open(f_2015_mini, 'r') as f:


 		print "Creating tweet collection..."
 		tweets = map(json.loads, f)[0]
		num_tweets = len(tweets)

		print "Reading tweets..."
		for tweet in tweets:
			text  = tweet['text']
			names = ""
			presenter_names = ""

			# Find hosts (working)
			for filt in host_filters:
				if filt in text:
					names = find_names(text)
					for name in names:
						if name in potential_hosts:
							potential_hosts[name] += 1
						else: 
							potential_hosts[name] = 1

			# Find nominees (working) and presenters (not working)
			# for each award
			for award in awards:
				contains_award = True
				# TODO put stop word analysis first to short circuit analysis of bad tweets, improves speed
				for req in award.get_filters():
					if not any(opt in text.lower() for opt in req):
						contains_award = False
				if any(stop in text.lower() for stop in award.get_stoplist()):
					contains_award = False
				if contains_award:
					for nom in award.get_nominees():
						# for each nominee that shows up in the tweet, increment its likelihood
						if nom in text.lower():
							award.increment_nominee(nom)
					for pn in presenter_list:
						if pn in text.lower():
							if pn.lower() in award.get_presenters():
								award.increment_presenter(pn.lower())
							else:
								award.add_presenter(pn.lower())

			# Display progress in terminal
			if not count % 100:
				percent = (float(count)/num_tweets) * 100
				if percent > curr_percent:
					curr_percent += 5
					sys.stdout.write("\r{0}".format(str(curr_percent) + "% complete"))
					sys.stdout.flush()
			count+=1


	# POST-FILTERING
	# Nominees for an award cannot present the award
	for presenter in presenter_list:
		for award in awards:
			if presenter in award.get_nominees():
				award.presenters.pop(presenter)

	# Grant presenters to highly-weighted awards
	for presenter in presenter_list:
		local_max = 0
		local_max_award = None
		for award in awards:
			if presenter in award.get_presenters():
				if award.presenters[presenter] > local_max:
					local_max = award.presenters[presenter]
					local_max_award = award
		for award in awards:
			if presenter in award.get_presenters():
				if local_max - award.presenters[presenter] > 15:
					award.presenters.pop(presenter)

	#Eliminate presenters who have <50% of the votes of the max presenter
	for award in awards:
		local_presenters = award.presenters
		max_votes = max(local_presenters.values())
		for presenter in award.get_presenters():
			if award.presenters[presenter] < (max_votes/2):
				award.presenters.pop(presenter)

	# If an award still has >2 presenters, eliminate presenters who are listed in an award with 2 or 1 presenters
	# TODO fix this so it works a little better
	# for award in awards:
	# 	if len(award.get_presenters()) > 2:
	# 			for presenter in award.get_presenters():
	# 				for award_inner in awards:
	# 					if presenter in award_inner.get_presenters() and award_inner.presenters[presenter] == max(award_inner.presenters.values()):
	# 						award.presenters.pop(presenter)
	# 						break



	# Determine and display results in terminal
	determine_results(awards, potential_hosts)
	
	# Determine and display results in frontend
	final_awards = awards_api(awards)
	final_hosts  = hosts_api(potential_hosts)
	final_nominees = nominees_api(nominees)
	return (final_hosts, final_awards, final_nominees)




if __name__ == "__main__":
	main()