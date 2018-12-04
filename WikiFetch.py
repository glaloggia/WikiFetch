import json, urllib.request

#Customized Exceptions
class MissingPage(Exception):
    pass
class NotEnoughRows(Exception):
    pass
class ConnError(Exception):
    pass

#Main Class - Wikipedia Article Fetcher
class WikiFetch:
    #Constructor.
    def __init__(self):
        pass

    #_getJson this private method is used to get the json data from the given url
    #Parameters:
    # page_id: Wikipedia API Page Id
    #Exceptions - This method throw the following exceptions:
    # MissingPage When It's not possible to retrieve the information.
    # ConnectionError When It's used without an internet connection.
    def _getJson(self,page_id):


        if not str(page_id).isalnum():
            raise MissingPage()

        wikipediaUrl = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids=" + str(page_id) + "&explaintext&format=json"        

        try:
            #Connect with the remote server            
            with urllib.request.urlopen(wikipediaUrl) as url:

            #Get the json downloaded and parsed into a dictionary
                data = json.loads(url.read().decode())
        except:
            raise ConnError()


        #When a requested page does not exist, the size of the dictionary that the query returns is 2. So I used that value in my logic.
        if len(data) == 2 :
            raise MissingPage()
    
        #Get the page URL, title and content    
        result={}        
        result['url']       = wikipediaUrl
        result['title']     = data['query']['pages'][str(page_id)]['title']
        result['extract']   = data['query']['pages'][str(page_id)]['extract']

        return result

    #_processData this private method is used to parse the json data and convert it into a better structure
    #Parameters:
    # extract: A string contains the content of the wikipedia page.
    #Exceptions - This method throw the following exceptions:
    #AttributeError When the input is null.
    def _processData(self,extract):


        #Remove escape sequences.
        lines = extract.splitlines()
        #Create a new string without special characters.
        joinedLines = " ".join(lines)
        #Separate the words inbetween spaces.
        words = joinedLines.split(' ')        


        # Convert every word to lower case for easy comparison
        wordsInLowerCase = []

        for word in words:
            wordsInLowerCase.append(word.lower())

        # Sort the lower case list
        wordsInLowerCaseSorted = sorted(wordsInLowerCase)            

        #Filter from the array words smaller than 4 characters and non-alphabetical ones.
        wordsFiltered = []
        for word in wordsInLowerCaseSorted:

            if len(word) > 3 and word.isalpha():

                wordsFiltered.append(word)

            else:

                word = word.replace(":","")
                word = word.replace(";","")
                word = word.replace(",","")
                word = word.replace(".","")
                word = word.replace("'s","")
                word = word.replace("'d","")
                word = word.replace('"',"")
                word = word.replace("\\","")
                word = word.replace("?","")
                word = word.replace("!","")                
                word = word.replace("(","")                
                word = word.replace(")","")                

                if len(word) > 3 and word.isalpha():
                    wordsFiltered.append(word)
            
            #Check if any other punctuation symbol is triggering a nonAlpha reaction within the isalpha() method.
            #Example: "Example-" is not alpha because of the "-"
            if len(word) > 3 and not word.isalpha():
                #Remove the last character and check if it is still nonAlpha after that.                    
                newWord = word[:-1]
                if len(newWord) > 3 and newWord.isalpha():
                    wordsFiltered.append(newWord)

        #Sort again after filter
        wordsFiltered = sorted(wordsFiltered)

        #Initialize counters
        statistics={}    
        counter = 0
        iterator1 = 0
        iterator2 = 0

        #This loop creates a dictionary called statistics with:
        #Key: Word
        #Value: Amount of repetitions
        while iterator2 < len(wordsFiltered) and iterator1 < len(wordsFiltered):
            if wordsFiltered[iterator1] == wordsFiltered[iterator2]:
                counter = counter + 1
                iterator1 = iterator1 + 1
                
                if iterator1 == len(wordsFiltered):
                    statistics[wordsFiltered[iterator2]] = counter    
            else:
                statistics[wordsFiltered[iterator2]] = counter
                counter = 0
                iterator2 = iterator1

                if iterator2 == len(wordsFiltered):
                    statistics[wordsFiltered[iterator2]] = 1

        #Sort the statistics dictionary by value in descending order            
        keysList = sorted(statistics,key=statistics.get,reverse=True)

        statisticsGrouped = {}

        #word
        prevElement = keysList[0]

        #frequency
        prevValue = statistics[prevElement]

        #list of words
        finalList = []

        #This loop creates a new dictionary with:
        #Key: The amount of repetitions of one or more words.
        #Value: A list of words with the same amount of repetitions.
        #This dictionary is an invertion of the previous in order to reagroup the words for an easy printing.
        for element in keysList:

            if statistics[element] == prevValue:
                finalList.append(element)
                if len(keysList) == 1:
                    statisticsGrouped[prevValue] = finalList    
            else:
                statisticsGrouped[prevValue] = finalList
                finalList = []
                finalList.append(element)
                prevElement = element
                prevValue = statistics[element]
                if prevValue == 1 and prevElement == keysList[-1]:
                    statisticsGrouped[prevValue] = finalList

        return statisticsGrouped

    #_printResult this private method is usedd to print the result
    #Parameters:
    # n: the number of results to be printed.
    # statisticsGrouped: a dictionary with frequency of words as key and lists of words with that frequency as values.
    # title: the title of the printed result.
    # url: the article's url
    #Exceptions - This method throw the following exceptions:
    #AttributeError When the dictionary input is null.
    #NotEnoughRows  When the number of records asked is more than the available.
    def _printResult(self,n,statisticsGrouped,title,url):
        
        if n > len(statisticsGrouped):
            raise NotEnoughRows()        

        keys = statisticsGrouped.keys()        

        print()

        print("URL:",url)
        
        print()

        print("Title:",title)

        print()

        print("Top",n,"words:")

        print()

        iterator = 0

        for key in keys:

            if iterator >= n:
                break

            line = "- " + str(key) + " "
            for counter in range(len(statisticsGrouped[key])):
                #The following if statement fix the comma after the last word in the line to be printed
                if counter == len(statisticsGrouped[key])-1:
                    line = line + statisticsGrouped[key][counter] + " "
                else:
                    line = line + statisticsGrouped[key][counter] + ", "
            print(line)

            iterator = iterator + 1

        print() 

    #scrap this is the main method in charge of call all other methods.
    #Parameters:
    # n: the numbers of results to be printed.
    # page_id: Wikipedia API Page id, a positive non-zero integer existing in the wikipedia database. 
    def scrap(self,page_id,n):

        try:

            jsonData = self._getJson(page_id)

            extract = jsonData['extract']

            statisticsGrouped = self._processData(extract)
            
            self._printResult(n,statisticsGrouped,jsonData['title'],jsonData['url'])

        except MissingPage:
            print("ERROR: It is not possible to retrieve the page requested.")
        except ConnError:
            print("ERROR: There is a problem with the internet connection.")
        except AttributeError:
            print("ERROR: There was an internal error. Please try again with other page-id or contact Support.")
        except NotEnoughRows:
            print("ERROR: You are asking for more records than the available.")
        except:
            print("ERROR: Unexpected error. Please contact Support.")