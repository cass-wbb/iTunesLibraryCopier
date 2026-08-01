# iTunesLibraryCopier
Copies selected items from an iTunes Library XML file and lets you move those specific files to whatever you want


# Using the program
<b>This program is intended for use on iTunes for Windows. It has not been tested with the new Apple Music apps on the Microsoft Store, or on iTunes for macOS or the Apple Music replacement in moderm macOS.</b>

## Creating necessary files
To start, you will need to export your library as a .xml through iTunes. In iTunes, click File -> Library -> Export Library

![Image showing how to export your library as an xml](readme_images/export.png)

Be sure to put this xml file in a place that you will know where it is at.

## The Process
* Run copier.py
* Input the path to the .xml file generated from iTunes. This can be a relative path or a complete path.
* Verify that it is the correct database file
* Determine an output destination. This can be a relative path or a complete path.
* Decide how to copy
    * All songs in library
    * Album by album
    * Playlist by Playlist


# Warnings
* If your iTunes Library's music takes up more storage than what you have available at the target, it will throw an error, any song copied before the space is filled will still be there, but any song after will not be.
* This tool will only properly work for music in your library. Videos will not copy, and audio using the "Open Stream" option in iTunes will not copy either.
* This is a work in progress, and as such, errors not mentioned here may show up.
* Most file names <i>should</i> be fine, but some special characters may give it issues, if this is the case, please open an issue!

# To be implemented
* More error handling
* Testing on the new Apple Music app on the Windows Store
* Testing on older macOS iTunes
    * Unfortunately I do not have a modern Mac so I will not be able to test with the new apps.