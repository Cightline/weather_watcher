
import requests
import os
import json

from pushbullet import Pushbullet

home          = os.getenv('HOME')
config_path   = '%s/.config/weather_watcher/config.json' % (home)

with open(config_path, 'r') as cfg:
    config = json.load(cfg)

pb              = Pushbullet(config['pushbullet_api_key'])
api_key         = config['api_key']
state           = config['state']
city            = config['city']
weather_dir     = '%s/.weather_watcher' % (home)
values_to_write = ['weather','temp_f', "precip_today_in"]
color           = True

alert_url       = 'http://api.wunderground.com/api/%s/alerts/q/%s/%s.json' % (api_key, state, city)
condition_url   = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (api_key, state, city)



def get_page(url):
    
    page = requests.get(url)

    if page.status_code != 200:
        print('incorrect status code: %s' % (page.status_code))


    return page.json()



condition_data = get_page(condition_url)['current_observation']


a = get_page(alert_url)['alerts']

if not a:
    print('No alerts')
    exit()


else:
    alert_data = []
    data = (get_page(alert_url)['alerts'])
    
    for alert in data:
        print(alert)

        #pb.push_note('Weather Alert: %s' % (alert['type'], 
        #                                    alert['description'],
        #                                    alert['message']))

        pb.push_note(alert['description'], alert['message'])


