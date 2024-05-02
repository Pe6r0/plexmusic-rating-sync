# Requires eyed3 and plexapi libraries, written & tested in python 3.9

from plexapi.myplex import MyPlexAccount
import eyed3

LIB = 'Syno'
# Counters
insync = 0
justsynced = 0
notag = 0
error = 0

def loadFile(str):
    loc = makeRemoteString(str)
    print('trying to load ' + loc)
    audiofile = eyed3.load(loc)
    print('loaded')
    return audiofile

def makeRemoteString(str):
    locationPrepend = r'X:/'
    locationRemove = r'/volume2/music'
    tmp = str.replace(locationRemove, locationPrepend)
    return tmp

def getRatingValueFromFile(file):
    return file.tag.popularities.get(b'MusicBee')

def convertRatingsToPlex(n):
    return float(n * 10 / 255)

def convertRatingsToMusicBee(n):
    return int(n * 255 / 10)

#plex ratings 0 - 10
#musicBee ratings 0 - 255


print("start")

account = MyPlexAccount('', '')
plex = account.resource(LIB).connect()
print('connected')
for album in plex.library.section('Music').albums():
    print('#################Checking out album: ' + str(album))
    for track in album.tracks():
        
        # Iterates across all tracks
        try:
            if isinstance(track.userRating, float): 
                # Checks to see if the Plex userRating exists, var type will be float if track is rated, it will be nonetype if not.
                
                print(track.title + ' is already rated in Plex, exporting..')
                file = loadFile(track.locations[0])
                # Ratings on both? We prefer plex to dictate for now, so we always write it on the file if present
                file.tag.popularities.set(b'MusicBee',convertRatingsToMusicBee(float(track.userRating)),0)
                file.tag.save()
                ratingFrame = getRatingValueFromFile(file)
                print('ID3 tag rating value of ' + str(ratingFrame.rating) + ' saved from Plex (' + str(convertRatingsToPlex(ratingFrame.rating)) + ')' )
                justsynced += 1 
            else:
                # This case is where Plex has no rating so it tries to fetch a value from the id3 tag
                
                print(track.title + ' has no rating in Plex, checking file id3 tag')
                file = loadFile(track.locations[0])
                ratingFrame = getRatingValueFromFile(file)
                if ratingFrame is not None:
                    # this case is where Plex has no rating but the iD3 tag does so the next steps import the rating into Plex.
                    track.rate(convertRatingsToPlex(ratingFrame.rating))
                    print('ID3 tag rating value of ' + str(ratingFrame.rating) + ' found and saved to Plex userRating field (' + str(convertRatingsToPlex(ratingFrame.rating)) + ')')
                    justsynced += 1 
                else:
                    print('No tag present on either side, continuing.')
                    notag += 1
        except:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Some odd problem with the file.. continuing.')
            error += 1

# Stats Output                          
print(str(insync) + ' files alread in sync')
print(str(justsynced) + ' newly synced files')
print(str(notag) + ' files with no tags')
print(str(error) + ' files had errors')
