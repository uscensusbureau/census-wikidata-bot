# from arepldump import dump

import requests, json, logging, sys, queue, pprint, functools

prn = pprint.PrettyPrinter(indent=2)
pipe = queue.Queue()
reduce = functools.reduce

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
        
        

def create_census_json(arr):
    keys_arr = arr[0]
    vals_arr = arr[1:]
    # return vals_arr

    result = list(map(lambda vals: 
        reduce(lambda acc, this: 
            acc.update({keys_arr[this[0]]: this[1]}) or acc, 
            enumerate(vals),
            {}),
        vals_arr))
    return result

        
pipe.put(get_census_values("https://api.census.gov/data/2017/acs/acs5", "NAME,B01001_001E", "state:*"))

# prn.pprint(list(map(lambda x: x, pipe.get())))
prn.pprint(create_census_json(pipe.get()))

# test_arr = [["key1", "key2", "key3"], [1, 2, 3], [4, 5, 6]]
# print(create_census_json(test_arr))




print("test {}".format("me"))

me = "Tarzan"

print(f"Me {me}")