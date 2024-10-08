from plexapi.myplex import MyPlexAccount

account = MyPlexAccount('<ACCOUNT>', '<PASSWORD>')
plex = account.resource('<SERVER>').connect()  # returns a PlexServer instance
music = plex.library.section('Music')
playlists = plex.playlists()

def build_fkey2tr(): #builds an array of all file paths in your library, to match against in your playlist
  global fkey2tr
  fkey2tr = {}
  for tr in music.searchTracks():
    fkey = tr.media[0].parts[0].file.lower() #enforces case sensitivity, just in case
    print("fkey",repr(fkey))
    if fkey in fkey2tr:
      print("fkey2tr ERROR:",fkey,"for",tr,"was",fkey2tr[fkey]) #if you somehow have two entries in your library that are pointing to the same file, throws an error
    fkey2tr[fkey] = tr
  print(len(fkey2tr), "tracks.")

build_fkey2tr()

plexpl=plex.playlist( '<TARGET PLAYLIST>' ) #Playlist you're writing to. I'm sure there's an API thing for "create" which could be subbed in here, but this code assumes you have an (empty, because it will be appending) playlist already in existence with this name

#pl = []
def updpl(plexpl,f):
#  global pl
  pl = []
  with open(f, 'r', encoding="utf8") as m3ufile: #Encoding utf-8 to handle ASCII characters
    cnt = 0
    cntpl = 0
    for fname in m3ufile:
      cnt = cnt+1
      fkey = fname.lower().rstrip() #enforce lowercase, strips \n
      if fkey in fkey2tr:
        cntpl = cntpl+1
        tr = fkey2tr[ fkey ]
        pl.append( tr )
        plexpl.addItems( tr ) #if you have a match, append to playlist
      else:
        print("fname=",fname,"fkey=",repr(fkey),"has no fkey2tr") #prints if there's a track that doesn't find a match

    print(cnt, "lines in M3U file.") 
    print(len(pl),"(",cntpl,")", "tracks in playlist.") #sanity stuff - at the end prints the number of lines in the m3u playlist and the number of tracks matched and added to the plex playlist 

updpl( plexpl, '<PATH TO M3U FILE>' )
