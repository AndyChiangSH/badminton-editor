from typing import Tuple, Dict, Any
from uuid import UUID
import time
from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup


#### Website 
WEBSITE = "https://bwf.tournamentsoftware.com"

#####   Selectors for different web pages   #####

NAME_SELECTORE_ON_FIND_PAGE             = "h5 > a"
MEMBER_ID_SELECTOR_ON_FIND_PAGE         = "h5 > span"

NAME_SELECTORE_ON_PROFILE_PAGE          = "h2 > span.nav-link.media__link > span"
COUNTRY_SELECTOR_ON_PROFILE_PAGE        = "small > a > span.nav-link__value"
DETAIL_SELECTOR_ON_PROFILE_PAGE         = "dl.list--bordered > div.list__item"

CAPTIONS_SELECTOR_ON_RANKING_PAGE       = "table.table--new.table--bordered > caption"
CONTENTS_SELECTOR_ON_RANKING_PAGE       = "table.table--new.table--bordered > tbody"

PLAYER1_WIN_SELECTOR_ON_H2H_PAGE        = "#h2h-team1wins"
PLAYER2_WIN_SELECTOR_ON_H2H_PAGE        = "#h2h-team2wins"
MATCHES_SELECTOR_ON_H2H_PAGE            = "#tab_matchescontent > ol div.match"
MATCHES_INFO_SELECTOR_ON_H2H_PAGE       = "ul.match__header-title > li"
MATCHES_STATISTICS_SELECTOR_ON_H2H_PAGE = "div.match__result > ul > li.points__cell"

NAME_SELECTOR_ON_TOURNAMENT_PAGE        = "h4 > a.media__link > span.nav-link__value"
LINK_SELECTOR_ON_TOURNAMENT_PAGE        = "h4 > a.media__link"
PLACE_SELECTOR_ON_TOURNAMENT_PAGE       = "small.media__subheading > span > span.nav-link__value"
TIME_SELECTOR_ON_TOURNAMENT_PAGE        = "small.media__subheading--muted > span > span.nav-link__value"
MATCHES_SELECTOR_ON_TOURNAMENT_PAGE     = "ol.match-group"

SELECTOR_ON_WINNER_PAGE                 = "#content > div.columncontainer > div > table > tbody > tr > td"

######  End of selectors    #####

"""
Access URL and get the cookies => for tournament and h2h page
"""
def get_cookies(url: str, delay=0.2):
    response = requests.get( 
        url, 
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        },
    )

    # sleep for a while
    time.sleep(delay)
    
    if response.status_code == 200:
        return response.cookies
    
    raise Exception("The URL is error or the crawler is classified as a robot!!")

"""
access url and return the html content
"""
def access_url(url: str, delay=0.2, cookies=None) -> str:

    response = requests.get( 
        url, 
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        },
        cookies=cookies
    )

    # sleep for a while
    time.sleep(delay)
    
    if response.status_code == 200:
        return response.text
        
    raise Exception("The URL is error or the crawler is classified as a robot!!")


def crawl_player_page_by_id(uuid: 'UUID') -> Dict[str, Any]:
    url = f"{WEBSITE}/player-profile/{str(uuid)}"
    html = access_url(url)
    
    soup = BeautifulSoup(html, 'html5lib')
    detail_tags = soup.select(DETAIL_SELECTOR_ON_PROFILE_PAGE)
    player_name_tag = soup.select(NAME_SELECTORE_ON_PROFILE_PAGE)[0]
    country_tag = soup.select(COUNTRY_SELECTOR_ON_PROFILE_PAGE)[0]

    interest_detail_processors = {
        "Height": lambda text: int(text.strip().split()[0]),
        "Year of birth": lambda text: int(text.strip()),
        "Play R or L": lambda text:  "R" if text.strip() == "Right handed" else "L"
    }

    result = {
        "country": country_tag.text.strip(),
        "name": player_name_tag.text.strip()
    }

    for detail_tag in detail_tags:
        name = detail_tag.dt.text.strip()
        if name in interest_detail_processors:
            value = interest_detail_processors[name](detail_tag.dd.text)
            result[name] = value

    return result
    
    
def crawl_ranking_page_by_id(uuid: 'UUID', target_ranking_name="BWF World Rankings") -> Dict[str, Any]:
    url = f"{WEBSITE}/player-profile/{str(uuid)}/ranking"
    html = access_url(url)
    
    soup = BeautifulSoup(html, 'html5lib')
    caption_tags = soup.select(CAPTIONS_SELECTOR_ON_RANKING_PAGE)
    content_tags = soup.select(CONTENTS_SELECTOR_ON_RANKING_PAGE)

    for caption_tag, content_tag in zip(caption_tags, content_tags):
        ranking_name = caption_tag.a.text.strip()
        date = datetime.strptime(caption_tag.span.text.strip(), "%m/%d/%Y")
        category = content_tag.a.text.strip()
        ranking = int(content_tag.td.a.text.strip())

        if ranking_name == target_ranking_name:
            return {
                "ranking_name": target_ranking_name,
                "category": category,
                "ranking": ranking,
                "update_date": date
            }
    raise Exception("No BWF Rankings")

