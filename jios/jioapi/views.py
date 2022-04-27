from django.shortcuts import render, redirect
import requests as rs
import json
import requests
import os.path
import mimetypes
from django.http import HttpResponse
def homepage(request):
    request_from_html=request.POST.get("songname")
    query=str(request_from_html)
    query=query.strip(" ")
    query=query.replace(" ","%2520")
    song_search=rs.get(f"https://www.jiosaavn.com/api.php?__call=autocomplete.get&query={query}&_format=json&_marker=0&ctx=web6dot0")
    song_id=song_search.content
    song_id=str(song_id)
    song_id=song_id.replace("b'\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n",'')
    song_id=song_id.replace("\\",'')
    song_id=song_id.replace("\'",'')
    song_id=json.loads(song_id)
    check=song_id["topquery"]['data']
    print(check)
    if len(check)==0:
        check="This_is_empty"
        song_id="None"
        go={song_id:"None"}
    else:
        check=song_id["topquery"]['data'][0]['more_info']
        song_id_check='song_pids'
        if song_id_check in check:
            print("This worksssssssssssssss")
            song_id=song_id["topquery"]['data'][0]['more_info']['song_pids']

        else:
            song_id=song_id["topquery"]['data'][0]['id']

    if check != "This_is_empty":
        song_request = rs.get(f"https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids={song_id}")
        cleaning_url = str(song_request.content)
        cleaning_url = cleaning_url.replace("b'\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n", '')
        cleaning_url = cleaning_url.replace("\\", '')
        cleaning_url = cleaning_url.replace("\'", '')
        cleaning_url=cleaning_url.replace("https://preview.saavncdn.com/","https://snoidcdnems08.cdnsrv.jio.com/jiosaavn.cdn.jio.com/")
        cleaning_url=cleaning_url.replace("96_p","320")
        print(5 * '-')
        go = json.loads(cleaning_url)
        print(go)

    return render(request, "homepage.html", {'data': go[song_id]})

