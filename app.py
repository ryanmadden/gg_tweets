from flask import Flask, render_template, Response, request
import json
import run

app = Flask(__name__)


@app.route("/", methods=['GET'])
def react():
	return render_template('react.html')

@app.route('/thedata.json', methods=['GET', 'POST'])
def json_handler():
    with open('data.json', 'r') as file:
        comments = json.loads(file.read())

    return Response(json.dumps(comments), mimetype='application/json')

@app.route('/submit', methods=['POST'])
def submit():
	hosts, awards = run.main()
	hosts.extend(awards)
	with open('data.json', 'w') as file:
		file.write(json.dumps(hosts, indent=4, separators=(',', ': ')))
	return

if __name__ == "__main__":
	app.run(debug=True)