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

                if correct == "Y" or correct == "y":
                    advance = True
                elif correct == "N" or correct == "n":
                    advance = False
                    library.close()
                    
                # Start of actually reading data
                current_line = library.readline()
                current_song = ""
                current_line_number = 8
                while current_line != "	<key>Playlists</key>\n":
                    if current_line.find("Name") != -1:
                        current_song = current_line[current_line.find("string") + 7:current_line.find("</string>")]
                        print(current_song)
                    current_line_number += 1 
                    current_line = library.readline()



if __name__ == "__main__":
    main()
