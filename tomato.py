#!/usr/bin/python
from bs4 import BeautifulSoup
import sys
import urllib2
import re


def main(argv):
    celebrity_url = create_celebrity_url(argv)
    page = urllib2.urlopen(celebrity_url).read()
    soup = BeautifulSoup(page)
    #soup = BeautifulSoup(open('jessica-alba.html'))

    filmography_table = soup.find_all("table", id="filmographyTbl")[0]
    movies = filmography_table.find_all("tr")
    #tv = filmography_table [1].find_all("tbody")

    rated_movies = 0
    total_score = 0
    rotten = 0
    fresh = 0
    vfresh = 0
    lowest_score = 100
    highest_score = 0
    for movie in movies:
        score_spans = movie.find_all("span", {"class":"tMeterScore"})
        if len(score_spans) == 0:
            continue
        score_tag = score_spans[0]
        score_string = score_tag.contents[0]
        score = int(score_string[:-1])

        rated_movies+=1
        total_score+=score

        if score>highest_score:
            highest_score = score

        if score<lowest_score:
            lowest_score = score

        if score <= 60:
            rotten += 1
        elif score >= 60 and score < 75:
            fresh += 1
        elif score >= 75:
            vfresh += 1

    print "   Total: {0}".format(len(movies)-1) # Don't count the header row
    print "Reviewed: {0}".format(rated_movies)
    print "  Rotten: {0}".format(rotten)
    print "   Fresh: {0}".format(fresh)
    print " V.Fresh: {0}".format(vfresh)
    print "     Avg: {0}%".format(total_score/rated_movies)
    print "    High: {0}%".format(highest_score)
    print "     Low: {0}%".format(lowest_score)

def format_celebrity_name(celebrity_name_params):
    celebrity_name = ""
    for name in celebrity_name_params:
        n = re.sub("-", '', name)
        celebrity_name += n.lower() + "_"

    return celebrity_name[:-1]


def create_celebrity_url(celebrity_name_params):
    return "http://www.rottentomatoes.com/celebrity/" + format_celebrity_name(celebrity_name_params)


if __name__ == "__main__":
    main(sys.argv[1:])
