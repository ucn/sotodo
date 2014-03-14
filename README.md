sotodo
======

**a download script for songs.to**


```
Usage: sotodo.py "album" [-a "kuenstler"] [-t "titel"] [-f] [-n] [-c]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a ARTIST, --artist=ARTIST
                        Suche nach Kuenstlername durchfuehren.
  -t TITLE, --title=TITLE
                        Suche nach Liedtitel durchfuehren.
  -p PLAYLIST, --playlist=PLAYLIST
                        Anzeigen einer Playlist.
  -c, --charts          Charts anzeigen.
  -f, --top             Anzeigen der Top500-Songs.
  -n, --new             Neueste Lieder anzeigen.
```

Verwendung:
----------------------

Dieses Python-Skript ist dazu gedacht mp3-Dateien von songs.to herunterzuladen.

Es kann nach einem Albumtitel, nach einem Künstlernamen oder nach einem Songtitel gesucht werden. Dies geschieht über die Angabe von Parametern. Wird das Skript ohne Optionen aufgerufen, so wird standardmäßig eine Albensuche durchgeführt. Nach Künstler bzw. Titel kann man unter Verwendung der entsprechenden Schalter suchen.

Ebenso ist es möglich eine Playlist auf songs.to mit Benutzerkonto zusammenzustellen und unter Angabe des Zahlencodes im Link der Playliste, diese anzuzeigen. Beispiel: http://songs.to/#!li=m5aAWlL3 => m5aAWlL3 => sotodo.py -p m5aAWlL3

Der Schalter -f lässt die Top500-Songs auf songs.to anzeigen.

Der Schalter -n lässt die neuesten Songs auf songs.to anzeigen.

Der Schalter -c zeigt die verfügbaren Charts auf songs.to an. Von diesen kann einer ausgewählt und angezeigt werden. Die einzelnen Platzierungen in den Charts lassen sich herunterladen.

War eine Suche erfolgreich, fragt das Skript nach den herunterzuladenden Songs. Die Eingabe kann wie folgt aussehen:


Auswahl eines Titels: 42

Auswahl mehrerer Titel: 08-15

Auswahl eines Bereichs von Titeln: 2, 4, 8, 16



Danach bittet das Skript um eine Bestätigung und beginnt dann mit dem Herunterladen der Lieder. Die Lieder werden hierbei im selben Verzeichnis, in welchem sich das Skript befindet gespeichert.

Das Skript kann jederzeit mit Ctrl+C bzw. Ctrl+D abgebrochen werden. Noch nicht fertig heruntergeladene Dateien können jedoch dadurch verloren gehen.


Danksagung:
----------------------
Dieses Skript basiert auf dem [XBMC-Plugin von sphere](http://www.xbmcnerds.com/index.php?page=Thread&threadID=21940).
