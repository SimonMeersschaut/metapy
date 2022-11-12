from datetime import datetime

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