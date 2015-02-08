import json

data = []
with open('gg2013.json') as f:
    for line in f:
#         data.append(json.loads(line))
#         print line
#         break

	# loaded = json.loads('[{"text":"hello"}, {"text":"goodbye"}, {"text":"strawberry fields forever"}]')
		loaded = json.loads(line)
		for d in loaded:
			for key, value in d.iteritems():
				if key == 'text':
					print value

