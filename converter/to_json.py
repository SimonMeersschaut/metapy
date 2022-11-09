from msilib.schema import Error
from . import decoder
from json import loads
from json.decoder import JSONDecodeError
from enum import Enum, auto
import string
import sys


class States(Enum):
  WaitForStar = auto()
  WaitForFirstLetterOfKey = auto()
  SavingKey = auto()
  WaitForFirstLetterOfValue = auto()
  SavingValue = auto()

def meta_to_json(meta:str) -> str:
  """Converts meta data to json."""
  # load all data
  data_lines = []
  for line in meta.split('\n'):
    data = meta_line_to_json(line)
    data_lines.append(data)

  # convert to JSON format
  output = '{\n'
  for i, data_line in enumerate(data_lines):
    if isinstance(data_line, tuple):
      output += f'"{data_line[0]}": "{data_line[1]}"'
      if any([isinstance(data, tuple) for data in data_lines[i+1:]]): #if there will be following data, a comma should be added
        output += ','
      output += '\n'
    elif data_line == decoder.EmptyLine:
      output += '\n'
  output += '}'
    
  return output


def meta_line_to_json(line:str) -> tuple:
  def char_following(s:str) -> bool:
    for char in s:
      if char == ':' or char == '=':
        return False
      if 32 < ord(char) < 127:
        return True
    return False

  state = States.WaitForStar
  key = ''
  value = ''
  for i, char in enumerate(line):
    if state == States.WaitForStar:
      if char == '*':
        state = States.WaitForFirstLetterOfKey
      elif char in string.ascii_letters:
        raise ValueError('key specified before *')
    elif state == States.WaitForFirstLetterOfKey:
      if char not in decoder.SPACE_CHARS:
        state = States.SavingKey
    elif state == States.WaitForFirstLetterOfValue:
      if (char == ':' and line[i+1] == '=') or (line[i-1] == ':' and char == '='):
        continue
      if char not in decoder.SPACE_CHARS:
        state = States.SavingValue
      
    if state == States.SavingKey:
      if char == ':' and line[i+1] == '=':
        state = States.WaitForFirstLetterOfValue
      else:
        if char_following(line[i:]):
          key += char
    elif state == States.SavingValue:
      value += char
  
  if state == States.SavingValue: #succesfully read line
      return (key, value)
  elif state == States.WaitForFirstLetterOfKey: #empty line (with star)
    return decoder.EmptyLine
  elif state == States.WaitForStar: # empty line
    return decoder.EmptyLine
  elif state == States.WaitForFirstLetterOfValue:
    return (key, "")
  elif state == States.SavingKey:
    print('WARNING - There are lines in meta-file without delimiter (not included in json).')
  else:
    print(f'Suspect meta-file error; state={state}')