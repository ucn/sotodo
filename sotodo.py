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

from resources.lib.api import SongsApi, NetworkError
import sys
from optparse import OptionParser 



parser = OptionParser(usage = "Usage: %prog \"album\" [-a \"kuenstler\"] [-t \"titel\"] [-f] [-n] [-c]", version="%prog 0.2")
api = SongsApi()


parser.add_option("-a", "--artist", dest="artist", help="Suche nach Kuenstlername durchfuehren.")
parser.add_option("-t", "--title", dest="title", help="Suche nach Liedtitel durchfuehren.")
parser.add_option("-p", "--playlist", dest="playlist", help="Anzeigen einer Playlist.")
parser.add_option("-c", "--charts", action="store_true", default=False, help="Charts anzeigen.")
parser.add_option("-f", "--top", action="store_true", default=False, help="Anzeigen der Top500-Songs.")
parser.add_option("-n", "--new", action="store_true", default=False, help="Neueste Lieder anzeigen.")
(parameter, args) = parser.parse_args()


def search_songs():
      
   if parameter.artist!=None and parameter.title!=None:
      parser.print_help()
      parser.error("Es wird maximal ein optionales Argument erwartet.")
      
   if len(args)==1: 
      if parameter.artist==None and parameter.title==None:
         if (len(sys.argv[1])<=2):
            print "Der Suchbegriff muss länger als zwei Zeichen sein."
            sys.exit()

         print "Suche wurde gestartet"
         result=api.search_songs("album", sys.argv[1]) #album, artist, title	

         if len(result)>0:
            i=0
            for song in result:   
               i=i+1
               string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
               print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )
            
            print "Es wurde(n) %s Songs gefunden." % i
            srange=enter_range()
            download_songs(result, srange[0], srange[1], srange[2])

         else:
            print "Die Suche lieferte keine Ergebnisse."
   
   if parameter.artist!=None and parameter.title==None and sys.argv[1]=="-a":
      if (len(parameter.artist)<=2):
         print "Der Suchbegriff muss länger als zwei Zeichen sein."
         sys.exit()

      print "Suche wurde gestartet"
      result=api.search_songs("artist", parameter.artist)

      if len(result)>0:
         i=0
         for song in result:   
            i=i+1
            string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
            print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

         print "Es wurde(n) %s Songs gefunden." % i
         srange=enter_range()
         download_songs(result, srange[0], srange[1], srange[2])

      else:
         print "Die Suche lieferte keine Ergebnisse."

   if parameter.artist==None and parameter.title!=None and sys.argv[1]=="-t":
      if (len(parameter.title)<=2):
         print "Der Suchbegriff muss länger als zwei Zeichen sein."
         sys.exit()

      print "Suche wurde gestartet"
      result=api.search_songs("title", parameter.title)

      if len(result)>0:
         i=0
         for song in result:
            i=i+1  
            string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
            print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

         print "Es wurde(n) %s Songs gefunden." % i
         srange=enter_range()
         download_songs(result, srange[0], srange[1], srange[2])

      else:
         print "Die Suche lieferte keine Ergebnisse."


def enter_range():
   srange = raw_input("Bitte herunterzuladende Songs eingeben (n oder a,b,c,…,z oder x-y): ")

   if "-" in srange:
      split=srange.split("-")
      #print split

      try: int(split[0])
      except ValueError:
         print "Ungültige Eingabe. Bitte geben Sie eine Zahl ein."
         sys.exit()

      try: int(split[1])
      except ValueError:
         print "Ungültige Eingabe. Bitte geben Sie eine Zahl ein."
         sys.exit()

      if (int(split[0])<int(split[1])):
         return int(split[0]), int(split[1]), None #start, end

      if (int(split[1])<int(split[0])):
         return int(split[1]), int(split[0]), None

      if (int(split[0])==int(split[1])):
         return int(split[0]), int(split[1]), None

   elif ("," in srange):
      split=srange.split(",")

      for i in range(0, len(split)):
         try: int(split[i])
         except ValueError:
            print "Ungültige Eingabe. Bitte geben Sie eine Zahl ein."
            sys.exit()

      return -1, -1, split

   else:
      try: int(srange)
      except ValueError:
         print "Ungültige Eingabe. Bitte geben Sie eine Zahl ein."
         sys.exit()

      return srange, srange, None


