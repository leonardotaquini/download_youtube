import pytube
def download_mp3(url):

    try:
        link = str(url)
        yt = pytube.YouTube(link)
        # audio = yt.streams.filter(only_audio=True).first()
        audio = yt.streams.get_audio_only()

        if audio is None:
            print("Audio stream not found for this video. Downloading may not be possible.")
            exit()

        # audio.download( filename=f"./static/{ audio.title }.mp3")
        audio.download( filename=f"static/{ audio.title }.mp3")
        return audio.title
          

    except Exception as e:
            print("An error occurred during download:", e)


    except Exception as e: 
        print("Unexpected error:", e)
