
# Video to Text Converter

Video to Text Converter is a simple desktop application that extracts spoken words from video files and converts them into text using speech recognition. The app features a user-friendly GUI built with PyQt5 and leverages powerful Python libraries to process video and audio content.

---

## Features

- Select and load `.mp4` video files
- Automatically extract audio and convert it to `.wav`
- Perform speech recognition to transcribe speech into text
- Save the transcription to a text file
- Easy-to-use GUI with status updates and error messages

---

## Built With

- [Python](https://www.python.org/)
- [PyQt5](https://pypi.org/project/PyQt5/) - for the GUI
- [moviepy](https://pypi.org/project/moviepy/) - for audio extraction
- [speechrecognition](https://pypi.org/project/SpeechRecognition/) - for converting speech to text

---

## Installation

### Requirements

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not provided, manually install:

```bash
pip install PyQt5 moviepy SpeechRecognition
```

---

## How to Run

```bash
python app.py
```

Make sure you're in the `Video to Text Converter` directory before running the script.

---

## Project Structure

```
Video to Text Converter/
│
├── app.py                  # Main application file with GUI and logic
```

---

## Screenshots


---

## How It Works

1. User selects an `.mp4` video file.
2. The app extracts the audio from the video and saves it as `speech.wav`.
3. Audio is split (if long) and passed to a speech recognizer.
4. Recognized text is displayed and can be saved.

---

## Troubleshooting

- Ensure the selected video has audible speech.
- For better results, use clear audio in videos.
- Internet connection might be required for some recognizer backends.

---

## Acknowledgements

- Python community and open-source contributors
- [MoviePy](https://zulko.github.io/moviepy/)
- [CMU Sphinx / Google Speech API](https://pypi.org/project/SpeechRecognition/)

