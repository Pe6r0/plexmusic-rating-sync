import plexapi
import eyed3
import plexapi.myplex

#plex ratings 0 - 10

#auxiliary script to rearrange the ratings (if you want to sync file and plex ratings this isn't the right script. use the other one. configure start.ps1 for it)

error = 0
removed = 0
movedTo1 = 0
tolerate = 0
keptsame = 0
total = 0

account = plexapi.myplex.MyPlexAccount('email', 'password')
plex = account.resource('name of plex server').connect()  # returns a PlexServer instance
print('connected')
for album in plex.library.section('Music').albums():
    #print('#################Checking out album: ' + str(album))
    for track in album.tracks():
        total += 1
        if isinstance(track.userRating, float):
            try:
                print(track.title)
                print('rating of' + str(track.userRating) + '(' + str(track.userRating/2) +') detected.')
                if track.userRating <= 0.5: # 0 - 0.25
                    track.rate(None)
                    removed += 1
                elif track.userRating <= 4.5: # 0.25 - 2.25
                    track.rate(2.0)
                    movedTo1 += 1
                elif track.userRating <= 5.5: # 2.25 - 2.75
                    track.rate(4.0)
                    tolerate += 1
                elif track.userRating <= 6.5: # 2.75 - 3.25
                    track.rate(6.0)
                    keptsame += 1 
                elif track.userRating <= 7.5: # 3.25 - 3.75
                    track.rate(7.0)
                    keptsame += 1    
                elif track.userRating <= 8.5: # 3.75 - 4.25
                    track.rate(8.0)
                    keptsame += 1  
                elif track.userRating <= 9.5: # 4.25 - 4.75
                    track.rate(9.0)
                    keptsame += 1                                          
                else:
                    track.rate(10.0) # 4.75 - 5.0
                    keptsame += 1
            except:
                print('Could not remove rate file. Continuing.')
                error += 1
        else:
            print('.', end='')

print("removed: " + str(removed))
print("moved to 1 star: " + str(movedTo1))
print("tolerate: " + str(tolerate))
print("kept the same: " + str(keptsame))
print("total = " + str(total))
print("problematic tracks: " + str(error))





