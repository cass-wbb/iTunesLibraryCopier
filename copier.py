import shutil
from urllib.parse import unquote
import os
import time
import datetime


def main():
    xml_path = input("Please input the path for the iTunes Library file: ")

    with open(xml_path, "r", encoding='utf-8', errors='ignore') as library:
        # Verify this is an iTunes Library XML via second line check
        library.readline()
        second_line = library.readline()
        if second_line != '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n':
            print("Not an iTunes XML File.")
            library.close()

        else:
            # skip the next few lines as there is no relevant data here
            for i in range(4):
                library.readline()
            # Show user the date and time this xml file was generated, if it is not correct, they can find the correct one
            date_generated = library.readline()[22:-9]
            print("Database file generated on " + date_generated[:10] + " at " + date_generated[11:] + " UTC")
            print("If this is not correct, please restart.")

            output_location = input("Please provide the location to output all songs: ") 
            if not output_location.rfind("/") == len(output_location) - 1 and not output_location.rfind("\\") == len(output_location) -1:
                output_location = output_location + "/"
                
            # Start of actually reading data
            current_line = library.readline()
            current_song = ""
            current_id = 0
            current_song_location = ""
            current_album_artist = ""
            current_album_artist_f = ""
            current_album = ""
            current_album_f = ""
            all_songs = {}
            ignore = False
            kind_str = ""

            while current_line != "	<key>Playlists</key>\n":  # Kept like this in case for whatever reason a song name is Playlists
                
                if current_line.find("Kind") == 8:
                    ignore = False
                    kind_str = current_line[current_line.find("string") + 7 : current_line.find("</string>")]
                    # Check to make sure if is either an imported audio file, ripped from a CD, or purchased from iTunes, and is a song
                    # Also removes songs that are audio streams
                    if not kind_str == "MPEG audio file" and not kind_str == "Purchased AAC audio file" and not kind_str == "AAC audio file":
                        ignore = True
                
                if current_line.find("Track ID") == 8:
                    # ID used in playlists
                    current_id = current_line[current_line.find("integer") + 8 : current_line.find("</integer>")]

                if current_line.find("Name") == 8:
                    current_song = current_line[current_line.find("string") + 7:current_line.find("</string>")]

                if current_line.find("Album Artist</key>") == 8:
                    current_album_artist_f = ""
                    current_album_artist = current_line[current_line.find("string") + 7:current_line.find("</string")]
                    for letter in current_album_artist:
                        # Removes any characters that may cause issues in the directory name
                        if letter.isalnum() or letter.isspace():
                            current_album_artist_f = current_album_artist_f + letter

                if current_line.find("Album</key>") == 8:
                    current_album_f = ""
                    current_album = current_line[current_line.find("string") + 7:current_line.find("</string>")]
                    for letter in current_album:
                        # Removes any characters that may cause issues in the directory name
                        if letter.isalnum() or letter.isspace():
                            current_album_f = current_album_f + letter

                if current_line.find("Location") == 8:
                    current_song_location = current_line[current_line.find("string") + 7:current_line.find("</string>")]
                    # Removes most HTML URL encoding, not all though
                    current_song_location = unquote(current_song_location)

                    # Things to remove
                    if current_song_location.find('file://localhost/') != -1:
                        current_song_location = current_song_location[17:]

                    # Other symbols to fix
                    if current_song_location.find("&#38;") != -1:
                        current_song_location = current_song_location[:current_song_location.find("&#38;")] + "&" + current_song_location[current_song_location.find("&#38;") + 5:]
                        
                    if not ignore:
                        # If not audio, ignore
                        all_songs.update({current_id: {"name" : current_song, "artist" : current_album_artist_f, "album" : current_album_f, "location" :  current_song_location}})

                current_line = library.readline()

    select_type = input("How would you like to export these tracks?"
                                "\n1: All tracks in library\n2: Select by album\n3: Select by playlist\n")
    if select_type == "1":
        for song in all_songs:
            if not os.path.exists(output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/"):
                os.makedirs(output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/")
            shutil.copy2(all_songs[song]["location"], output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/" +  all_songs[song]["location"][all_songs[song]["location"].rfind("/"):])
            print(f"{datetime.datetime.now()} - {all_songs[song]["name"]} moved from {all_songs[song]["location"]} to {output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/" +  all_songs[song]["location"][all_songs[song]["location"].rfind("/"):]}")

    elif select_type == "2":
        # Get list of all albums
        album_list = []
        for song in all_songs:
            if all_songs[song]["album"] not in album_list:
                album_list.append(all_songs[song]["album"])
        # Continue to ask user albums to copy
        while True:
            if len(album_list) == 0:
                print("\nNo more albums left to copy!")
                break
            else:
                print("\nAll albums:")
                for i in range(len(album_list)):
                    print(f"{i + 1}: {album_list[i]}")
                selection = input("Please select one album to copy: ")
            
                if not selection.isdigit() or not int(selection) == float(selection)  or int(selection) <= 0 or int(selection) > len(album_list):
                    print("Not a valid album number.")
                    time.sleep(2)

                else:
                    for song in all_songs:
                        if all_songs[song]["album"] == album_list[int(selection) - 1]:
                            if not os.path.exists(output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/"):
                                os.makedirs(output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/")
                            shutil.copy2(all_songs[song]["location"], output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/" +  all_songs[song]["location"][all_songs[song]["location"].rfind("/"):])
                            print(f"{datetime.datetime.now()} - {all_songs[song]["name"]} moved from {all_songs[song]["location"]} to {output_location + all_songs[song]["artist"] + "/" + all_songs[song]["album"] + "/" +  all_songs[song]["location"][all_songs[song]["location"].rfind("/"):]}")
                    album_list.pop(int(selection) - 1)
                
                advance = input("Type Y to continue copying albums: ")
                if not advance == "y" and not advance == "Y":
                    break

    elif select_type == "3":
        default_playlists = ["Downloaded", "Music", "Movies", "TV Shows", "Podcasts", "Audiobooks", "Genius"]
        ignore = False
        all_playlists = {}
        playlist_songs = []
        playlist_id = ""
        playlist_name = ""
        current_line == library.readline()
        while not current_line == "</plist>\n":

            if current_line.find("Master") == 8:
                # Removes some default playlists
                ignore = True

            if current_line.find("Name") == 8:
                playlist_name = current_line[current_line.find("string") + 7 : current_line.find("</string>")]
                # Ignore default playlists
                if not default_playlists.count(playlist_name) == 0:
                    ignore = True

            if current_line.find("Playlist ID") == 8:
                playlist_id = current_line[current_line.find("integer") + 8 : current_line.find("</integer>")]

            if current_line.find("Track ID") == 10:
                song_id = current_line[current_line.find("integer") + 8 : current_line.find("</integer>")]
                # Only add song if it is in the library as a song
                if not all_songs.get(song_id) == None:
                    playlist_songs.append(song_id)

            if current_line.find("</array>") == 3:
                # End of playlist
                if not ignore:
                    all_playlists.update({playlist_id: {"name" : playlist_name, "songs" : playlist_songs}})
                # Reset values
                ignore = False
                playlist_songs = []

            current_line = library.readline()

        # Get list of all playlists
        playlist_list = []
        id_list = []
        for playlist in all_playlists:
            playlist_list.append(all_playlists[playlist]["name"])
            id_list.append(playlist)
        # Continue to ask user playlists to copy
        while True:
            if len(playlist_list) == 0:
                print("\n No more playlists left to copy!")
                break
            else:
                print("\nAll playlists:")
                for i in range(len(playlist_list)):
                    print(f"{i + 1}: {playlist_list[i]}")
                selection = input("Please select one album to copy: ")

                if not selection.isdigit() or not int(selection) == float(selection)  or int(selection) <= 0 or int(selection) > len(playlist_list):
                    print("Not a valid playlist number.")
                    time.sleep(2)

                else:
                    # Create path for playlist folder
                    if not os.path.exists(output_location + playlist_list[int(selection) - 1] + "/"):
                        os.makedirs(output_location + playlist_list[int(selection) - 1] + "/")
                    # Song is formatted in ID number
                    for song in all_playlists[id_list[int(selection) - 1]]["songs"]:
                        shutil.copy2(all_songs[song]["location"], output_location + playlist_list[int(selection) - 1] + "/" + all_songs[song]["location"][all_songs[song]["location"].rfind("/"):])
                        print(f"{datetime.datetime.now()} - {all_songs[song]["name"]} moved from {all_songs[song]["location"]} to {output_location + playlist_list[int(selection) - 1] + "/" + all_songs[song]["location"][all_songs[song]["location"].rfind("/"):]}")
                        
                    playlist_list.pop(int(selection) - 1)

                    advance = input("Type Y to continue copying playlists: ")
                    if not advance == "y" and not advance == "Y":
                        break

        library.close()

if __name__ == "__main__":
    main()
