''' convert a file to a json file '''

from operator import ne
import converter
import sys

try:
    filename = sys.argv[1]
except IndexError:
    print('No input file given.')
    input('[EXIT]')

with open(filename, 'r') as f:
    content = f.read()

try:
    new_filename = filename.split('.meta')[0] + '.json'
except IndexError:
    print('Error with file extension')
    input('[EXIT]')

with open(new_filename, 'w+') as f:
    f.write(
        converter.meta_to_json(content)
    )

print('SUCCESS')