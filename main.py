import shutil
from urllib.parse import unquote
import os

def main():
    advance = False
    while not advance:
        xml_path = input("Please input the path for the iTunes Library file: ")

        with open(xml_path, "r", encoding='utf-8', errors='ignore') as library:
            # Verify this is an iTunes Library XML via second line check
            library.readline()
            second_line = library.readline()
            if second_line != '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n':
                print("Not an iTunes XML File.")
                print(second_line)
                library.close()

            else:
                # skip the next few lines as there is no relevant data here
                for i in range(4):
                    library.readline()
                # Show user the date and time this xml file was generated, if it is not correct, they can find the correct one
                date_generated = library.readline()[22:-9]
                print("Database file generated on " + date_generated[:10] + " at " + date_generated[11:] + " UTC")

                correct = input("Is this the correct file? Y or N: ")
                if (correct != "Y" and correct != "y" and correct != "N" and correct != "n"):
                    correct = input("Please type Y or N: ")
                    print(correct)

                if correct == "N" or correct == "n":
                    advance = False
                    library.close()
                elif correct == "Y" or correct == "y":
                    advance = True

                    output_location = input("Please provide the location to output all songs: ") 
                        
                    # Start of actually reading data
                    current_line = library.readline()
                    current_song = ""
                    current_id = 0
                    current_song_location = ""
                    current_album = ""
                    current_album_f = ""
                    all_songs = {}

                    while current_line != "	<key>Playlists</key>\n":  # Kept like this in case for whatever reason a song name is Playlists
                        if current_line.find("Track ID") == 8:
                            # ID used in playlists
                            current_id = current_line[current_line.find("integer") + 8 : current_line.find("</integer>")]

                        if current_line.find("Name") == 8:
                            current_song = current_line[current_line.find("string") + 7:current_line.find("</string>")]

                        if current_line.find("Album</key>") == 8:
                            current_album_f = ""
                            current_album = current_line[current_line.find("string") + 7:current_line.find("</string>")]
                            for letter in current_album:
                                if letter.isalnum() or letter.isspace():
                                    current_album_f = current_album_f + letter
                            print(current_album_f)

                        if current_line.find("Location") == 8:
                            current_song_location = current_line[current_line.find("string") + 7:current_line.find("</string>")]
                            current_song_location = unquote(current_song_location)
                            if current_song_location.find('file://localhost/') != -1:
                                current_song_location = current_song_location[17:]
                            all_songs.update({current_id: {"name" : current_song, "album" : current_album_f, "location" :  current_song_location}})

                        current_line = library.readline()

                    library.close()
                    
                    for song in all_songs:
                        # print(all_songs[song]["location"])
                        # print(output_location + all_songs[song]["album"])
                        if not os.path.exists(output_location + all_songs[song]["album"] + "/"):
                            os.makedirs(output_location + all_songs[song]["album"] + "/")
                        shutil.copy2(all_songs[song]["location"], output_location + all_songs[song]["album"] + "/" +  all_songs[song]["location"][all_songs[song]["location"].rfind("/"):])



if __name__ == "__main__":
    main()
