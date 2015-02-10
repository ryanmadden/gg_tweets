import run

def create_meta_each(method, method_description):
	category = {}
	category["method"] = method
	category["method_description"] = method
	return category

def create_meta_data(year):
	metadata = {}
	metadata["year"] = year
	metadata["hosts"] = create_meta_each("test", "test1")
	metadata["nominees"] = create_meta_each("test", "test1")
	metadata["awards"] = create_meta_each("test", "test1")
	metadata["presenters"] = create_meta_each("test", "test1")
	return metadata

# TODO: add presenters and nominees
def create_unstructured(hosts, awards, nominees):
	unstructured = {}
	winners = []
	awards = [] 
	for each in hosts:
		unstructured["hosts"] = each["hosts"]
	for each in awards:
		winner.append(each["winner"])
		awards.append(each["award"])
	unstructured["winners"] = winners
	unstructured["awards"] = awards
	unstructured["nominees"] = nominees
	return unstructured

# TODO: add presenters and nominees
def create_structured_each(each):
	award = {}
	award["winner"] = each["winner"]
	award["nominees"] = each["nominees"]
	award["presenters"] = []
	return award

def create_structured(awards):
	structured = {}
	for each in awards:
		structured[each["award"]] = create_structured_each(each)
	return structured


def create_data():
	hosts, awards, nominees = run.main()
	print hosts
	print awards
	data = {}
	data["unstructured"] = create_unstructured(hosts, awards, nominees)
	data["structured"] = create_structured(awards)
	return data

def main(year):
	autograder = {}
	autograder["metadata"] = create_meta_data(year)
	autograder["data"] = create_data()
	return autograder

if __name__ == "__main__":
	main()