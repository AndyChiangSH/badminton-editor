from crawler import (
    crawl_find_page_by_name, crawl_player_page_by_id, crawl_ranking_page_by_id,
    crawl_h2h_page_by_id, crawl_tournament_page_by_name
)
from typing import Dict, Any
from datetime import datetime


"""
Given the player name 
and return the rank & category of that palyer
"""
def get_rank(player_name: str) -> Dict[str, Any]:

    uuid, _ = crawl_find_page_by_name(player_name)
    result = crawl_ranking_page_by_id(uuid)

    return {
        "rank": result["ranking"],
        "category": result["category"]
    }

"""
Given the player name 
and return the country of that palyer
"""
def get_country(player_name: str) -> Dict[str, Any]:

    uuid, _ = crawl_find_page_by_name(player_name)
    result = crawl_player_page_by_id(uuid)

    return {
        "country": result["country"]
    }


"""
Given the player name 
and return the age of that palyer
"""
def get_age(player_name: str) -> Dict[str, Any]:

    uuid, _ = crawl_find_page_by_name(player_name)
    result = crawl_player_page_by_id(uuid)

    return {
        "age": int(datetime.now().year) - result["Year of birth"]
    }


"""
Given the player name 
and return the latest tournemant and result
"""
def get_tournament(player_name: str) -> Dict:
    result = crawl_tournament_page_by_name(player_name)
    return result


"""
Given the player1 & player2 name 
and return the head2head result and latest match
"""
def get_h2h(player_name1: str, player_name2: str) -> Dict:
    _, member_id1 = crawl_find_page_by_name(player_name1)
    _, member_id2 = crawl_find_page_by_name(player_name2)
    
    result = crawl_h2h_page_by_id(member_id1, member_id2)

    if result["match-details"]["winner"] == 1:
        result["match-details"]["winner"] = player_name1
    else:
        result["match-details"]["winner"] = player_name2


    return result
