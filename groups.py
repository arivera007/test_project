###################################################################################
# Interview project for MightyHive
# Author: Adriana Rivera
# Usage: groups.py nameOfFile [email, phone or both]
###################################################################################

import csv
import sys


def get_fields_to_compare(row, match_type):
    """
    Calculates the fields that will be checked.
    For now is hardcoded, need to ask if I need to parse the header of the file.
    Returns: A list with the field numbers
    """
    if match_type == 'email':
        if len(row) < 6:
            return [3]
        else:
            return [4, 5]
    elif match_type == 'phone':
        if len(row) < 6:
            return [2]
        else:
            return [2, 3]
    else:
        if len(row) < 6:
            return  [2, 3]
        else:
            return  [2, 3, 4, 5]
            
def calculate_id(row, matches, fields, unique_id):
    """
    Analizes the important fields from the row, and obtains the needed id.
    This is done by keeping a counter in a hash table by either the email or phone.
    Returns the applicable if for the specific row.
    """
    if unique_id == 0:               # If it is the header row, just return title and unique id will start at 1.
        return ['ID', 1]               
    curr_id = 0
    for field in fields:        # List with fields numbers that need to be compared. [phone1, phone2, phoneN, email1, email2, emailN]
        key_data = row[field]
        if key_data in matches:
            curr_id = matches[key_data]      # if the email or phone matches a value in the hashmap, that becomes the id for the entire row.
            break                           # so we stop checking the rest of the fields (columns).
    if curr_id == 0:
        curr_id = unique_id                 # if matched not found, we get the master unique value
        unique_id += 1                      # update the master counter.
    for field in fields:                    # Add to the hashmap, the id that belongs to that particular phone or email.
        key_data = row[field]
        if key_data != '':       ## Doublee check empty columns could be different from ''
            matches[key_data] = str(curr_id)
    return [curr_id, unique_id]
    

def clasify_groups(input_file, match_type):
    """
    Reads one line, calculates the unique identifier, and in the same loop writes the updated row
    into a newfile. Only one row at a time is in memory.
    Returns: the name of the file with the results.
    """
    matches = {}
    unique_id = 0
    result_file = 'copy_'+input_file
    with open(input_file, 'rU') as original_f, open(result_file, 'w') as copy_f:
        reader = csv.reader(original_f, delimiter=',')
        writer = csv.writer(copy_f)
        for i, row in enumerate(reader):
            if i == 0:
                fields = get_fields_to_compare(row, match_type)         ##if fields == []
            row_id, unique_id = calculate_id(row, matches, fields, unique_id)   # row_id and unique_id are the same is row is not matched to a previous one.
            writer.writerow([str(row_id)] + row)
    return result_file    
        
        
if __name__ == "__main__":
    filename = sys.argv[1]
    match_type = sys.argv[2]
    result_file = clasify_groups(filename, match_type)
    print "Done digesting your file. Results found at: ", result_file
    
    