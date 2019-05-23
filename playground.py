import requests, json, logging, sys


def get_census_values(api_url, get_var, for_var):
    try:
        payload = {'get': get_var, 'for': for_var}
        r = requests.get(api_url, params=payload)
        return r.json()
    except requests.exceptions.RequestException as e:
        logging.error('General Exception: {}'.format(e))
        sys.exit(1)
    except IOError as err:
        logging.error('IOError: {}'.format(err))
        
        
result = get_census_values("https://api.census.gov/data/2017/acs/acs5", "NAME", "state:*")

print(result)

