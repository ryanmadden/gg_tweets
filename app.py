from flask import Flask, render_template, Response, request
import json
import run

app = Flask(__name__)


@app.route("/", methods=['GET'])
def react():
	run.main()
	return render_template('react.html')

@app.route('/thedata.json', methods=['GET', 'POST'])
def json_handler():
    with open('data.json', 'r') as file:
        comments = json.loads(file.read())

    if request.method == 'POST':
        comments.append(request.form.to_dict())

        with open('data.json', 'w') as file:
            file.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(json.dumps(comments), mimetype='application/json')



if __name__ == "__main__":
	app.run(debug=True)