
import requests
import os
import json

with open(config_path, 'r') as cfg:
    config = json.load(cfg)

api_key       = config['api_key']
state         = config['state']
city          = config['city']
home          = os.getenv('HOME')
weather_dir   = '%s/.weather_watcher' % (home)
config_path   = '%s/.config/weather_wather/config.json'
values_to_write = ['weather','temp_f', "precip_today_in"]
pango         = True

alert_url     = 'http://api.wunderground.com/api/%s/alerts/q/%s/%s.json' % (api_key, state, city)
condition_url = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (api_key, state, city)



def get_page(url):
    
    page = requests.get(url)

    if page.status_code != 200:
        print('incorrect status code: %s' % (page.status_code))


    return page.json()


def write_to_file(base_path, data):
    with open('%s/%s' % (weather_dir, base_path), 'w') as f:

        try:
            to_write = str(int(data))

        except:
            to_write = str(data).strip().lower()
            
            
        f.write(to_write)



condition_data = get_page(condition_url)['current_observation']


for item in values_to_write:
    write_to_file(item, condition_data[item])


a = get_page(alert_url)['alerts']

if not a:
    alert_data = "none"

else:
    if pango:
        alert_data = "<span color='red'>%s</span>" % (get_page(alert_url)['alerts'][0]['description'])

    else:
        alert_data = "%s" % (get_page(alert_url)['alerts'])





write_to_file('alerts', alert_data)
