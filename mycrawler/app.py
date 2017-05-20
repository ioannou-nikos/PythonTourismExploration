from searches import Searches
import csv
import time
import sys

# This list holds the names of the functions to be called
s_functions = ['selenium_google', 'selenium_yahoo', 'bing', 'tripadvisor', 'booking', 'twitter', 'facebook', 'youtube']
s_functions = ['selenium_bing', 'selenium_yahoo', 'selenium_google']


# Read comma separated line into a list
def read_list(filename=None):
    if filename is None:
        return []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return list(reader)


if __name__ == "__main__":
    Searches.facebook("")
    sys.exit()

    locations = open("locations.txt").readlines()
    with open("results.csv", "w") as fout:
        s = Searches()
        fout.write("source,phrase,count\n")
        try:
            for sf in s_functions:
                r = getattr(Searches, sf)(locations)
                print(r)
                fout.write(r)
        except Exception:
            print("Major Problem")
        finally:
            fout.close()
    sys.exit()

    phrases = read_list(filename='phrases.txt')[0]  # Read the phrases
    print(len(locations))
    print(phrases)
    s = Searches()  # Create a Searches object
    final_results = "source,place,phrase,count\n"
    loc_limit = 200
    loc_counter = 0
    for place in locations:  # Iterate through locations
        loc_counter += 1
        if loc_counter > loc_limit:
            break
        for phrase in phrases: # Iterate through phrases
            for sf in s_functions:  # Iterate through all the functions
                if phrase.endswith(' '):
                    search_phrase = phrase.strip() + ' ' + place.strip()
                elif phrase.strip() == '-':
                    search_phrase = place.strip()
                else:
                    search_phrase = place.strip() + ' ' + phrase.strip()
                search_phrase = search_phrase.lower()
                print(search_phrase)
                count = getattr(Searches, sf)(search_phrase)
                final_results += "%s,%s,%s,%s\n" % (sf, place.strip(), phrase.strip(), count)
                #time.sleep(10)
    print("\n\n\n")
    print("================== FINAL RESULTS ======================")
    print(final_results)
    with open('results.csv', 'w') as fout:
        fout.write(final_results)
        fout.close()
