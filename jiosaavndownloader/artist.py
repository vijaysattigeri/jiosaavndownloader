from jiosaavndownloader.api_src import endpoints, jiosaavn, helper

import json
import requests


def get_artist_id(a_url):
    res = requests.get(a_url)
    try:
        return (res.text.split('"artistView":{')[1].split('"artist":{"type":"artist","id":"')[1].split('","image":')[0])
    except:
        raise


def get_artist_data(a_url, a_lyrics):
    artist_id = get_artist_id(a_url)
    try:
        artist_details_base_url = endpoints.artist_url+artist_id
        artist_dict = json.loads( requests.get(artist_details_base_url).text )
        
        # Format the data
        artist_dict['image'] = artist_dict['image'].replace("150x150","500x500")
        artist_dict['name'] = helper.format(artist_dict['name'])

        for each_song in artist_dict['topSongs']['songs']:
            helper.format_song(each_song, a_lyrics)

        for i in range(0, len(artist_dict['topAlbums']['albums'])):
            artist_dict['topAlbums']['albums'][i] = jiosaavn.get_album( artist_dict['topAlbums']['albums'][i]['albumid'], a_lyrics)

        return artist_dict
    except:
        raise
        #return None
