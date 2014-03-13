#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#    download script for songs.to, based on the XBMC-plugin for songs.to by sphere  
#    Copyright (C) 2012 sphere
#    Copyright (C) 2014 ucn
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import re
import simplejson as json
from urllib import urlencode
from urllib2 import urlopen, Request, HTTPError, URLError
import urllib2
import sys


MAIN_URL = 'http://songs.to'
PLAY_URL = MAIN_URL + '/data.php?id=%s'

DEFAULT_LANGUAGE = 'de'



class NetworkError(Exception):
    pass


class SongsApi():

    USER_AGENT = 'Sotodo v0.1'

    def __init__(self, language=None):
        if language in ('de', 'en'):
            self.language = language
        else:
            self.language = DEFAULT_LANGUAGE

    def get_chart_types(self):
        path = '/json/app.php?f=charts&lang=%s' % self.language
        return self.__api_call(path)

    def get_charts(self, chart_type):
        path = '/json/songlist.php?charts=%s' % chart_type
        return self.__format_charts(self.__api_call(path), chart_type)

    def get_top_songs(self):
        path = '/json/songlist.php?top=all'
        return self.__format_songs(self.__api_call(path))

    def get_new_songs(self):
        path = '/json/songlist.php?g='
        return self.__format_songs(self.__api_call(path))

    def get_similar_songs(self, song_id):
        path = '/json/songlist.php?record=%s' % song_id
        return self.__format_songs(self.__api_call(path))

    def get_songs(self, album=None, artist=None, title=None):
        if not album and not artist and not title:
            raise AttributeError('Need at least one parameter')
        path = '/json/songlist.php?quickplay=1'
        data_dict = {
            'data': [{
                'artist': artist or '',
                'album': album or '',
                'title': title or ''
            }]
        }
        post_data = {'data': json.dumps(data_dict)}
        return self.__format_songs(self.__api_call(path, post_data))

    def search_songs(self, field, keyword):
        if field == 'all' or field not in ('title', 'album', 'artist'):
            field = ''
        qs = {'keyword': keyword, 'col': field}
        path = '/json/songlist.php?%s' % urlencode(qs)
        return self.__format_songs(self.__api_call(path))

    def get_playlist(self, plist):
        path = '/json/songlist.php?playlist=%s' % plist
        result = self.__format_songs(self.__api_call(path))
        return result


    @staticmethod
    def __format_songs(songs):

        def __cover(cover):
            if cover:
                return '%s/covers/%s' % (MAIN_URL, cover)

        def __date(date_str):
            if date_str:
                y, m, d = date_str.split()[0].split('-')
                return '%s.%s.%s' % (d, m, y)

        return [{
            'id': song['hash'],
            'title': song['title'],
            'artist': song['artist'],
            'album': song['album'],
            'genre': song['genre'],
            'playtime': song['playtime'],
            'bitrate': song['bitrate'],
            'track_nr': song['track_nr'],
            'disc_nr': song['disc_nr'],
            'thumb': __cover(song['cover']),
            #'thumb': song['cover'],
            'date': __date(song['entrydate']),
        } for song in songs]


    @staticmethod
    def __format_charts(charts, chart_type):

        return [{
            'name1': chart['name1'],
            'name2': chart['name2'],
            'position': chart['position'],
            'info': chart['info'],
            'chart_type': chart_type,
        } for chart in charts]


    def __api_call(self, path, post_data=None):
        url = MAIN_URL + path
        if post_data:
            req = Request(url, urlencode(post_data))
        else:
            req = Request(url)
        req.add_header('User-agent', self.USER_AGENT)
       
        try:
            response = urlopen(req).read()            
        except URLError, error:
          
            raise NetworkError(error)
       
        json_data = json.loads(response)
        #print "JSONDATA: "
        #print json_data
        if json_data.get('error'):
            err = json_data['error']
          
        return json_data.get('data', [])


    def download_song(self, id, name):
       url = PLAY_URL % id
       print url
       name=re.sub('\xf6', 'oe', name)
       name=re.sub('\xfc', 'ue', name)
       name=re.sub('\xe4', 'ae', name)
       name=re.sub('[^\w\-_\. ]', ' ', name)
       file_name = name+".mp3"
       req = Request(url)
       req.add_header('User-agent', self.USER_AGENT)
       mp3file =  urllib2.urlopen(req)
       f = open(file_name, 'wb')
       meta = mp3file.info()
       file_size = int(meta.getheaders("Content-Length")[0])
       print "Downloading: %s Bytes: %s" % (file_name, file_size)

       file_size_dl = 0
       block_sz = 8192
       while True:
           buffer = mp3file.read(block_sz)
           if not buffer:
               break

           file_size_dl += len(buffer)
           f.write(buffer)
           status = r"%10d Bytes [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
           status = status + chr(8)*(len(status)+1)
           print status,

       f.close()


    def query_yes_no(self, question, default="yes"):
       """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
       """
       valid = {"yes":True,   "y":True,  "ye":True,
                 "no":False,     "n":False}
       if default == None:
           prompt = " [y/n] "
       elif default == "yes":
           prompt = " [Y/n] "
       elif default == "no":
           prompt = " [y/N] "
       else:
           raise ValueError("invalid default answer: '%s'" % default)
   
       while True:
           print(question + prompt)
           choice = raw_input().lower()
           if default is not None and choice == '':
               return valid[default]
           elif choice in valid:
               return valid[choice]
           else:
               sys.stdout.write("Bitte mit 'yes' or 'no' "\
                                "(or 'y' or 'n') antworten.\n")
