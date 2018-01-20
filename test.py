
def run_quickstart():
    # Imports the Google Cloud client library
    # [START migration_import]
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # [END migration_import]
    import os
    import io
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\Python27\workspace\weakness.json"
    print os.environ.keys()
    client = speech.SpeechClient()
    # [END migration_client]
    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),

        'kon.raw')

    print file_name

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]


if __name__ == '__main__':
    run_quickstart()