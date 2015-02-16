import run
import sys
from pprint import pprint

def create_meta_each(method, method_description):
	category = {}
	category["method"] = method
	category["method_description"] = method
	return category

def create_meta_data(year):
	metadata = {}
	metadata["year"] = year
	metadata["hosts"] = create_meta_each("detected", "test1")
	metadata["nominees"] = create_meta_each("hardcoded", "test1")
	metadata["awards"] = create_meta_each("detected", "test1")
	metadata["presenters"] = create_meta_each("detected", "test1")
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

# TODO: add presenters and nominees
def create_structured_each(each):
	award = {}
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
	print hosts
	print awards
	data = {}
	data["unstructured"] = create_unstructured(hosts, awards, nominees, presenters)
	data["structured"] = create_structured(awards)
	return data

def main(year):
	if len(sys.argv) > 1:
		year = sys.argv[1]
		print year	
	autograder = {}
	autograder["metadata"] = create_meta_data(year)
	autograder["data"] = create_data(year)
	pprint(autograder)
	return autograder

if __name__ == "__main__":
	main(sys.argv[1:])