def download_songs(result, range_start=None, range_end=None, range_array=None):
   #print int(range_start), int(range_end), range_array

   if range_array!=None:
      if 0 in range_array:
         sys.exit()

      for i in range(1, len(range_array)):
         if int(range_array[i])>len(result):
            sys.exit()

      choice=api.query_yes_no("%s Songs herunterladen?" % (len(range_array)))

      if choice:
         for i in range(0, len(range_array)):
            print i
            api.download_song(result[int(range_array[i])-1]['id'], "%s - %s" % (result[int(range_array[i])-1]['artist'], result[int(range_array[i])-1]['title']))

         print "%s Songs erfolgreich heruntergeladen." % len(range_array)

      else:
         sys.exit()

   else:
      if int(range_start)<1:
         sys.exit()

      if int(range_end)>len(result):
         sys.exit()

      if int(range_start)==int(range_end):
         choice=api.query_yes_no("1 Song herunterladen?")

         if choice:
            i=int(range_start)
            for song in result:
               print i
               api.download_song(result[i-1]['id'], "%s - %s" % (result[i-1]['artist'], result[i-1]['title']))
               i=i+1
               print "1 Song erfolgreich heruntergeladen."
               break

         else:
            sys.exit()

      elif int(range_start)!=int(range_end):
         choice=api.query_yes_no("%s Songs herunterladen?" % (int(range_end)+1-int(range_start)))

         if choice:
            i=int(range_start)
            for song in result:
               if i>int(range_end):
                  print "%s Songs erfolgreich heruntergeladen." % (int(range_end)+1-int(range_start))
                  break

               else:
                  print i
                  api.download_song(result[i-1]['id'], "%s - %s" % (result[i-1]['artist'], result[i-1]['title']))
                  i=i+1

         else:
            sys.exit()


def show_top_500_songs():
   return api.get_top_songs()


################################################################################

sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=130))

if len(sys.argv)>3:
   parser.print_help()
   parser.error("Zuviele Argumente.")

try:
   if (parameter.top==True):
      result=show_top_500_songs()

      if len(result)>0:
         i=0
         for song in result:   
            i=i+1
            string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
            print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

         srange=enter_range()
         download_songs(result, srange[0], srange[1], srange[2])

      else:
          print "Die Suche lieferte keine Ergebnisse."

   elif (parameter.playlist!=None):
      result=api.get_playlist(parameter.playlist)

      if (len(result)>0):
         i=0
         for song in result:   
            i=i+1
            string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
            print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

         srange=enter_range()
         download_songs(result, srange[0], srange[1], srange[2])

      else:
          print "Die Playlist ist leer oder existiert nicht."

   elif (parameter.new==True):
      result=api.get_new_songs()

      if (len(result)>0):
         i=0
         for song in result:   
            i=i+1
            string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
            print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

         print "Es wurde(n) %s Songs gefunden." % i
         srange=enter_range()
         download_songs(result, srange[0], srange[1], srange[2])

      else:
          print "Konnte neueste Songs nicht laden."

   elif (parameter.charts==True):
      chart_types=api.get_chart_types()
      liste=[]
      i=0

      for chart_type in chart_types:
         liste.insert(i, chart_type)
         i=i+1
         string=str(i) + "ID: " +chart_type['type'] + " Name: " + chart_type['title']
         print(string)

      print "Bitte gewünschte Chart-Nummer eingeben."
      choice = raw_input()

      try: int(choice)
      except ValueError:
         print "Ungültige Eingabe. Bitte geben Sie eine Zahl ein."
         sys.exit()

      if int(choice)>0:
         try:
            charts=api.get_charts(liste.pop(int(choice)-1)['type'])
         except:
            print "Ungültige Eingabe."
            sys.exit()
      else:
         print "Ungültige Eingabe."
         sys.exit()

      if len(charts)>0:

         if liste.pop(int(choice)-2)['is_album']==True:

            for chart in charts:
               string='    Position: ' + chart['position']+ '   Kuenstler: ' + chart['name1'] + '   Album: ' + chart['name2']
               print string
            print "Bitte Album-Nr. auswählen."
            suche=raw_input()
            result=api.search_songs("album", charts[int(suche)-1]['name2'].encode('ascii', 'replace'))

            if len(result)>0:
               i=0
               for song in result:
                  i=i+1  
                  string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
                  print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

               print "Es wurde(n) %s Songs gefunden." % i
               srange=enter_range()
               download_songs(result, srange[0], srange[1], srange[2])

            else:
               print "Die Suche lieferte keine Ergebnisse."
         else:

            for chart in charts:

               string='    Position: ' + chart['position']+ '   Kuenstler: ' + chart['name1'] + '   Titel: ' + chart['name2']
               print string

            print "Bitte Lied-Nr. auswählen."
            suche=raw_input()
            result=api.search_songs("title", charts[int(suche)-1]['name2'].encode('ascii', 'replace'))

            if len(result)>0:
               i=0
               for song in result:
                  i=i+1  
                  string=str(i) + '    Titel: ' + song['title'] + '   Kuenstler: ' + song['artist'] + '   Album: ' + song['album']+ '   Genre: '+ song['genre']
                  print (#            'hash': song['hash'],
                     string
#            'playtime': song['playtime'],
#            'bitrate': song['bitrate'],
#            'track_nr': song['track_nr'],
#            'disc_nr': song['disc_nr'],
#           'thumb': __cover(song['cover']),
#           'date': __date(song['entrydate']),
	                )

               print "Es wurde(n) %s Songs gefunden." % i
               srange=enter_range()
               download_songs(result, srange[0], srange[1], srange[2])

            else:
               print "Die Suche lieferte keine Ergebnisse."

   elif len(sys.argv)==1:
      parser.print_help()
      sys.exit()

   else:
      search_songs()

except (KeyboardInterrupt, EOFError):
   sys.exit("\nKeyboardInterrupt or EOFError => Exiting …")
