#### An experiment in matching and parallel processing. It takes the products found in data/products.txt and finds matching listings for them from data/listings.txt using parallel processing to make it speedy.

It requires Python 3 and probably Linux - I haven't run it anywhere else, in any case.

To run, execute go.py.

## Matching

It uses two methods of matching, which I am calling Hard Matching and Split Matching.

Let's say we have a product name of "Acme Thunderer".

The Hard Matcher searches for that full string in the description, so that "Blue **Acme Thunderer**" whould be matched, but "Acme Blue Thunderer" would not.

The Split Matcher matches if it finds the component words of the product name at any place within the description, so it would match both "Blue **Acme Thunderer**" and "**Acme** Blue **Thunderer**".

Split Matching can be turned off in the config.

## Mutiple Parallel Processes

The program is distributed across any number of parallel processes, so reducing the wall time in processing the products. From the data given in /data and on my laptop, using one process completes the task in around 65 seconds. With the default setting of four processes, this is reduced to around 22 seconds.

The number of processes are configurable within config.py. I found on my machine increasing above four kicks in the law of diminishing returns, and beware - this is just for a bit of a fun and experimentation, it is not anything like a production-
 ready bit of kit, it has no safety valves and if you raise the number of processes too high it will bring your machine to its knees without a trace of shame or remorse.
