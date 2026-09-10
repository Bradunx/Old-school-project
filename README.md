# Old-school-project
This is an old project I had to do for school, an RFID Jukebox.
Basically a Jukebox running on a Raspberry Pi.

The goal was to develop a solution in any programming language to use RFID cards as disks to switch the music on the Jukebox and be able to control the music on the interface.

The solution was to first write RFID cards with YouTube URLs (from the most accurate video via keywords) in a specific Python program.
Then, the Python VLC library was used to play music, with a lot of features available such as playing video and key controls.
Therefore, a touch screen display was used to show video and as an interface to control the video.

The main program in Python:
- asks to scan an RFID card
- when an RFID card is successfully read, downloads a YouTube video from the URL read
- when the video is downloaded, it will automatically be played on the screen
- the interface is created with the Tkinter library, with labels and buttons to use commands

The project had to be done in 40 hours; even though the main objective of the project was done, I wanted to do a lot more.
After finishing the project for school, I continued the project on my own for my personal usage.
This custom version works as an .exe without RFID cards and has a reworked interface to work on any PC:
- reworked interface with color codes, progress bar, Tkinter buttons, and command keys as controls
- Windows settings (video window, playlist window, and no video window)
- download video directly in the main program via a search bar
- a playlist management system, up to 10 songs (personal limitation), manage song order, and randomizer buttons
  


