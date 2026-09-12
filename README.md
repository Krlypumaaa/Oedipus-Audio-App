# Oedipus-Audio-App
A small local audio player written in python
## About

I mad this as a fun little project for myself after getting upset at the default Microsoft media player and not wanting to install and alternative myself. The project was written entirely in python mainly using the PyQt6 import libraries. The source code is somewhat sloppy, I tried my best to clean it up but I have no real Idea on how to best organize my code for others. I don't think I plan to update this version of the application, but I have been working on a more expansive version for that I think I might write it in another language.

# Features

- Plays audio from any .mp3, .ogg, .flacc, and .mp4(.mp4s can only play audio no video)
- Displays metadata for the chosen title, such as:
	- Title
	- Cover
- Allows for changeable volume (0%-100%) and playback rate (0.1x-5.0x)
- Song Looping
- Backtrack
- Forward
- Seek media (Kind of broken)
- Pause and Resume

# Appearance

The color scheme wasn't an expert pick but its a sort of strawberry/strawberry milk. The window itself is borderless and has custom minimize and close buttons along with a now playing/title bar.
There is a lack of a maximize button as the application is meant to be styled like a mp3 player and isn't intended to be resized.

# Usage

When the application is running you can choose a directory that contains your audio or video files you would like to listen to.

Click on the file and press the play button at the bottom.

```python
def open_file(self):
	path = QFileDialog.getExistingDirectory(self, 'Select Folder')

	if path:
		self.current_folder = path
		self.file_list.clear()
		for file_name in os.listdir(path):
			if file_name.lower().endswith(('.mp3', '.ogg', '.wav', '.flac', '.mp4')):
				self.file_list.addItem(file_name)
```

# Known Bugs

With the way the code is set up when you click on an item it sets the list index to that item so if you were to backtrack a song or fast-forward one it will backtrack/fast-forward to the song before/after the song that is selected even if that song isn't currently being played.

The seek media function is somewhat finicky and won't really work whilst a song is playing if you just click.

If the chosen file has no cover or doesn't have the tag it should display an error message but occasionally the display will not update and use the cover of latest song that had a cover.

# Feedback

> *If you have any feedback, Ideas, or criticism, please feel free to start a [Discussion](https://github.com/Krlypumaaa/Oedipus-Audio-App/discussions)!*
