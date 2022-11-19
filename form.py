import tkinter
from tkinter import ttk, messagebox
#from tkcalendar import Calendar
import converter # self-written module, included in this dir
import upload # self-written script, included in this dir
import json
from datetime import datetime
import sys
import requests
from  buttons import ENTRY_BUTTONS

row = 0

# TODO fix validate input passing!

entries = []
def get_entry(name):
  for entry in entries:
    try:
      if entry.name == name:
        return entry
    except AttributeError:
      # Horizontal Seperator
      pass

class Entry:
  def __init__(self, window, name, row):
    self.name = name
    # if button != {}:
      # self.create_button(window=window, button_data=button)
  
  def create_button(self, window, button_data:dict):
    try:
      print(button_data)
      rowspan = button_data['rowspan']
    except KeyError:
      rowspan = 1
    

    button = tkinter.Button(
      window,
      text=button_data['text'],
      command= lambda: self.run_button_action(button_data['on_click'])
    )
    button.grid(row=row, column=2, sticky=tkinter.N+tkinter.S, rowspan=rowspan)
  
  def run_button_action(self, action):
    if type(action) == callable: 
      #function
      ...
    elif type(action) == dict:
      try:
        self.set_value(action['self']())
      except KeyError:
        pass
      
      for key, value in action.items():
        try:
          get_entry(key).set_value(value())
        except AttributeError:
          if key != 'self':
            raise RuntimeError(f"'{key}' could not be found.")
        


  def get_value(self):
    try:
      return self.entry.value()
    except AttributeError:
      pass
    
    try:
      return self.current_value.get()
    except AttributeError:
      pass
  
  def validate_input(self) -> bool:
    # pass function to base class
    return type(self).check_format(self.get_value())
  

class TextEntry(Entry):
  @classmethod
  def check_format(cls, value:str) -> bool:
    return True
  
  def __init__(self, window, name, row, button={}):
    super().__init__(window, name, row)
    label = tkinter.Label(window, text=name)
    label.grid(row=row, column=0, sticky="W")

    self.entry = tkinter.Entry(window, width=70)
    self.entry.grid(row=row, column=1, sticky='W')
    self.entry.bind('<FocusOut>', self.focus_out)
    if button != {}:
      self.create_button(window, button)
  
  def get_value(self) -> str:
    return self.entry.get()
  
  # def validate_input(self):
  #   return True
  
  def focus_out(self, event):
    # print(self.validate_input())
    # print(type(self))
    if not(self.validate_input()):
      self.entry.config(highlightbackground='red')
      self.entry.config(highlightthickness=2)
    else:
      self.entry.config(highlightbackground='white')
      self.entry.config(highlightthickness=0)
  
  def set_value(self, value):
    self.entry.delete(0,tkinter.END)
    self.entry.insert(0,value)

class DateEntry(TextEntry):
  def __init__(self, window, name, row, button={}):
    super().__init__(window, name, row, button=button)
    # now = tkinter.Button(window, text='now', command=self.set_to_now)
    # now.grid(row=row, column=1, sticky='E')
  
  @classmethod
  def check_format(cls, date_str) -> bool:
    try:
      _ = datetime.strptime(date_str, '%Y.%m.%d')
      return True
    except ValueError: #FIXME
      return False
  
  # def validate_input(self):
  #   try:
  #     _ = datetime.strptime(self.get_value(), '%Y.%m.%d')
  #     return True
  #   except ValueError: #FIXME
  #     return False
    
class TimeEntry(TextEntry):
  def __init__(self, window, name, row, button={}):
    super().__init__(window, name, row, button=button)
    # now = tkinter.Button(window, text='now', command=self.set_to_now)
    # now.grid(row=row, column=1, sticky='E')
  
  @classmethod
  def check_format(cls, date_str) -> bool:
    try:
      _ = datetime.strptime(date_str, '%H:%M')
      return True
    except ValueError: #FIXME
      return False
  
  # def validate_input(self):
  #   try:
  #     _ = datetime.strptime(self.get_value(), '%H:%M')
  #     return True
  #   except ValueError: #FIXME
  #     return False


class FloatEntry(TextEntry):
  def __init__(self, window, name, row, button={}):
    super().__init__(window, name, row, button)
  
  @classmethod
  def check_format(cls, value:str) -> bool:
    try:
      _ = float(value)
      return True
    except ValueError:
      return False
  
  # def validate_input(self):
  #   try:
  #     _ = float(self.get_value())
  #     return True
  #   except ValueError: #FIXME
  #     return False
  
class BooleanEntry(TextEntry):
  def __init__(self, window, name, row, button={}):
    super().__init__(window, name, row, button)
  
  @classmethod
  def check_format(cls, value:str) -> bool:
    if value.lower() in ['true', 'false']:
      return True
    else:
      return False
  
  # def validate_input(self):
  #   return self.get_value().lower() in ['true', 'false']


class HorizantalSeperator:
  def __init__(self, window, row):
    row += 1
    self.separator2 = tkinter.Frame(window, bd=10, relief='sunken', height=10)
    self.separator2.grid(row=row, column=1)
    row += 1

