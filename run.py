import json
import operator
import re
import sys
from nltk import word_tokenize
from timer import timeit
from pprint import pprint


class Award(object):

	def __init__(self, t, f, n):
		self.title      = t
		self.filters    = f
		self.nominees   = {nominee: 0 for nominee in n}
		self.presenters = {}

	def get_title(self):
		return self.title

	def get_filters(self):
		return self.filters

	def get_nominees(self):
		return self.nominees.keys()

	def get_presenters(self):
		return self.presenters.keys()

	def set_title(self, t):
		self.title = t

	def set_filters(self, f):
		self.filters = f

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
		print "-- Award: " + self.title
		print "     Presented by: " + str(sorted(self.presenters.iteritems(), key=operator.itemgetter(1), reverse=True))
		print "     Winner: " + winner.keys()[0].title()

	def show_api(self):
		winner =  dict(sorted(self.nominees.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
		return {"award" : self.title, "winner" : winner.keys()[0].title(), "nominees" : self.nominees.keys()}



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



# def nominees_api_dict(award_titles, nominees):
# 	nom_dict = {}
# 	for a,n in zip(award_titles, nominees):
# 		if a in nom_dict:
# 			nom_dict[a].append(n)
# 		else:
# 			nom_dict[a] = [n]
# 	return nom_dict



@timeit
def main():
	f_2015_mini = './gg15mini.json'
	f_2015      = './goldenglobes2015.json'
	f_2013      = './gg2013.json'

	# Tweet Parsing Filters
	host_filters      = ["host", "hosting", "hosts", "hosted"]
	presenter_filters = ["presented", "presenting", "presenter"]
	award_filters     = [[["best"], ["picture"],    ["drama"]],
						 [["best"], ["picture"],    ["musical", "comedy"]],
						 [["best"], ["actor"],      ["drama"]],
						 [["best"], ["actress"],    ["drama"]],
						 [["best"], ["actor"],      ["musical", "comedy"]],
						 [["best"], ["actress"],    ["musical", "comedy"]],
						 [["best"], ["supporting"], ["actor"]],
						 [["best"], ["supporting"], ["actress"]],
						 [["best"], ["director"]],
						 [["best"], ["screenplay"]],
						 [["best"], ["score"]],
						 [["best"], ["song"]],
						 [["best"], ["animated"]],
						 [["best"], ["foreign"]]]

	# Hardcoded Info
	nominees          = [["boyhood", "foxcatcher", "the imitation game", "selma", "the theory of everything"],
						 ["the grand budapest hotel", "birdman", "into the woods", "pride", "st. vincent"],
						 ["eddie redmayne", "steve carell", "benedict cumberbatch", "jake gyllenhaal", "david oyelowo"],
						 ["julianne moore", "jennifer aniston", "felicity jones", "rosamund pike", "reese witherspoon"],
						 ["michael keaton", "ralph fiennes", "bill murray", "joaquin phoenix", "christoph waltz"],
						 ["amy adams", "emily blunt", "helen mirren", "julianne moore", "quvenzhane wallis"],
						 ["j. k. simmons", "robert duvall", "edward norton", "mark ruffalo"],                                          #ethan hawke
						 ["patricia arquette", "jessica chastain", "keira knightley", "emma stone", "meryl streep"],
						 ["richard linklater", "wes anderson", "ava duvernay", "david fincher", "alejandro inarritu gonzalez"],
						 ["birdman", "the grand budapest hotel", "gone girl", "the imitation game", "boyhood"],
						 ["the imitation game", "birdman", "gone girl", "interstellar", "the theory of everything"],
						 ["noah", "annie", "the hunger games: mockingjay - part 1", "selma" "big eyes"],
						 ["how to train your dragon 2", "big hero 6", "the book of life", "the boxtrolls", "the lego movie"],
						 ["leviathan", "force majeure", "gett: the trial of viviane amsalem", "ida", "tangerines"],
						 ["downton abbey (masterpiece)", "game of thrones", "the good wife", "house of cards", "the affair"]
						 ["claire danes", "viola davis", "julianna margulies", "robin wright"],
						 ["clive owen", "liev schreiber", "james spader", "dominic west", "kevin spacey"],
						 ["girls", "jane the virgin", "orange is the new black", "silicon valley", "transparent"],
						 ["lena dunham", "edie falco", "julia louis-dreyfus", "taylor schilling", "gina rodriguez"],
						 ["louis c.k.", "don cheadle", "ricky gervais", "william h. macy", "jeffrey tambor"],
						 ["the missing", "the normal heart", "olive kitteridge", "true detective", "fargo"],
						 ["jessica lange", "frances mcdormand", "frances o'connor", "allison tolman", "maggie gyllenhaal"],
						 ["martin freeman", "woody harrelson", "matthew mcconaughey", "mark ruffalo", "billy bob thornton"],
						 ["uzo aduba", "kathy bates", "allison janney", "michelle monaghan", "joanne froggatt"],
						 ["alan cumming", "colin hanks", "bill murray", "jon voight", "matt bomer"],
						 ["george clooney"]
	award_titles      = ["Best Motion Picture - Drama",
						 "Best Motion Picture - Musical/Comedy",
						 "Best Actor in a Motion Picture - Drama",
						 "Best Actress in a Motion Picture - Drama",
						 "Best Actor in a Motion Picture - Musical/Comedy",
						 "Best Actress in a Motion Picture - Musical/Comedy",
						 "Best Supporting Actor in a Motion Picture - Drama/Musical/Comedy",
						 "Best Supporting Actress in a Motion Picture - Drama/Musical/Comedy",
						 "Best Director",
						 "Best Screenplay",
						 "Best Original Score",
						 "Best Original Song",
						 "Best Animated Feature Film",
						 "Best Foreign Language Film",
						# "Best Television Series - Drama",
						# "Best Performance by an Actress in a Television Series - Drama",
						#"Best Performance by an Actor in a Television Series - Drama",
						#"Best Television Series - Comedy/Musical",
						# "Best Performance by an Actress in a Television Series - Comedy/Musical",
						 #"Best Performance by an Actor in a Television Series - Comedy/Musical",
						 #"Best Mini-Series or Motion Picture Made for Television",
						 #"Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television",
						 #"Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television",
						 #"Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television",
						 #"Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television",
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
	awards = [Award(award_titles[x], award_filters[x], nominees[x]) for x in range(14)]
	print "Awards created..."

	# Read and parse through tweets
	potential_hosts      = {}
	count = 0
	curr_percent = -5
 	with open(f_2015_mini, 'r') as f:
 		tweets = map(json.loads, f)[0]
		print "Tweet collection created..."
		num_tweets = len(tweets)

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
<<<<<<< HEAD
				# determine if tweet pertains to an award
=======
>>>>>>> hardcode-presenters
				contains_award = True
				for req in award.get_filters():
					if not any(opt in text.lower() for opt in req):
						contains_award = False
<<<<<<< HEAD
				# if it does,
				if contains_award:
					# check if a nominee shows up in the tweet
					for nom in award.get_nominees():
						# if one does,
						if nom in text.lower():
							# increment that nominee's weight
							award.increment_nominee(nom)
					# check if presenter shows up in the tweet
					for filt in presenter_filters:
						# if one does,
						if filt in text:
							# increment that presenter's weight
							if not presenter_names:
								presenter_names = find_presenter_names(text)
							for pn in presenter_names:
								if pn.lower() in award.get_presenters():
									award.increment_presenter(pn.lower())
								else:
									award.add_presenter(pn.lower())
=======
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
>>>>>>> hardcode-presenters

			# Display progress in terminal
			if not count % 100:
				percent = (float(count)/num_tweets) * 100
				if percent > curr_percent:
					curr_percent += 5
					sys.stdout.write("\r{0}".format(str(curr_percent) + "% complete"))
					sys.stdout.flush()
			count+=1

	# Determine and display results in terminal

	# ensure presenters only appear on their top award
	for name in presenter_list:
		for award in awards:
			if name in award.nominees:
				award.presenters.pop(name)
		# curr_max = 0
		# max_award = awards[0]
		# for award in awards:
		# 	curr_presenters = award.presenters
		# 	if name in curr_presenters.keys():
		# 		if curr_presenters[name] > curr_max:
		# 			max_award = award
		# 			curr_max = curr_presenters[name]
		# for award in awards:
		# 	if award is not max_award:
		# 		if name in award.presenters:
		# 			award.presenters.pop(name)

	determine_results(awards, potential_hosts)
	
	# Determine and display results in frontend
	final_awards = awards_api(awards)
	final_hosts  = hosts_api(potential_hosts)
	final_nominees = nominees_api(nominees)
	return (final_hosts, final_awards, final_nominees)




if __name__ == "__main__":
	main()