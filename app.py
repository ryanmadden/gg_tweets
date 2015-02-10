from flask import Flask, render_template, Response, request
import json
import run
import createAutograder

app = Flask(__name__)


@app.route("/", methods=['GET'])
def react():
	return render_template('react.html')

@app.route('/thedata.json', methods=['GET', 'POST'])
def json_handler():
    with open('data.json', 'r') as file:
        comments = json.loads(file.read())
    return Response(json.dumps(comments), mimetype='application/json')

# create autograder based on the year
@app.route('/submit/<year>', methods=['POST'])
def submit(year):
	autograder_json = createAutograder.main(year)

	with open('autograder.json', 'w') as file:
		file.truncate()
		file.write(json.dumps(autograder_json, indent=4, separators=(',', ': ')))
	return ""

# create host json in data.json 
@app.route('/host', methods=['POST'])
def get_host():
	with open('autograder.json', 'r') as file:
		data = json.loads(file.read())
		hosts = data['data']['unstructured']['hosts']
		hosts_json = [{"hosts": hosts}]
	with open('data.json', 'w') as file:
		file.write(json.dumps(hosts_json, indent=4, separators=(',', ': ')))
	return ""

# create award json in data.json 
@app.route('/awards/<award>', methods=['Post'])
def get_awards(award):
	award = award.replace('_','/')
	#award_json_formated =[]
	with open('autograder.json', 'r') as file:
		data = json.loads(file.read())
		structured = data['data']['structured']
		award_json_formated = []
		if award == 'all':
			for key in structured:
				award_json_formated.append(createJsonFormat(structured,key))
		else:
			award_json_formated = [createJsonFormat(structured,award)]
	with open('data.json', 'w') as file: 
		file.write(json.dumps(award_json_formated, indent=4, separators=(',', ': ')))
	return ""

def createJsonFormat(structured, key):
	award_json = structured[key]
	award_json_formated = {}
	award_json_formated["award"] = key
	award_json_formated["winner"] = award_json["winner"]
	award_json_formated["nominees"] = award_json["nominees"]
	award_json_formated["presenters"] = award_json["presenters"]
	return award_json_formated	

if __name__ == "__main__":
	app.run(debug=True)