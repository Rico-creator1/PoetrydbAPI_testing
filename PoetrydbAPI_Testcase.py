import json
import unittest
import requests

class MyTestCase(unittest.TestCase):
    def test_baseURL_page(self):
        response = requests.get('https://poetrydb.org/')
        self.assertIn('PoetryDB is the world\'s first API for next generation internet poets', response.text)
        self.assertEqual(response.status_code, 200)

    # TC: Author API call Response 200 for the following endpoints (/author,/author/<author>,/author/<author>/author,/author/<author>:abs/author)
    def test_GET_author_list(self):
        response = requests.get('https://poetrydb.org/author')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('Ernest Dowson', response.text)
        self.assertIn('Shelley', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/author/Shelley')
        self.assertIn('"title":', response.text)
        self.assertIn('"author":', response.text)
        self.assertIn('"lines":', response.text)
        self.assertIn('"linecount":', response.text)
        self.assertIn('The Mask of Anarchy. Written on the Occasion of the Massacre at Manchester', response.text)
        self.assertIn('Percy Bysshe Shelley', response.text)
        self.assertNotIn('"A Ballad of Death",', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/author/william/author')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"author":', response.text)
        self.assertIn('William', response.text)
        self.assertIn('William Allingham', response.text)
        self.assertIn('William Cowper', response.text)
        self.assertNotIn('Ernest Dowson', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/author/Ernest Dowson:abs/author')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"author":', response.text)
        self.assertIn('Ernest Dowson', response.text)
        self.assertNotIn('William', response.text)
        self.assertNotIn('William Ernest Henley', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/author/Ernest Dowson/author,title,linecount')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title": "The Moon Maiden\'s Song",', response.text)
        self.assertIn('"author": "Ernest Dowson",', response.text)
        self.assertIn('"linecount": "16"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/author/Ernest Dowson/author,title,linecount.text')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('title', response.text)
        self.assertIn('author', response.text)
        self.assertIn('linecount', response.text)
        self.assertIn('The Moon Maiden\'s Song', response.text)
        self.assertIn('Ernest Dowson', response.text)
        self.assertIn('16', response.text)
        self.assertEqual(response.status_code, 200)

    def test_GET_search_nonexistingauthor(self):
        response = requests.get('https://poetrydb.org/author/nonexistentauthor')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('status":404', response.text)
        self.assertIn('reason":"Not found', response.text)
        self.assertEqual(response.status_code, 200)

   # TC: Response 200 for the following endpoints (/title, /titles, /title/<title>,/title/<title>/title,/title/<title>:abs/title,/title/<title>/<output field>,
   # <output field>,<output field>,/title/<title>/<output field>,<output field>,<output field>.<format>)
    def test_list_all_title(self):
        response = requests.get('https://poetrydb.org/title')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"A Ballad Of The Trees And The Master",', response.text)
        self.assertIn('"A Ballad of Burdens",', response.text)
        self.assertIn('The Moon Maiden\'s Song', response.text)
        self.assertIn('"Youth And Age"', response.text)
        self.assertEqual(response.status_code, 200)

    def test_list_all_titles(self):
        response = requests.get('https://poetrydb.org/titles')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"A Ballad Of The Trees And The Master",', response.text)
        self.assertIn('"A Ballad of Burdens",', response.text)
        self.assertIn('The Moon Maiden\'s Song', response.text)
        self.assertIn('"Youth And Age"', response.text)
        self.assertEqual(response.status_code, 200)

    def test_search_poem_bytitle(self):
        response = requests.get("https://poetrydb.org/title/Ozymandias")
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title":', response.text)
        self.assertIn('"author":', response.text)
        self.assertIn('"lines":', response.text)
        self.assertIn('"linecount":', response.text)
        self.assertIn('Ozymandias', response.text)
        self.assertIn('"Percy Bysshe Shelley",', response.text)
        self.assertIn('"I met a traveller from an antique land",', response.text)
        self.assertEqual(response.status_code, 200)

    def test_search_poemtitle_bytitle(self):
        response = requests.get("https://poetrydb.org/title/Ozymandias/title")
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title":', response.text)
        self.assertNotIn('"author":', response.text)
        self.assertNotIn('"lines":', response.text)
        self.assertNotIn('"linecount":', response.text)
        self.assertIn('Ozymandias', response.text)
        self.assertEqual(response.status_code, 200)

    def test_search_poemtitle_byexacttitle(self):
        response = requests.get("https://poetrydb.org/title/In spring and summer winds may blow:abs/title")
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title":', response.text)
        self.assertIn('"In spring and summer winds may blow"', response.text)
        self.assertNotIn('"author":', response.text)
        self.assertNotIn('"lines":', response.text)
        self.assertNotIn('"linecount":', response.text)
        self.assertEqual(response.status_code, 200)

    # search by title to retrieve specific poem's author,title, linecount.
    def test_get_poemtitle_byfilter(self):
        response = requests.get("https://poetrydb.org/title/Ozymandias/author,title,linecount")
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title": "Ozymandias",', response.text)
        self.assertIn('"author":', response.text)
        self.assertIn('"linecount":', response.text)
        self.assertIn('Percy Bysshe Shelley', response.text)
        self.assertIn('14', response.text)
        self.assertEqual(response.status_code, 200)

    # search by title to retrieve specific poem's title, line in text format.
        response = requests.get("https://poetrydb.org/title/Ozymandias/title,lines.text")
        self.assertTrue(len(response.text) > 0)
        self.assertIn('title', response.text)
        self.assertIn('lines', response.text)
        self.assertIn('Ozymandias', response.text)
        self.assertIn('Half sunk, a shattered visage lies, whose frown,', response.text)
        self.assertIn('\'My name is Ozymandias, king of kings:', response.text)
        self.assertIn('Of that colossal wreck, boundless and bare', response.text)
        self.assertEqual(response.status_code, 200)

    #test if API can handle response for invalid / non-existing title
    def test_GET_nonexistingtitle(self):
        response = requests.get('https://poetrydb.org/title/nonexistenttitle')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('status":404', response.text)
        self.assertIn('reason":"Not found', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/title/spring:abs/title')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('status":404', response.text)
        self.assertIn('reason":"Not found', response.text)
        self.assertEqual(response.status_code, 200)

    # TC: Response 200 for the following endpoints (/lines/<lines>,/lines/<lines>/<output field,
    # /lines/<lines>/<output field>,<output field>,<output field>, /lines/<lines>/<output field>,<output field>,<output field>.<format>
    def test_get_poem_byline(self):
        response = requests.get("https://poetrydb.org/lines/Latitudeless Place")
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title":', response.text)
        self.assertIn('"author":', response.text)
        self.assertIn('"linecount": "20"', response.text)
        self.assertIn('"linecount":', response.text)
        self.assertIn('Emily Dickinson', response.text)
        self.assertIn('"Traversed she though pausing",', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get("https://poetrydb.org/lines/Latitudeless Place/author") #get poem's author name
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"author":', response.text)
        self.assertIn('"author": "Emily Dickinson"', response.text)
        self.assertNotIn('"linecount"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get("https://poetrydb.org/lines/Latitudeless Place/author,title,linecount")  # search 'by line' to get poem's author,title,linecount
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title": "Now I knew I lost her --",', response.text)
        self.assertIn('"author": "Emily Dickinson",', response.text)
        self.assertIn('"linecount": "20"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get("https://poetrydb.org/lines/Latitudeless Place/author,title,linecount.text")  # search 'by line' to get poem's author,title,linecount (in text format)
        self.assertTrue(len(response.text) > 0)
        self.assertIn('title', response.text)
        self.assertIn('author', response.text)
        self.assertIn('linecount', response.text)
        self.assertIn('Now I knew I lost her --', response.text)
        self.assertIn('Emily Dickinson', response.text)
        self.assertIn('20', response.text)
        self.assertEqual(response.status_code, 200)

# Test if the APi can handle invalid / non-existing poem line.
    def test_GET_nonexistingline(self):
        response = requests.get('https://poetrydb.org/line/nonexistentline')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('status":"405"', response.text)
        self.assertIn('reason":"line input field not available. Only author, title, lines, linecount, and poemcount or random allowed."', response.text)
        self.assertEqual(response.status_code, 200)

    # TC: Response 200 for the following endpoints (/linecount/<linecount>, /linecount/<linecount>/<output field>, /linecount/<linecount>/<output field>,<output field>,<output field>
    # /linecount/<linecount>/<output field>,<output field>.<format>
    def test_get_poem_bylinecount(self):
            response = requests.get("https://poetrydb.org/linecount/3") # display all poem with linescount=3
            self.assertTrue(len(response.text) > 0)
            self.assertIn('"title":', response.text)
            self.assertIn('"author":', response.text)
            self.assertIn('"lines":', response.text)
            self.assertIn('"linecount": "3"', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get("https://poetrydb.org/linecount/3/title") # display all the poem's title (only) of all poems with linescount=3
            self.assertTrue(len(response.text) > 0)
            self.assertIn('"title":', response.text)
            self.assertIn('"title": "Fragment: The Deserts of Dim Sleep"', response.text)
            self.assertNotIn('"author":', response.text)
            self.assertNotIn('"lines":', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get("https://poetrydb.org/linecount/51/author,title,linecount") # display all the poem's title,author,linecount (only) of all poems with linescount=51
            self.assertTrue(len(response.text) > 0)
            self.assertIn('"title":', response.text)
            self.assertIn('"author":', response.text)
            self.assertIn('"linecount":', response.text)
            self.assertIn('"title": "On the Death of the Rev. Dr. Sewell",', response.text)
            self.assertIn('"author": "Phillis Wheatley",', response.text)
            self.assertIn('"linecount": "51"', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get(
                "https://poetrydb.org/linecount/39/author,title.text")  # display all the poem's title,author (only) of all poems with linescount=31 in test format
            self.assertTrue(len(response.text) > 0)
            self.assertIn('title', response.text)
            self.assertIn('author', response.text)
            self.assertIn('My Boy Hobbie O', response.text)
            self.assertIn('George Gordon, Lord Byron', response.text)
            self.assertNotIn('"title":', response.text)
            self.assertNotIn('"author":', response.text)
            self.assertEqual(response.status_code, 200)

    # TC: Response 200 for the following endpoints (<input field>,poemcount/<search term>;<poemcount>, <input field>,poemcount/<search term>;<poemcount>/<output field>,
    #<input field>,poemcount/<search term>;<poemcount>/<output field>,<output field>,<output field>, <input field>,poemcount/<search term>;<poemcount>/<output field>,<output field>.<format>
    def test_get_poem_bypoemcount(self):
        response = requests.get(
            "https://poetrydb.org/author,poemcount/Dickinson;2")  # display all the poem's of the author with limit =2 <poemcount>
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title": "Not at Home to Callers",', response.text)
        self.assertIn('"author": "Emily Dickinson",', response.text)
        self.assertIn('"Wishing you Good Day --"', response.text)
        self.assertIn('"linecount": "4"', response.text)
        self.assertIn('"title": "Defrauded I a Butterfly --",', response.text)
        self.assertIn('"author": "Emily Dickinson",', response.text)
        self.assertIn('"Defrauded I a Butterfly --",', response.text)
        self.assertIn('"linecount": "2"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/author,poemcount/Dickinson;2/title")  # display all the author's poem title with limit =2
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title": "Not at Home to Callers"', response.text)
        self.assertIn('"title": "Defrauded I a Butterfly --"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/author,poemcount/Dickinson;2/author,title,linecount")  # display all the author's poem title,author,linecount with limit =2
        self.assertTrue(len(response.text) > 0)
        self.assertIn('"title": "Not at Home to Callers"', response.text)
        self.assertIn('"author": "Emily Dickinson",', response.text)
        self.assertIn('"linecount": "4"', response.text)
        self.assertIn('"title": "Defrauded I a Butterfly --"', response.text)
        self.assertIn('"author": "Emily Dickinson",', response.text)
        self.assertIn('"linecount": "2"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/author,poemcount/Dickinson;2/author,title.text")  # display all the author's poem title,author with limit =2 in text form
        self.assertTrue(len(response.text) > 0)
        self.assertIn('title', response.text)
        self.assertIn('author', response.text)
        self.assertNotIn('"title": "Not at Home to Callers"', response.text)
        self.assertNotIn('"title": "Defrauded I a Butterfly --"', response.text)
        self.assertEqual(response.status_code, 200)

    # TC: Response 200 for the following endpoints (/random, /random/<random count>, /random/<random count>/<output field>
    # /random/<random count>/<output field>,<output field>,<output field>, /random/<random count>/<output field>,<output field>.<format>
    def test_getpoem_byrandom(self):
        response = requests.get(
            "https://poetrydb.org/random")  # display one random poem
        self.assertTrue(len(response.text) > 0)
        json_response = json.loads(response.text)
        response_array_count = len(json_response)
        self.assertEqual(response_array_count,1)
        self.assertIn('title', response.text)
        self.assertIn('"author"', response.text)
        self.assertIn('"lines"', response.text)
        self.assertIn('"linecount"', response.text)
        self.assertNotIn('},', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/random/3")  # display three random poem
        self.assertTrue(len(response.text) > 0)
        json_response = json.loads(response.text)
        response_array_count = len(json_response)
        self.assertEqual(response_array_count,3)
        self.assertIn('title', response.text)
        self.assertIn('"author"', response.text)
        self.assertIn('"lines"', response.text)
        self.assertIn('"linecount"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/random/3/title")  # search 3 random poem title
        self.assertTrue(len(response.text) > 0)
        json_response = json.loads(response.text)
        response_array_count = len(json_response)
        self.assertEqual(response_array_count,3)
        self.assertIn('"title"', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/random/3/author,title,linecount")  # display title, author, linecount of the three random poem
        self.assertTrue(len(response.text) > 0)
        json_response = json.loads(response.text)
        response_array_count = len(json_response)
        self.assertEqual(response_array_count, 3)
        self.assertIn("title", response.text)
        self.assertIn("author", response.text)
        self.assertIn("linecount", response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            "https://poetrydb.org/random/3/author,title.text")  # display title, author, linecount of the three random poem in text format
        self.assertTrue(len(response.text) > 0)
        self.assertIn("title\n", response.text)
        self.assertIn("author\n", response.text)
        self.assertNotIn('},', response.text)
        self.assertEqual(response.status_code, 200)

    # Test if the APi can handle invalid / invalid endpoint.
    def test_GET_poem_byinvalidendpoint(self):
        response = requests.get('https://poetrydb.org/invalidendpoint')
        self.assertTrue(len(response.text) > 0)
        self.assertIn('status":"405"', response.text)
        self.assertIn(
                'reason":"invalidendpoint list not available. Only author and title allowed."',
            response.text)
        self.assertEqual(response.status_code, 200)

    # TC: Response 200 for the following endpoints (/<input field>,<input field>/<search term>;<search term>,
    #/<input field>,<input field>,<input field>/<search term>;<search term>;<search term>, /<input field>,<input field>/<search term>:abs;<search term>
    #/<input field>,<input field>,<input field>,<input field>/<search term>;<search term>;<search term>;<search term>,
    #/<input field>,<input field>/<search term>;<search term>/<output field>,
    #/<input field>,<input field>/<search term>;<search term>/<output field>[.<format>]
    def test_getpoem_bycombination(self):
            response = requests.get(
                "https://poetrydb.org/title,random/Sonnet;3")  # display 3 random poem with filter 'Sonnet;3'. this will display 3 random Sonnet poem
            self.assertTrue(len(response.text) > 0)
            json_response = json.loads(response.text)
            response_array_count = len(json_response)
            self.assertEqual(response_array_count, 3)
            self.assertIn('title', response.text)
            self.assertIn('"author"', response.text)
            self.assertIn('"lines"', response.text)
            self.assertIn('"linecount"', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get(
            "https://poetrydb.org/title,author,linecount/Winter;Shakespeare;18")  # display 3 random poem with filter 'Winter;Shakespeare;18'.
            self.assertTrue(len(response.text) > 0)                                   #  this will display 3 random Shakespeare's poem with 18 linecount and contains string 'Winter' in the title
            json_response = json.loads(response.text)
            response_array_count = len(json_response)
            self.assertEqual(response_array_count, 3)
            self.assertIn('title', response.text)
            self.assertIn('"author"', response.text)
            self.assertIn('"lines"', response.text)
            self.assertIn('"linecount"', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get(
                "https://poetrydb.org/title,author/Winter:abs;William%20Shakespeare")  # display poem with filter 'Winter;Shakespeare;18'.
            self.assertTrue(len(response.text) > 0)                                     # this will display Shakespeare's poem with exact string 'Winter' in the title
            json_response = json.loads(response.text)
            response_array_count = len(json_response)
            self.assertEqual(response_array_count, 1)
            self.assertIn('"title": "Winter"', response.text)
            self.assertIn('"author": "William Shakespeare",', response.text)
            self.assertIn('"lines"', response.text)
            self.assertIn('"linecount"', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get(
                "https://poetrydb.org/title,author,linecount,poemcount/Winter;William Shakespeare;14;1")  # this will display one Shakespeare's poem with linecount=14 and string 'Winter' in the title
            self.assertTrue(len(response.text) > 0)
            json_response = json.loads(response.text)
            response_array_count = len(json_response)
            self.assertEqual(response_array_count, 1)
            self.assertIn('"title"', response.text)
            self.assertIn('winter', response.text)
            self.assertIn('"author": "William Shakespeare",', response.text)
            self.assertIn('"lines"', response.text)
            self.assertIn('"linecount": "14"', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get(
                "https://poetrydb.org/title,author/Winter;William Shakespeare/title")  # this will display all Shakespeare's poem with string 'Winter' or winter in the title
            self.assertTrue(len(response.text) > 0)
            json_response = json.loads(response.text)
            response_array_count = len(json_response)
            self.assertGreater(response_array_count, 0)
            self.assertIn('"title"', response.text)
            self.assertIn('winter', response.text)
            self.assertEqual(response.status_code, 200)

            response = requests.get(
                "https://poetrydb.org/title,author/Winter;William Shakespeare/title.text")  # this will fetch all Shakespeare's poem with string 'Winter' or winter in the title, displays 'title' only.
            self.assertTrue(len(response.text) > 0)
            self.assertIn('title', response.text)
            self.assertIn('winter', response.text)
            self.assertEqual(response.status_code, 200)

    def test_search_byauthor_with_combination_of_valid_andinvalid_outputfields(self):
        response = requests.get('https://poetrydb.org/author/Shakespeare/wrong;lines')
        self.assertIn('405', response.text)
        self.assertIn('reason', response.text)
        self.assertIn('wrong;lines output field not available. Only author, title, lines, and linecount allowed', response.text)
        self.assertEqual(response.status_code, 200)

        response = requests.get('https://poetrydb.org/author/Shakespeare/wrong')
        self.assertIn('405', response.text)
        self.assertIn('reason', response.text)
        self.assertIn('wrong output field not available. Only author, title, lines, and linecount allowed.', response.text)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