def crawl_tournament_page_by_name(player_name: str) -> Dict[str, Any]:

    cookies = get_cookies(WEBSITE)

    uuid, _ = crawl_find_page_by_name(player_name)

    url = f"{WEBSITE}/player-profile/{str(uuid)}/tournaments"
    html = access_url(url, cookies=cookies)

    soup = BeautifulSoup(html, "html5lib")
    
    tournament_name = soup.select(NAME_SELECTOR_ON_TOURNAMENT_PAGE)[0].text.strip()
    link = soup.select(LINK_SELECTOR_ON_TOURNAMENT_PAGE)[0]["href"].strip()

    place = soup.select(PLACE_SELECTOR_ON_TOURNAMENT_PAGE)[0].text.split('|')[1].strip()
    start_time, end_time = tuple( soup.select(TIME_SELECTOR_ON_TOURNAMENT_PAGE)[0].text.strip().split('to') )

    last_match_tags = soup.select(MATCHES_SELECTOR_ON_TOURNAMENT_PAGE)[0]
    last_match_tags = last_match_tags.select("li > div.match")

    matches = []

    # for match_tag in last_match_tags:
    #     match_result = dict()
    #     match_result["name"] = match_tag.select("div.match__header span.nav-link__value")[0].text.strip()
    #     match_result["lasting"] = match_tag.select("div.match__header-aside time")[0].text.strip()
    #     match_result["date"] = match_tag.select("div.match__footer span.nav-link__value")[0].text.strip()
    #     match_result["place"] = match_tag.select("div.match__footer span.nav-link__value")[-1].text.strip()
    #     match_result["opponent"] = match_tag.select("div.match__body span.match__row-title-value-content a span")[-1].text.strip()
        
    #     score_tags = match_tag.select("div.match__body ul.points li")
    #     for round, i in enumerate(range(0, len(score_tags), 2)):
    #         match_result[f"round_{round+1}"] = score_tags[i].text.strip() + ":" + score_tags[i+1].text.strip()

    #     matches.append(match_result)

    start_time = start_time.strip()
    end_time = end_time.strip()

    winner_url = WEBSITE + link.replace("tournament", "winners.aspx")
    
    html = access_url(winner_url)
    soup = BeautifulSoup(html, "html5lib")
    rank_and_name_tags = soup.select(SELECTOR_ON_WINNER_PAGE)
    player_name = player_name.lower()

    rank = 0
    for i in range(0, len(rank_and_name_tags), 2):
        name = rank_and_name_tags[i+1].text.strip().lower()
        if player_name in name:
            rank = rank_and_name_tags[i].text.strip()
            break

    return {
        "name": tournament_name,
        "place": place,
        "start-date": start_time,
        "end-date": end_time,
        "rank": rank,
        "matches": matches,
    }
    

def crawl_h2h_page_by_id(player1_member_id: int, player2_member_id: int) -> Dict[str, Any]:
    
    cookies = get_cookies(WEBSITE)
    url = f"{WEBSITE}/head-2-head?OrganizationCode=209B123F-AA87-41A2-BC3E-CB57133E64CC&T1P1MemberID={player1_member_id}&T2P1MemberID={player2_member_id}"

    html = access_url(url, cookies=cookies)

    if len(html) == 0:
        return dict()
    
    soup = BeautifulSoup(html, "html5lib")
    win_count1 = int( soup.select(PLAYER1_WIN_SELECTOR_ON_H2H_PAGE)[0].text )
    win_count2 = int( soup.select(PLAYER2_WIN_SELECTOR_ON_H2H_PAGE)[0].text )
    match_tags = soup.select(MATCHES_SELECTOR_ON_H2H_PAGE)


    category_mapping = {
        "MS": "Men's Singles", "WS": "Women's Singles",
        "MD": "Men's Doubles", "WD": "Women's Doubles",
        "XD": "Mixed Doubles"
    }
    latest_match_info = dict()

    if len(match_tags) != 0:
        latest_match_tag = match_tags[0]
        info_tag = latest_match_tag.select(MATCHES_INFO_SELECTOR_ON_H2H_PAGE)

        latest_match_info["name"] = info_tag[0].text.strip()
        latest_match_info["category"] = category_mapping[info_tag[1].text.strip()]
        latest_match_info["type"] = info_tag[2].text.strip()
        
        score_tags = latest_match_tag.select(MATCHES_STATISTICS_SELECTOR_ON_H2H_PAGE) 

        for round, i in enumerate(range(0, len(score_tags), 2)):
            latest_match_info[f"round_{round+1}"] = score_tags[i].text.strip() + ":" + score_tags[i+1].text.strip()

        latest_match_info["lasting"] = latest_match_tag.time.text.strip()
    

    return {
        "player1-win": win_count1,
        "player2-win": win_count2,
        "match-details": latest_match_info
    }

def crawl_find_page_by_name(player_name: str) -> Tuple["UUID", int]:
    
    name_query = player_name.replace(' ', '+')

    url = f"{WEBSITE}/find/player?q={name_query}"
    html = access_url(url)
    
    soup = BeautifulSoup(html, 'html5lib')
    player_name_tags = soup.select(NAME_SELECTORE_ON_FIND_PAGE)
    member_id_tags = soup.select(MEMBER_ID_SELECTOR_ON_FIND_PAGE)
    
    
    for player_name_tag, member_id_tag in zip(player_name_tags, member_id_tags):
        name = player_name_tag.text.strip()

        if name.lower() == player_name.lower():
            # name is match when query
            member_id_str = re.search(r"([0-9]+)", member_id_tag.text.strip())
            if member_id_str is None:
                raise Exception("Can't get the member id!")
            return (
                UUID( player_name_tag["href"].split('/player-profile/')[1] ),
                int( member_id_str.group(1) )
            )
    raise Exception("Error name!! Please check the player name again!")
