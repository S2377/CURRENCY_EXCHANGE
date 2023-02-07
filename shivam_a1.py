'''Module for currency exchange
This module provides several string parsing functions to
implement a
simple currency exchange routine using an online currency
service.
The primary function in this module is exchange.
Author: shivam kumar
Date: Nov,26,2022
'''
def before_space(s):
	'''Returns a copy of s up to,but not including, the first space

	Example:
	>>> before_space('5.432 INR')
	'5.432'
	>>> before_space('5.432  USD')
	'5.432'

	parameter s: the string to slice
	precondition: s is a string with at least one space'''

	end_last=s.find(' ')
	before=s[:end_last]
	return before



def after_space(s):
	'''Returns a copy of s after  the first space

	Example:
	>>> after_space('5.432 INR')
	'INR'
	>>> after_space('5.432  INR')
	' INR'

	parameter s: the string to slice
	precondition: s is a string with at least one space'''

	end_last=s.find(' ')
	after=s[end_last+1:]
	return after




def first_inside_quotes(s):
	'''Returns the first substring of s between two (double) quotes


    A quote character is one that is inside a string, not one that
    delimits it. We typically use single quotes (') to delimit a
    string if we want to use a double quote character (") inside of
    it.

    Example:
	>>> first_inside_quotes('A "B C" D')
	'B C'
	>>> first_inside_quotes('A "B C" D "E F" G ')
	'B C'


	because it only picks the first such substring

	parameter s: a string to search 
	precondition: s is a string containing at least two double quotes'''

	quote1=s.index('"')
	quote2=s.index('"',quote1+1)
	char=s[quote1+1:quote2]
	return char


def get_lhs(json):
	'''Returns the lhs value in the response to a currency query


    Given a JSON response to a currency query, this returns the
    string inside double quotes (") immediately following the
    keyword
    "lhs". For example, if the JSON is
    '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'
    then this function returns '1 Bitcoin' (not '"1 Bitcoin"').
    This function returns the empty string if the JSON response
    contains an error message.
    Parameter json: a json string to parse
    Precondition: json is the response to a currency query

	Example:
	>>> get_lhs('{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }')
	'1 Bitcoin'
	'''

	return json[12:20]

	
	# start=json.index(':')
	# end=json.index('"',start+3)
	# lhs=json[start+3:end]
	# return lhs


def get_rhs(json):
	'''Returns the rhs value in the response to a currency query


    Given a JSON response to a currency query, this returns the
    string inside double quotes (") immediately following the
    keyword
    "rhs". For example, if the JSON is
    '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'
    then this function returns '19995.85429186 Euros' (not
    '"38781.518240835 Euros"').
    This function returns the empty string if the JSON response
    contains an error message.
    Parameter json: a json string to parse
    Precondition: json is the response to a currency quer

	Example:
	>>> get_rhs('{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }')
	'19995.85429186 Euros'
	'''

	return json[-42:-15]
	




def has_error(json):
	'''
	Returns True if the query has an error; False otherwise.


    Given a JSON response to a currency query, this returns True if
    there
    is an error message. For example, if the JSON is
    '{ "lhs" : "", "rhs" : "", "err" : "Currency amount is invalid." }'
    then the query is not valid, so this function returns True (It
    does NOT return the message 'Currency amount is invalid.').
    Parameter json: a json string to parse
    Precondition: json is the response to a currency query
	Example:
	>>> has_error('{ "lhs":"2 Namibian Dollars", "rhs":"2 Lesotho Maloti","err":"" }')
	False
	>>> has_error('{ "lhs" : "", "rhs" : "", "err" : "Source currency code is invalid." }')
	True
	'''


	return len(json[-13:-4])>0 


	
if __name__=='__main__':
	import doctest
	doctest.testmod()





def query_website(old,new,amt):

	'''Returns a JSON string that is a response to a currency query.


    A currency query converts amt money in currency old to the
	currency new. The response should be a string of the form
	'{ "lhs":"<old-amt>", "rhs":"<new-amt>", "err":"" }'
	where the values old-amount and new-amount contain the value
	and name for the old and new currencies. If the query is
	invalid, both old-amount and new-amount will be empty, while
	"err" will have an error message.
	Parameter old: the currency on hand
	Precondition: old is a string with no spaces or non-letters
	Parameter new: the currency to convert to
	Precondition: new is a string with no spaces or non-letters
	Parameter amt: amount of currency to convert
	Precondition: amt is a float'''

	import requests
	json=(requests.get(f'http://cs1110.cs.cornell.edu/2022fa/a1?old={old}&new={new}&amt={amt}')).text
	return json  
	


def is_currency(code):
	'''

	Returns: True if code is a valid (3 letter code for a) currency It returns False otherwise.

	Parameter code: the currency code to verify
	Precondition: code is a string with no spaces or non-letters.'''

	amt=5.0
	return has_error(query_website(code,code,amt))




def exchange(old,new,amt):
	'''Returns the amount of currency received in the given exchange.


	In this exchange, the user is changing amt money in currency
	old to the currency new. The value returned represents the
	amount in currency new.
	The value returned has type float.
	Parameter old: the currency on hand
	Precondition: old is a string for a valid currency code
	Parameter new: the currency to convert to
	Precondition: new is a string for a valid currency code
	Parameter amt: amount of currency to conver
	precondition:amt is float'''

	 
	return before_space(get_rhs(query_website(old,new,amt)))


