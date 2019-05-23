# from arepldump import dump

import requests, json, logging, sys, functools, ast
from queue import Queue
from pprint import PrettyPrinter

prn = PrettyPrinter(indent=2).pprint
queue = Queue()

reduce = functools.reduce

def get_census_values(api_url, get_var, for_var, *in_vars):
    try:
        payload = {'get': get_var, 'for': for_var, 'in': in_vars}
        r = requests.get(api_url, params=payload)
        req = requests.Request("GET", api_url, params=payload)
        prep = req.prepare()
        print(prep.url)
        return r.json()
    except requests.exceptions.RequestException as e:
        logging.error('General Exception: {}'.format(e))
        sys.exit(1)
    except IOError as err:
        logging.error('IOError: {}'.format(err))
        

def parse_if_number(candidate):
    try: return ast.literal_eval(candidate)
    except: return candidate
    
def parse_out_number(candidate):
    parsed = parse_if_number(candidate)
    try:
        if (parsed < -100000):
            return candidate
        else:
            return parsed
    except:
        return candidate
    

# takes array of arrays and returns a dict that uses the first nested arrays' vals as keys for the rest:
# see actual result: https://api.census.gov/data/2017/acs/acs5?get=NAME,B01001_001E&for=state:*
def create_census_json(arr):
    keys_arr = arr[0]
    vals_arr = arr[1:]

    result = list(map(lambda vals: 
        reduce((lambda acc, this: 
            # or allows the accumulator to be returned first (don't ask me why that's not the default)
            acc.update({
                keys_arr[this[0]]: parse_out_number(this[1])
                }) or acc
            ), 
            # enumerate returns each item in the iterable paired with it's index: [(0, val1), (1, val2), ...]
            enumerate(vals), 
            {}),
        vals_arr))
    return result

        
queue.put(get_census_values("https://api.census.gov/data/2017/acs/acs5", "NAME,B01001_001E,B12007D_001E,B25070_001E,B25077_001E", "block group:*", "state:01", "county:025"))
prn(create_census_json(queue.get()))

# prn(list(map(lambda x: x, queue.get())))

# test_arr = [["key1", "key2", "key3"], [1, 2, 3], [4, 5, 6]]
# print(create_census_json(test_arr))




print("You {}".format("Jane"))

me = "Tarzan"

print(f"Me {me}")