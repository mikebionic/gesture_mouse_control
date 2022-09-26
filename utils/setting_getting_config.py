# Write data to file
import json

config = {"key1": "value1", "key2": "value2"}

with open('config1.json', 'w') as f:
    json.dump(config, f)


# Read data from a file:

import json

with open('config.json', 'r') as f:
    config = json.load(f)

#edit the data
config['key3'] = 'value3'

#write it back to the file
with open('config.json', 'w') as f:
    json.dump(config, f)
