import converter
import glob
import json
from datetime import datetime
import string
import os
import sys
import snapshot

def upload_meta(metadata:str):
  # First convert it to a dictionary to perform a check
  json_data = json.loads(converter.meta_to_json(metadata))
  if file_already_uploaded(json_data)[0]:
    # file already uploaded
    return (False, 'This file is already used in: '+file_already_uploaded(json_data)[1])
    # input('Press [enter] to exit')
    # exit()
  else:
    # file not yet uploaded
    # => UPLOAD
    with open(f"datafiles/{generate_filename(json_data['Date'], json_data['Time'])}", 'w+') as f:
      f.write(metadata)
    snapshot.create_snaptshot()
    return (True, 'successfully uploaded the file')

def file_already_uploaded(json_data:dict) -> (bool, str):
  '''
  Check in all uploaded files if the same date is entered (date & time).
  '''
  # Check for meta files
  for filename in glob.glob('datafiles/*.meta'):
    checking_file_date = filename.split('.meta')[0].split('datafiles/')[-1]
    # with open(filename, 'r') as f:
    #   content = f.read()
    #   data = json.loads(converter.meta_to_json(content))
    # now, we don't need to check the content of the files, as the time is also written in the filename
    try:
      print(checking_file_date, json_data['Date']+'_'+json_data['Time'])
      if checking_file_date == json_data['Date']+'_'+json_data['Time']:
        return (True, filename) # file already uploaded
    except KeyError:
      print('No date in previously uploaded meta file')
  
  return (False, None)

def generate_filename(date:str, time:str) -> str:
  '''
  Generates a filename for a new meta file.
  -> format: the date (Year.Month.day) + a letter (to avoid duplicate filenames)
  '''
  return f'{date}_{time}.meta'

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