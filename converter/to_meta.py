from . import decoder
from enum import Enum, auto
import json


class States(Enum):
  WaitKeyBegin = auto() # waiting for the key to begin with a "
  KeyBegan = auto() # Reading the key, wich ends with a "
  WaitValueBegin = auto() # waiting for the value to begin with a "
  ValueBegan = auto() # Reading the value, wich ends with a "

def json_to_meta(json_data:dict, template:list = None):
  if type(json_data) == dict:
    # stringify the JSON-dict 
    # NOTE: the indent is required as it will return the dict in the right fomat
    json_data = json.dumps(json_data, indent=9999)

  print(json_data)
  data_lines = []
  for line in json_data.split('\n'):
    data_lines.append(json_line_to_meta_line(line))
  
  print(data_lines)

  # calculate max length (to optimize the spaces in the table)
  max_key_length = max([len(data_line[0]) for data_line in data_lines if data_line != None and data_line != decoder.EmptyLine])  

  output = ''
  if template == None:
    # no template given -> just put it in the order as it was recieved (in the dict)
    for data_line in data_lines:
      if data_line == None:
        pass
      elif data_line == decoder.EmptyLine:
        # add an empty line (with the star)
        if output != '':
          output += '\n'
        output += ' *'
      else:
        # write the key and value
        output += f'\n * {data_line[0]}{"".join([" " for i in range(max_key_length - len(data_line[0]) + 1)])}:= {data_line[1]}'
  else:
    # follow the template (list)
    for template_item in template:
      if template_item == decoder.EmptyLine:
        output += '\n *'
      else:
        # template_item is the key
        template_key, _ = template_item
        # get value
        for data_line in data_lines:
          if data_line:
            if template_key == data_line[0]:
              break
        if template_key  and data_line and template_key == data_line[0]:
          value = data_line[1]
          output += f'\n * {data_line[0]}{"".join([" " for i in range(max_key_length - len(data_line[0]) + 1)])}:= {value}'

  return output


def json_line_to_meta_line(json_line:str) -> str:
  """Convert a json line into a meta line."""
  if '{' in json_line or '}' in json_line:
    return
  json_line = json_line.replace('{', '').replace('}', '')
  
  state = States.WaitKeyBegin
  key, value = ('', '')
  for i, char in enumerate(json_line):
    if state == States.WaitKeyBegin:
      if char == '"':
        state = States.KeyBegan
    elif state == States.KeyBegan:
      if char == '"':
        state = States.WaitValueBegin
      else:
        key += char
    elif state == States.WaitValueBegin:
      if char == '"':
        state = States.ValueBegan
    elif state == States.ValueBegan:
      if char == '"':
        break
      else:
        value += char
  
  if key and value: 
    #Success
    return (key, value)
  else: 
    #Empty line
    return decoder.EmptyLine
  
if __name__ == '__main__':
  print(json_to_meta({"test":"z", "t":"z", "q":"r"}, order=['q']))