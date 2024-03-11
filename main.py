import sys
from app_communication import *

filename = sys.argv[1]
        
audio_url = upload(filename=filename)
save_transcript(audio_url=audio_url, filename=filename)