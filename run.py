import json
import operator
import re
from nltk import word_tokenize
from timer import timeit



class Award(object):

	def __init__(self, t, f, n):
		self.title      = t
		self.filters    = f
		self.nominees   = {nominee: 0 for nominee in n}
		self.presenters = {}

	def get_filters(self):
		return self.filters

	def get_nominees(self):
		return self.nominees.keys()

	def get_presenters(self):
		return self.presenters.keys()

	def add_presenter(self, p):
		self.presenters[p] = 1

	def increment_nominee(self, n):
		self.nominees[n] += 1

	def increment_presenter(self, p):
		self.presenters[p] += 1

	def show(self):
		print "Award: " + self.title
		winner =  dict(sorted(self.nominees.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
		print winner.keys()[0].title()



def find_names(tweet):
	return re.findall("([A-Z][-'a-zA-Z]+\s[A-Z][-'a-zA-Z]+)", tweet)



def determine_results(awards, hosts):
	hosts = dict(sorted(hosts.iteritems(), key=operator.itemgetter(1), reverse=True)[:2])
	print hosts
	print ""
	for award in awards:
		award.show()


@timeit
def main():
	f_2015_mini = './gg15mini.json'
	f_2015      = './goldenglobes2015.json'
	f_2013      = './gg2013.json'

	host_filters      = ["host", "hosting", "hosts", "hosted"]
	presenter_filters = ["presented", "presenting", "presenter", "presenters"]
	award_filters     = [["best motion picture", "drama"],
						 ["best motion picture", "musical", "comedy"],
						 ["best actor in a motion picture", "drama"],
						 ["best actress in a motion picture", "drama"],
						 ["best actor in a motion picture", "comedy", "musical"],
						 ["best actress in a motion picture", "comedy", "musical"],
					     ["best supporting actor in a motion picture", "drama", "musical", "comedy"],
					     ["best supporting actress in a motion picture", "drama", "musical", "comedy"],
					     ["best director"],
					     ["best screenplay"],
					     ["best original score", "best score"],
					     ["best original song", "best song"],
					     ["best animated"],
					     ["foreign", "language"]]
	nominees          = [["boyhood", "foxcatcher", "the imitation game", "selma", "the theory of everything"],
						 ["the grand budapest hotel", "birdman", "into the woods", "pride", "st. vincent"],
						 ["eddie redmayne", "steve carell", "benedict cumberbatch", "jake gyllenhaal", "david oyelowo"],
						 ["julianne moore", "jennifer aniston", "felicity jones", "rosamund pike", "reese witherspoon"],
						 ["michael keaton", "ralph fiennes", "bill murray", "joaquin phoenix", "christoph waltz"],
						 ["amy adams", "emily blunt", "helen mirren", "julianne moore", "quvenzhane wallis"],
						 ["j. k. simmons", "robert duvall", "ethan hawke", "edward norton", "mark ruffalo"],
						 ["patricia arquette", "jessica chastain", "keira knightley", "emma stone", "meryl streep"],
						 ["richard linklater", "wes anderson", "ava duvernay", "david fincher", "alejandro gonzalez inarritu"],
						 ["birdman", "wes anderson", "gillian flynn", "richard linklater", "graham moore"],
						 ["johann johannsson", "alexandre desplat", "trent reznor and atticus ross", "antonio sanchez", "hanz zimmer"],
						 ["glory", "big eyes", "mercy is", "opportunity", "yellow flicker beat"],
						 ["how to train your dragon 2", "big hero 6", "the book of life", "the boxtrolls", "the lego movie"],
						 ["leviathan", "force majeure", "gett: the trial of viviane amsalem", "ida", "tangerines"]]
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
						 "Best Foreign Language Film"]
	awards = [Award(award_titles[x], award_filters[x], nominees[x]) for x in range(14)]
	print "Awards created..."


	potential_hosts      = {}
	potential_presenters = {}
	potential_nominees   = {}

	with open(f_2015_mini, 'r') as f:
		tweets = map(json.loads, f)[0]

		for tweet in tweets:
			text  = tweet['text']
			names = ""

			# Filter for hosts
			for filt in host_filters:
				if filt in text:
					names = find_names(text)
					for name in names:
						if name in potential_hosts:
							potential_hosts[name] += 1
						else: 
							potential_hosts[name] = 1

			# filter for nominees and presenters
			for award in awards:
				for filt in award.get_filters():
					if filt in text:
						for t in award.get_nominees():
							if t in text.lower():
								award.increment_nominee(t)
					for filt in presenter_filters:
						if filt in text:
							if not names:
								names = find_names(text)
							for n in names:
								if n.lower() in award.get_presenters():
									award.increment_presenter(n.lower())
								else:
									award.add_presenter(n.lower())

	determine_results(awards, potential_hosts)





if __name__ == "__main__":
	main()