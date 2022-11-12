import tkinter
from tkinter import ttk, messagebox
#from tkcalendar import Calendar
import converter # self-written module, included in this dir
import upload # self-written script, included in this dir
import json
from datetime import datetime
import sys
import requests
import snapshot


row = 0

# TODO fix validate input passing!


ENTRY_BUTTONS = {
  'Date':{'text':'now', 'on_click':lambda: datetime.now().strftime('%Y.%m.%d')},
  'Time':{'text':'now', 'on_click':lambda: datetime.now().strftime('%H:%M')},
  'SF6_pressure[bar]':{'text':'fetch', 'on_click':lambda: fetch('https://mill.capitan.imec.be/api/any/motrona_sf6')['counter_0_value']},
  'SF6_temperature[C]': {'text':'fetch', 'on_click':lambda: fetch('https://mill.capitan.imec.be/api/any/motrona_sf6')['counter_1_value']}
}

def fetch(url):
  try:
    print('fetching...')
    r = requests.get(url)
    return json.loads(r.text)
  except Exception as e:
    if type(e) == requests.exceptions.ConnectionError:
      messagebox.showwarning(title='An error accured while fetching the data.', message='ConnectionError: ' + str(type(e)) + ' while fetching data. ') #TODO custom message
    else:
      messagebox.showwarning(title='An error accured while fetching the data.', message='Error: ' + str(type(e)) + ' while fetching data.')


class Entry:
  def __init__(self, window, name):
    self.name = name
    # if button != {}:
      # self.create_button(window=window, button_data=button)
  
  def create_button(self, window, button_data:dict):
    button = tkinter.Button(
      window,
      text=button_data['text'],
      command=lambda: self.set_value(button_data['on_click']())
      )
    button.grid(row=row, column=2, sticky='E')

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
    return type(self).check_format(self.get_value())
  
  # def set_value(self, value):
  #   try:
  #     return self.current_value.set(value)
  #   except AttributeError:
  #     self.entry.set('')
      
class TextEntry(Entry):
  @classmethod
  def check_format(cls, value:str) -> bool:
    return True
  
  def __init__(self, window, name, button={}):
    super().__init__(window, name)
    global row
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
    print(type(self))
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
  def __init__(self, window, name, button={}):
    super().__init__(window, name, button=button)
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
  def __init__(self, window, name, button={}):
    super().__init__(window, name, button=button)
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
  def __init__(self, window, name, button={}):
    super().__init__(window, name, button)
  
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
  def __init__(self, window, name, button={}):
    super().__init__(window, name, button)
  
  @classmethod
  def check_format(cls, value:str) -> bool:
    if value.lower() in ['true', 'false']:
      return True
    else:
      return False
  
  # def validate_input(self):
  #   return self.get_value().lower() in ['true', 'false']


class HorizantalSeperator:
  def __init__(self, window):
    global row
    row += 1
    self.separator2 = tkinter.Frame(window, bd=10, relief='sunken', height=10)
    self.separator2.grid(row=row, column=1)
    row += 1

def search_entry(name) -> object:
  for entry in entries:
    if type(entry) == HorizantalSeperator:
      print(name)
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
  
  print(data)
  success, message = upload.upload_meta(
    # the upload function requires metadata, so we first need to convert the JSON data
    converter.json_to_meta(
      data,
      template=template_format # the template argument is used to keep the right format
      ) 
  )

  if success:
    messagebox.showinfo(title='Uploading file', message=message)
    snapshot.create_snaptshot()
    #TODO new msg
  else:
    messagebox.showwarning(title='Error while uploading metadata', message=message+'\nThe data is not saved.')
  
def create_entry(key, value) -> Entry:
  for entry_type in ENTRY_TYPES:
    if entry_type.check_format(value):
      # create the entry
      # check if there is a button registered for this entry
      if key in list(ENTRY_BUTTONS.keys()):
        return entry_type(second_frame, key, button=ENTRY_BUTTONS[key])
      else:
        return entry_type(second_frame, key)

def check_keywords(template_format, keywords_filename:str) -> bool:
  """Check if all keys in the template_format are alos in the keywords_file."""
  with open(keywords_filename, 'r') as f:
    content = f.read()
    data = json.loads(converter.meta_to_json(content))
    allowed_keywords_format = converter.load_format(content)
  
  for item in template_format:
    if type(item) == tuple: # (key, value)
      if not(item) in allowed_keywords_format:
        print(f'[ERROR]: key "{item[0]}" was not found in the keywords_file "{keywords_filename}".')
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
        entry = create_entry(key, value)

        entry.set_value(value) # set the entry value to the one on the template file
        entries.append(entry)

      elif template_item == converter.decoder.EmptyLine:
        entries.append(
          HorizantalSeperator(second_frame)
        )
      row += 1


    row += 1
    button = tkinter.Button(window, text='save', width=8, command=save)
    button.pack()

    window.mainloop()
    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 1 )
    # exit()
  except Exception as e:
    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 1 )
    print('[ERROR]: Unexpected error:')
    print('[ERROR]: '+str(e))
    input('[ERROR]: Press <ENTER> to continue')
    
  
    
