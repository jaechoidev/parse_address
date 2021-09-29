import sys
import re
import test

with_postal = r'([0-9]+[-]?[0-9]+) (.+) (.+) ([^ ]+) ([a-zA-Z][a-zA-Z]) ([a-zA-Z][0-9][a-zA-Z] ?[0-9][a-zA-Z][0-9])$'
without_postal = r'([0-9]+[-]?[0-9]+) (.+) (.+) ([^ ]+) ([a-zA-Z][a-zA-Z])$'
street_suffix = ['road', 'rd.', 'avenue', 'ave.','st.','street','dr.','drive','way']

def clean_up(address):
    '''
    strip whitespaces and comma
    '''
    cleaned_group = []
    for elem in address.groups():
        elem = elem.replace(',','')
        elem = elem.strip()
        cleaned_group.append(elem)
    return cleaned_group

def street_validation(street):
    '''
    split the street name by suffix list because city name might be more than 2 words.
    '''
    for st in street_suffix:
        if street.lower().endswith(st):
            return street, ''
    for st in street_suffix:
        street_match = re.match(r'(.+'+st+r')(.+)', street, re.M|re.I)
        if street_match:
            return street_match.group(1), street_match.group(2)
    return street, ''

def parse_to_dict(address_re):
    '''
    parse RE object to dict
    '''
    result = dict()
    cleaned_group = clean_up(address_re)
    street = "{} {}".format(cleaned_group[1],cleaned_group[2])
    street, city = street_validation(street)

    if '-' in cleaned_group[0]:
        result['unit'], result['number'] = cleaned_group[0].split('-')
    else:
        result['number'] = cleaned_group[0]

    result['street'] = street
    result['city'] = ' '.join([city,cleaned_group[3]])
    result['province'] = cleaned_group[4]

    if len(cleaned_group)>5:
        result['postal_code'] = cleaned_group[5]
    return result

def address_to_dict(address_str):
    '''
    check if there's postal code first
    and then, check without postal code.
    if there's no match for both, parsing will be returned as failed.
    '''
    add_postal = re.match(with_postal, address_str, re.M|re.I)
    if add_postal:
        return parse_to_dict(add_postal)

    add_no_postal = re.match(without_postal, address_str, re.M|re.I)
    if add_no_postal:
        return parse_to_dict(add_no_postal)
    
    return {'failed_parsing':address_str}

def run(data):
    for d in data:
        print(d + '  ->  ')
        print(address_to_dict(d))

def main(args):
    if len(args) == 1 or (len(args) >= 2 and args[1] == 'test'):
        print ('== running test data...==')
        run(test.postal_code)
        run(test.no_postal_code)
        run(test.invaild)
        print ('== parsing ended ===')    
    elif len(args) >= 2 and isinstance(args[1], str):
        print ('== running to parse data...==')
        run([args[1]])
        print ('== parsing ended ===')

if __name__ == "__main__":
    main(sys.argv)