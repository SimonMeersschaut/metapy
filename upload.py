import converter
import glob
import json
from datetime import datetime
import string
import os
import sys

def upload_meta(metadata:str):
  # First convert it to a dictionary to perform a check
  json_data = json.loads(converter.meta_to_json(metadata))
  if file_already_uploaded(json_data)[0]:
    return (False, 'This file is already used in: '+file_already_uploaded(json_data)[1])
    # input('Press [enter] to exit')
    # exit()
  else:
    # UPLOAD
    with open(f'datafiles/{generate_filename()}', 'w+') as f:
      f.write(metadata)
    return (True, 'successfully uploaded the file')

def file_already_uploaded(json_data:dict) -> (bool, str):
  '''
  Check in all uploaded files if the same date is entered (date & time).
  '''
  # check for all json files
  for filename in glob.glob('datafiles/*.json'):
    with open(filename, 'r') as f:
      data = json.load(f)
    try:
      if data['Date'] == json_data['Date'] and data['Time'] == json_data['Time']:
        return (True, filename)
    except KeyError:
      print('No date in previously uploaded meta file')
  
  # Now check for meta files
  for filename in glob.glob('datafiles/*.meta'):
    with open(filename, 'r') as f:
      content = f.read()
      data = json.loads(converter.meta_to_json(content))
    try:
      if data['Date'] == json_data['Date'] and data['Time'] == json_data['Time']:
        return (True, filename)
    except KeyError:
      print('No date in previously uploaded meta file')
  
  return (False, None)

def generate_filename() -> str:
  '''
  Generates a filename for a new meta file.
  -> format: the date (Year.Month.day) + a letter (to avoid duplicate filenames)
  '''
  now = datetime.now()
  filename = ''
  i = 0
  while filename == '' or os.path.exists('datafiles/'+filename):
    filename = f'{now.strftime("%Y.%m.%d")}{string.ascii_lowercase[i]}.meta'
    i += 1
  return filename

if __name__ == '__main__':
  # Upload file
  filename = sys.argv[1]
  print('Uploading: '+filename)
  with open(filename, 'r') as f:
    content = f.read()
  success, msg = upload_meta(content)
  if success:
    print('[SUCCESS] uploaded the file')
  else:
    print('[ERROR] '+msg)