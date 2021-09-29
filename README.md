# Parsing Addresses

This is for parsing addresses given in the following format and returns the components as a dictionary. 

## examples 
123 Main St Vancouver BC A1B2C3 ->
{‘number’: 123, ‘street’: ‘Main St’, ‘city’: ‘Vancouver’, ‘province’: ‘BC’, ‘postal_code’: ‘A1B2C3’}


Eg2. 4-567 W8th Ave Vancouver BC D4E5F6 ->
{‘unit’: 4, ‘number’: 567, ‘street’: ‘W8th Ave’, ‘city’: ‘Vancouver’, ‘province’: ‘BC’, ‘postal_code’: ‘D4E5F6’}


## How it works

1. 
```
>>> import parse
>>> parse.address_to_dict('123 Main St Vancouver BC A1B2C3')
{'province': 'BC', 'city': 'Vancouver', 'street': 'Main St', 'postal_code': 'A1B2C3', 'number': '123'}
```

2. 
```
% python parse.py '123 Main St Vancouver BC A1B2C3' 
```

3. There's some test cases to see the results
```
% python parse.py test
```

## Valid Cases and invalid cases

#### Postal Code : 6 characters(char/digit/char/digit/char/digit) and allows one middle spacing.
- Valid : A1B2C3 , A1B 2C3
- invalid : A 1 B 2 C 3, A1 B2 C3, A1B2C 3 .... etc

#### unit + number : any numbers without spacing and allows one dash to separate unit and number
- Valid : 123-123, 1-23, 1234-1242, 123, 12, ...
- invalid : 123 - 123, 12- 12, 123 4, ... etc

#### Province : consist of 2 chars, not case-sensitive
- Valid : BC, NC, ON, on, bc, ..
- invalid : British Columbia, .. (more than 2 chars)

#### city : one word, could be more than 2 words in some cases (explained below)
- Valid : Vancouver, Toronto, Quebec-city 
- invalid : Quebec City, (more than 2 words..)

if the street name ends with proper suffix, city name could be more than 2 words
> ex) 12-629 King Road Saint Nicolas, QC 

#### street
street and city names are not seperated by comma or something, so it was hard to make them as a regular case. So, this code is detecting street name as greedy (city name as 1 word, and others will be street name) and then split the street name by suffix like below. 

> street_suffix = ['road', 'rd.', 'avenue', 'ave.','st.','street','dr.','drive','way']

Basically street name will be take more words like this. 
> ex) 7141 High Noon Court Carbonear, LB -> street: High Noon Court

However, if street name has one of the suffix in the list, it would be seperated from there. 
> ex) 12-629 King Road Saint Nicolas, QC  -> street: King Road


