import json
import config

def split_file(path_to_file, split_into):
    lines_in_file = sum(1 for line in open(path_to_file))
    base_size = lines_in_file // config.processes
    line_count_list = [base_size for i in range(config.processes)]
    files_with_an_extra_line = lines_in_file % split_into
    for i in range(files_with_an_extra_line):
        line_count_list[len(line_count_list) - (i + 1)] += 1
    
    lines_written = 0
    file_number = 0
    split_files = []
    split_file = 'split_file' + str(file_number) + '.txt'
    split_files.append(split_file)
    next_split = line_count_list[0]    
     
    with open(path_to_file, 'r') as product_handle:
        for line in product_handle:       
            with open(config.tmp_path + '/' + split_file, 'a+') as results_handle:
                results_handle.write(line)
                lines_written = lines_written + 1
                if lines_written == next_split:
                    if file_number != split_into - 1:
                        file_number = file_number + 1                                           
                        next_split = next_split + line_count_list[file_number]
                        split_file = 'split_file' + str(file_number) + '.txt'
                        split_files.append(split_file)
                        
    return split_files

def process_product_file(file, process_number):
    
    print('Process ' + str(process_number) + ' starting...')
    products_processed = 0
    hard_cnt = 0
    split_cnt = 0
    
    with open(config.tmp_path + '/' + file, 'r') as product_handle:
        for line in product_handle:
            result = {}        
            product = json.loads(line)
            
            result['product_name'] = product['product_name']
            result['listings'] = []
            
            with open(config.listings_file_path, 'r') as listings_handle:
                for line in listings_handle:
                    listing = json.loads(line)
                                   
                    if product['product_name'].replace('_', ' ') in listing['title']:
                        hard_cnt = hard_cnt + 1
                        result['listings'].append(listing)
                        continue;
                    
                    if not config.split_match_enabled:
                        continue;
                    
                    split = product['product_name'].split('_')
                    
                    split_match = True
                    
                    for word in split:
                        if word not in listing['title']:
                            split_match = False
                    
                    if split_match:
                        split_cnt = split_cnt + 1
                        result['listings'].append(listing)              
                     
            with open(config.tmp_path + '/' + '/results_' + file, 'a+') as results_handle:    
                json.dump(result, results_handle)
                results_handle.write('\n')           
            
            products_processed = products_processed + 1

         
    if config.split_match_enabled:  
        print('Process ' + str(process_number) + ' finished: ' +  str(products_processed) + ' products processed - found ' + str(hard_cnt) + ' hard matches and ' + str(split_cnt) + ' split matches.')
    else:
        print('Process ' + str(process_number) + ' finished: ' +  str(products_processed) + ' products processed - found ' + str(hard_cnt) + ' hard matches.')
        
def merge_files(split_files):
    for split_file in split_files:
        results_handle = open(config.results_file_path, 'a+')
        with open(config.tmp_path + 'results_' + split_file, 'r') as split_handle:
            for line in split_handle:
                results_handle.write(line)
                
