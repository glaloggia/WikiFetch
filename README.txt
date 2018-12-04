Readme.txt

Word Frequency Assigment.
*************************

--Content--
1.- Files.
2.- Description.
3.- How to use it.
4.- How to test it.
5.- Scope.
 

1.- Files.

- WikiFetch.py
  This module includes the class WikiFetch which is the main one of this project.

- launcher.py
  This module includes a simple example of how to use the class described before.

- Tests.py
  This module includes all the testing rutines for every one of the methods 
  developed for this project.
  
- readme.txt
  This document.


2.- Description.

The language of choice for this development was Python. There is no third-party
libraries used in the code, just modules from the Standard Python Library.
As Python is an interpreted language there is no need of compile the code, but
is advisable to run in a Python 3.6.3 environment which was the version I used it
to write it.


3.- How to use it.

In order to use this library it is necessary to create an instance of the class
"WikiFetch".

newObject = WikiFetch()

Then call the public method "scrap" with the parameters: page_id and n.
	- page_id: It is the id of the wikipedia page that will be downloaded.
	- n: It is the number of results that are going to be shown.

newObject.scrap(page_id,n)

The result is printed in the console screen.

Example:
newObject = WikiFetch()
newObject.scrap(21721040,5)

This is the output:

URL: https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids=21721040&explaintext&format=json

Title: Stack Overflow

Top 5 words:

- 20 questions
- 15 overflow
- 13 stack, that
- 12 users
- 8 question


4.- How to test it.

All the unit tests are located in the file Tests.py
In order to run them:
	- Open a console
	- type "python -m unittest" and hit Enter

One test called "test_noConnection" involved internet connection issues, so need to be executed offline, otherway, 
It will fail the assertion.

All the other tests can be executed in a normal python 3.6.3 environment.



5.- Scope.

The scope of this library is the analysis of alphabetical words and that concept
don't include the following examples:

Inv3nti0n5:
Words with numbers in the middle.

Hyphened-words:
Complex words joined with a hyphen.

Inc@ns!stences:
NonAlphabetical characters in the word.

English Contractions:
'd
's
't

All the item described above are skipped by the algorithm.