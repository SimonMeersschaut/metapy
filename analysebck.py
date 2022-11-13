import glob
import json
from datetime import datetime
import string
import sys
import metapy

DELIMETER = '\t'
EMPTY_VALUE = '/'

def load_date(filename:str) -> datetime:
  """Converts a filename eg. '2022.08.06a.json' to a datetime object."""
  date:str = filename.split('.meta')[0].split('\\')[-1][:-1]
  return datetime.strptime(date, '%Y.%m.%d')

def filter_file(filename:str, content, filter_func_args) -> bool:
  """
  A function, that is called for each file to check wether it should be filtered out or not.
  -> True  | append file in csv
  -> False | filter out / don't use
  """
  try:
    start_date, end_date = filter_func_args
  except Exception as e:
    raise ValueError('The filter function (used to filter out json files) wrong arguments: '+str(e))
  if not start_date:
    return True
  else:
    return start_date <= load_date(filename) <= end_date #and content['Sample_piece'] == '1'

def meta_files_to_csv(filenames, allowed_keys_file:str, filter_func:callable, filter_func_args:tuple) -> str:
  '''
  Loads all json files and combines them into one csv file.
  1. load all files
  2. filter out the files using the filter func
  3. saves all the keys that are used in every file and stores it in list: keys
  4. generates a csv string
  Arguments:
    * filenames: a list of all filenames or paths to the files
    * filter_func: a function that is called on each file with the filename and content as parameters (+filter_func_args)
    * filter_func_args: the last parameter of the filter_func
  Returns:
    A string with the data of all (filtered) files, in a csv-format.
  '''
  
  #load all meta files
  data = {}
  file_contents = []
  files_filtered = 0
  for i, file_name in enumerate(filenames):
    with open(file_name, 'r') as f:
      #data = json.load(f)
      content = f.read()
      data = json.loads(metapy.meta_to_json(content, check_keys=False)) # checking if a key is valid or not will be done later
      #print(data)
  
    if filter_file(file_name, data, filter_func_args):
      print(f"{i+1}. {file_name}")
      file_contents.append(data)
    else:
      files_filtered += 1
      print(f'{i+1}. {file_name} x')
  print(f'{files_filtered} files rejected')

  # load all keys
  keys = []
  # first load allowed keys
  with open(allowed_keys_file, 'r') as f:
    content = f.read()
  allowed_keys = list(json.loads(metapy.meta_to_json(
    content,
    check_keys=False
  )).keys())
  keys = keys + allowed_keys

  # check if all keys are valid
  for file_content in file_contents:
    for key in list(file_content.keys()):
      if not(key in keys):
        keys.append(key)
  
  # create header
  csv:str = ''
  for i, key in enumerate(keys):
    csv += key
    if i != len(keys) - 1:
      csv += DELIMETER
  csv += '\n'

  # append the data of every line to the csv
  for file_name, file_content in zip(filenames, file_contents):
    for key_i, key in enumerate(keys):
      if key in file_content.keys(): # if this file has a value for that key
        csv += file_content[key]
      else: # a default value for if the json file doesn't have a value for the key
        csv += EMPTY_VALUE
      if key_i != len(keys)-1:
        csv += DELIMETER
    csv += '\n'
  return csv

if __name__ == '__main__':
  #load args
  import sys
  if len(sys.argv) == 2:
    _, allowed_keys_file = sys.argv
  elif len(sys.argv) == 3:
    _, allowed_keys_file, start_date = sys.argv
  elif len(sys.argv) >= 4:
    _, allowed_keys_file, start_date, end_date = sys.argv
  else:
    print('not enough arguments')
  try:
    start_date = datetime.strptime(start_date, '%Y.%m.%d')
  except IndexError:
    start_date = None
  try:
    end_date = datetime.strptime(end_date, '%Y.%m.%d')
  except IndexError:
    end_date = datetime.now()

  # create csv data
  filenames = glob.glob('../datafiles/*.meta')
  #print(filenames)
  csv = meta_files_to_csv(filenames, allowed_keys_file, filter_func=filter_file, filter_func_args=(start_date, end_date))

  #write csv to output file
  with open('analysis.txt', 'w+') as f:
    f.write(csv)
  #input('[ENTER] to exit')