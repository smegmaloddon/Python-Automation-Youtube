# imports
from concurrent.futures import ThreadPoolExecutor

# functions
def Thread(
    func : object = None,
    items : list[dict] = [], 
    workers : int = 8
) -> None:
    
    # create executor() as thread manager
    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:
        
        # create 'futures' to wait for functions
        futures : list = [
            executor.submit(
                func, **item
            )
            for item in items
        ]

        # wait & finish function
        for future in futures:

            future.result()