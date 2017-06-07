import os

#Number of processes the matcher will use.
processes = 4
#Whether the matcher will use split matching as well as hard matching
split_match_enabled = True
#Paths to files
path = os.path.dirname(os.path.abspath(__file__))
tmp_path = path + '/tmp/'
product_file_path = path + '/data/products.txt'
listings_file_path = path + '/data/listings.txt'
results_file_path = path + '/data/results.txt'