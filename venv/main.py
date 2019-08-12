import bs4
from urllib.request import urlopen as u_req
from bs4 import BeautifulSoup as soup
from venv.clue import Clue
import pickle

# clue list for holdings clues
clue_list = []

for x in range(1, 6095):

    print(x)

    # Looks like the last game in the archive is 6095
    myurl = 'http://www.j-archive.com/showgame.php?game_id=' + str(x)

    # opening connection grabbing page
    uClient = u_req(myurl)
    page_html = uClient.read()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    # grabs all clues
    clues = page_soup.findAll("td",{"class" : "clue"})

    # grabs all categories
    categories = page_soup.findAll("td",{"class" : "category_name"})
    parsed_categories = []

    # parses cateoories for pure text
    for category in categories:
        parsed_category = ""

        for char in category:
            # TODO Figure out how to get tagged categories
            if isinstance(char, bs4.Tag):
                continue
            parsed_category += char

        parsed_categories.append(parsed_category)


    # i variable used to count daily double/final
    i = 0

    # row and column variables to find category
    x = 0
    y = 0

    # parse every clue for clue text
    for clue in clues:
        clue_text = clue.find("td", {"class" : "clue_text"})
        clue_value = clue.find("td", {"class" : "clue_value"})

        # skip clue if none type for whatever reason lol (looks like there are missing clues in the archive)
        if clue_text is None:
            if x == 5:
                x = 0
                y = y + 1
            else:
                x = x + 1


            continue

        # Parsing for correct response

        # Final jeopardy: y should be 10
        if y == 10:
            # Relevant text will be slightly different
            final_round = page_soup.find("table", {"class" : "final_round"})
            revelant_text = final_round.tr.td.div["onmouseover"]

        elif clue.table.tr.td.div is not None:
            revelant_text = clue.table.tr.td.div["onmouseover"]

        # tracker will store all of the characters in each string thus far
        # place will keep track of how far along we are in the relevant text
        tracker = ""
        place = 0
        right_place = False
        correct_response =""

        for char in revelant_text:
            # check if none
            if revelant_text is None:
                break

            # if we haven't gotten to the right place in the string yet...
            if not right_place:
                tracker += char

                if len(tracker) > 42:
                    possible = tracker[-10:]

                    # Relevant text for final jeopardy looks slightly different
                    if y == 10 and possible == "esponse\\\">":
                        right_place = True

                    elif possible == "response\">":
                        right_place = True

            else:
                # if we've finished gathering the response...
                # Need to address special case
                if char == '<' and len(correct_response) != 0:
                    break
                else:
                    correct_response += char

        # remove <i> from correct response if necessary
        if correct_response[:3] == "<i>":
            correct_response = correct_response[3:]


        # declaration of parsed variable
        parsed = ""
        parsed_value = ""
        cat = ""

        # use x and y to determine category
        # if single jeopardy
        if y < 5:
            if x == 0:
                cat = parsed_categories[0]
            if x == 1:
                cat = parsed_categories[1]
            if x == 2:
                cat = parsed_categories[2]
            if x == 3:
                cat = parsed_categories[3]
            if x == 4:
                cat = parsed_categories[4]
            if x == 5:
                cat = parsed_categories[5]
        # else if double jeopardy
        elif y < 10:
            if x == 0:
                cat = parsed_categories[6]
            if x == 1:
                cat = parsed_categories[7]
            if x == 2:
                cat = parsed_categories[8]
            if x == 3:
                cat = parsed_categories[9]
            if x == 4:
                cat = parsed_categories[10]
            if x == 5:
                cat = parsed_categories[11]
        # else if final jeopardy
        else:
            cat = parsed_categories[12]


        # TODO: Handle visual clues
        # ignore line breaks
        # parse clue text for pure text
        for s in clue_text:
            if isinstance(s, bs4.Tag):
                # TODO Figure out how to get pure text from tag
                continue

            parsed += s

        # parse value text for pure text
        # check if daily double or final jeopardy
        if clue_value is not None:
            for s in clue_value:
                parsed_value += s
        elif i < 3:
            parsed_value = "Daily Double"
            i = i + 1
        else:
            parsed_value = "Final Jeopardy"


        # create new clue with parsed info and add to list
        new_clue = Clue(parsed, parsed_value, cat, correct_response)
        clue_list.append(new_clue)

        # increment x and y variables
        if x == 5:
            x = 0
            y = y + 1
        else:
            x = x + 1


clue_file = open(r'/home/seamus/PycharmProjects/Bunker/clues.pkl', 'wb')
pickle.dump(clue_list, clue_file)
clue_file.close()



