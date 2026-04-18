# imports 
import requests
import random
import time

# constants
TIME_LIST : list[str] = [

    'day',
    'week',
    'month',
    'year',
    'all'
]
MAXIMUM_ERROR : int = 3
QUERY_LIST: list[str] = [

    'hot', 
    'new',
    'top',
    'rising',
    # 'controversial'
]
TIME_DELAY : float = 0.75
HEADERS : dict[str : str] = {
    'User-Agent': 'my-reddit-app/0.1'
}

# global variables
error : float = 0

# functions
def Run(
    archive : list[str]
) -> list:

    # set local to global variable
    global error
    
    time.sleep(
        TIME_DELAY
    )
    if error >=MAXIMUM_ERROR:

        raise ResourceWarning(
            'Possible RATE-LIMIT'
        )
    
    # assert array
    assert isinstance(
        archive, list
    ) and len(
        archive
    ) != 0, 'Archive must not be \'None\' /or length of 0'

    # fetch query & page & timezone
    query : str = random.choice(
        seq=QUERY_LIST
    ) # hot, rising..
    page : str = random.choice(
        seq=archive
    ) # instantkarma, fails..
    timezone : str = random.choice(
        seq=TIME_LIST
    ) # best, today..

    # build url & request
    url : str = f'https://www.reddit.com/r/{page}/{query}.json?t={timezone}'

    # fetch response & error check
    response : requests.Response = requests.get(
        url=url,
        headers=HEADERS
    )
    if response.status_code != 200:

        print('failed : ', url)
        error = error +1

        # return list[]
        return []
    
    # reduce error
    error = error -0.5
    
    # convert to .json & build posts
    response : dict = response.json()
    placeholder : list[dict] = [
        array['data']
        for array in response['data']['children']
    ]

    return placeholder