def search_entry(name) -> object:
  for entry in entries:
    if type(entry) == HorizantalSeperator:
      # print(name)
      continue
    if entry.name == name:
      return entry
  return None #()

def save():
  # check all entries
  # if not(all(entry.validate_input() for entry in entries)):
  for entry in entries:
    # try:
    if type(entry) == HorizantalSeperator:
      continue
    if not entry.validate_input():
      messagebox.showwarning(title='Error while uploading metadata', message='The input to an entry was not valid: ' + entry.name + '\nThe data is NOT saved.')
      return None
    # except AttributeError: # Some objects don't have a validate_input func e.g. HorizontalSeperator
    #   pass


  global template
  data = {}
  for template_item in template_format:
    # search the input from the entries
    if type(template_item) == tuple:
      template_key, _ = template_item
      entry = search_entry(template_key)
      if entry:
        value = entry.get_value()

        if value == None or value == '':
          value = '/'
        data.update({entry.name: value})
      else:
        raise RuntimeError('ERROR: entry could not be found')
    else:
      pass # skip empty lines
  
  # print(data)
  try:
    success, message = upload.upload_meta(
      # the upload function requires metadata, so we first need to convert the JSON data
      converter.json_to_meta(
        data,
        template=template_format # the template argument is used to keep the right format
        ),
        allowed_keywords_filename=ALLOWEDKEYWORDS
    )
  except Exception as e:
    messagebox.showwarning(title='Uploading file', message=e.__repr__())
    raise e
  print('success, message')
  if success:
    messagebox.showinfo(title='Uploading file', message=message)
    
    #TODO new msg
  else:
    messagebox.showwarning(title='Error while uploading metadata', message=message+'\nThe data is not saved.')
  
def create_entry(key, value, row) -> Entry:
  for entry_type in ENTRY_TYPES:
    if entry_type.check_format(value):
      # create the entry
      # check if there is a button registered for this entry
      if key in list(ENTRY_BUTTONS.keys()):
        return entry_type(second_frame, key, row, button=ENTRY_BUTTONS[key])
      else:
        return entry_type(second_frame, key, row)

def check_keywords(template_format, keywords_filename:str) -> bool:
  """Check if all keys in the template_format are alos in the keywords_file."""
  with open(keywords_filename, 'r') as f:
    content = f.read()
    data = json.loads(converter.meta_to_json(content))
    allowed_keywords_format = converter.load_format(content)
  for item in template_format:
    if type(item) == tuple: # (key, value)
      template_key = item[0]
      #print(item)
      #print(allowed_keywords_format)
      if not(template_key in [item[0] for item in allowed_keywords_format if type(item) == tuple]):
        print(f'[ERROR]: key "{template_key}" was not found in the keywords_file "{keywords_filename}".')
        return False
  return True

ENTRY_TYPES = [
  DateEntry,
  FloatEntry,
  BooleanEntry,
  TimeEntry,
  TextEntry
]


if __name__ == '__main__':
  # HIDE CMD
  import ctypes
  ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
  try:
    try:
      ALLOWEDKEYWORDS = sys.argv[1]
      TEMPLATE_FILE = sys.argv[2]
    except IndexError:
      raise Exception('No allowedkeywords and/or template file given.')
    # Load template file
    try:
      with open(TEMPLATE_FILE, 'r') as f:
        content = f.read()
        data = json.loads(converter.meta_to_json(content))
        template_format = converter.load_format(content)
    except FileNotFoundError:
      print(f'No `{TEMPLATE_FILE}´-file found in current working directory.')
      input('[ENTER] to exit')
    
    # check keywords of template file with the allowedkeywords.meta - file
    if check_keywords(template_format, ALLOWEDKEYWORDS):
      ## SUCCESS
      pass
    else:
      raise Exception('template file does not match allowed keywords file.')

    # Create the tkinter window
    window = tkinter.Tk()
    window.option_add( "*font", "lucida 12" )
    # window.maxsize(width=700, height=800)
    window.minsize(width=550, height=500)
    window.geometry('1000x800')
    
    window.title('Form')
    # window.maxsize(500, 500)

    # Create scrollbar
    my_canvas = tkinter.Canvas(window)
    my_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

    scrollbar = tkinter.ttk.Scrollbar(window, orient=tkinter.VERTICAL, command=my_canvas.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion= my_canvas.bbox('all')))

    second_frame = tkinter.Frame(my_canvas)
    second_frame.config(highlightthickness=0)

    my_canvas.create_window((0,0), window=second_frame, anchor='nw')



    entries = []
    for template_item in template_format:
      if type(template_item) == tuple:
        key, value = template_item
        # find type of value
        entry = create_entry(key, value, row)

        entry.set_value(value) # set the entry value to the one on the template file
        entries.append(entry)

      elif template_item == converter.decoder.EmptyLine:
        HorizantalSeperator(second_frame, row)
      row += 1


    row += 1
    button = tkinter.Button(window, text='save', width=8, command=save)
    button.pack()

    window.mainloop()
    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 1 )
    exit()
  except Exception as e:
    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 1 )
    print('[ERROR]: Unexpected error:')
    print('[ERROR]: '+e.__repr_())
    input('[ERROR]: Press <ENTER> to continue')
    exit()
    
  
    
