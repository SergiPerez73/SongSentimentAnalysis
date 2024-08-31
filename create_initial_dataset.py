import requests
import pandas as pd
import time

def find_point_html(html_content,word,start_point,offset):
    #Gets an html_content to find a word starting by
    #some specific point an adding some offset
    #to the point where it is finded. 
    #A point is an index of the html_content string.

    point = 0
    n_finded = 0
    for i,chr in enumerate(html_content[start_point:]):
        if chr == word[n_finded]:
            n_finded += 1
            if n_finded == len(word):
                point = i + offset
                break
        else:
            n_finded = 0
    
    return point

def find_album_html(html_content):
    #Gets an html_content with the page of a specific
    #song lyrics and returns the starting and ending
    #point of the album name inside the html_content.

    word = 'album: '

    start_album = find_point_html(html_content,word,0,5)
    
    end_album = find_point_html(html_content,'"',start_album,start_album)

    
    return start_album, end_album

def find_lyrics_html(html_content):
    #Gets an html_content with the page of a specific
    #song lyrics and returns the starting and ending
    #point of the lyrics inside the html_content unparsed.

    word = '<!-- Usage'

    offset = - len(word) + 134
    start_lyrics = find_point_html(html_content,word,0,offset)
    
    word = '</div>'
    n_finded = 0

    offset =  - len(word) + 1 + start_lyrics
    end_lyrics = find_point_html(html_content,word,start_lyrics,offset)
    
    return start_lyrics, end_lyrics

def find_songlist_html(html_content):
    #Gets an html_content with the page of a specific
    #music group and returns the starting and ending
    #point of the songlist unparsed.

    word = 'var songlist = '

    offset = - len(word) +19
    start_lyrics = find_point_html(html_content,word,0,offset)
    
    word = '];'
    offset = - len(word) + 1 + start_lyrics
    end_lyrics = find_point_html(html_content,word,start_lyrics,offset)
    
    return start_lyrics, end_lyrics

def read_song_lyrics_html(url):
    #Gets an url of the page of a specific song lyrics
    #song lyrics and returns the lyrics of the song and
    # the name of the album

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        exit()

    start_lyrics, end_lyrics = find_lyrics_html(html_content)
    lyrics_unparsed = html_content[start_lyrics:end_lyrics]
    lyrics_parsed = lyrics_unparsed.replace('<br>','')

    start_album, end_album = find_album_html(html_content)
    album = html_content[start_album:end_album]
    year =  (html_content[end_album+7:end_album+11]) #mejorar
    try:
        year = int(year)
    except:
        year = 0
        album = 'singles'
    return lyrics_parsed, album, year

def read_group_lyrics_html(group):
    #Gets the name of a music group and saves a dataset
    #with a row per song of the group with the name
    #of the song, the album and its lyrics.

    url = 'https://www.azlyrics.com/'+group[0]+'/'+group+'.html'

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
            
        print("HTML read successfully!")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        exit()
    
    start_lyrics, end_lyrics = find_songlist_html(html_content)

    songlist_parsed = html_content[start_lyrics:end_lyrics]

    song_names = []
    song_urls = []

    for line in songlist_parsed.split('\n'):
        end_name = 0
        for i,c in enumerate(line[4:]):
            if c=='"':
                end_name=i+4
                break
        song_names.append(line[4:end_name])

        end_name2 = 0
        for i,c in enumerate(line[end_name+6:]):
            if c=='"':
                end_name2=i+end_name+6
                break

        song_urls.append(line[end_name+6:end_name2])

    song_lyrics = []
    song_album = []
    song_year = []
    for i in range(len(song_names)):
        print(i)
        if (song_urls[i][0] != 'h'):
            url = 'https://www.azlyrics.com' + song_urls[i]
            lyrics,album, year = read_song_lyrics_html(url)
            
        else:
            lyrics, album, year = read_song_lyrics_html(song_urls[i])
        song_lyrics.append(lyrics)
        song_album.append(album)
        song_year.append(year)
        time.sleep(15)
    
    data = {
        'name': song_names,
        'url': song_urls,
        'lyrics': song_lyrics,
        'album': song_album,
        'year': song_year
    }

    df_songlist = pd.DataFrame(data)

    df_songlist.to_csv(group+'.csv')

if __name__ == "__main__":
    group= 'eminem'
    
    read_group_lyrics_html(group)

    

