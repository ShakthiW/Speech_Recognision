import requests
import time
from api_secrets import API_KEY_ASSEMBLYAI


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY_ASSEMBLYAI}

# upload
def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(5242880)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(filename))
    # print(upload_response.json())
    audio_url = upload_response.json()['upload_url']
    
    return audio_url


# start transcription
def transcribe(audio_url):
    json = {
        'audio_url': audio_url
    }
    
    transcript_response = requests.post(transcription_endpoint, json=json, headers=headers)
    job_id = transcript_response.json()['id']
    return job_id

# transcript_id = transcribe(audio_url=audio_url)
# print(transcript_id)

# poll for transcription

def poll(transcript_id):
    polling_endpoint = transcription_endpoint + '/' + transcript_id
    polling_res = requests.get(polling_endpoint, headers=headers)
    # print(polling_res.json())
    return polling_res.json()


def get_transcription_result_url(audio_url):
    transcribe_id = transcribe(audio_url)
    
    # loop until transcription is completed
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            # print("completed")
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        
        # wait 30 seconds before polling again
        print("waiting 10 seconds...")
        time.sleep(10)
        
        



# save transcription
def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)
    if data:
        text_filename = filename + '.txt'
        with open(text_filename, 'w') as f:
            f.write(data['text'])
            
        print(f"Transcription saved to {text_filename}")
        
    elif error:
        print(f"Error: {error}")