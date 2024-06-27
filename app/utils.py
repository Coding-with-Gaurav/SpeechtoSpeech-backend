import speech_recognition as sr
from googletrans import Translator
import os 

from pydub import AudioSegment

# A tuple containing all the languages and codes of the language
dic = ('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am', 'arabic', 'ar', 
       'armenian', 'hy', 'azerbaijani', 'az', 'basque', 'eu', 'belarusian', 'be', 
       'bengali', 'bn', 'bosnian', 'bs', 'bulgarian', 'bg', 'catalan', 'ca', 
       'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)', 'zh-cn', 
       'chinese (traditional)', 'zh-tw', 'corsican', 'co', 'croatian', 'hr', 
       'czech', 'cs', 'danish', 'da', 'dutch', 'nl', 'english', 'en', 
       'esperanto', 'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi', 
       'french', 'fr', 'frisian', 'fy', 'galician', 'gl', 'georgian', 'ka', 
       'german', 'de', 'greek', 'el', 'gujarati', 'gu', 'haitian creole', 'ht', 
       'hausa', 'ha', 'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 'hi', 
       'hmong', 'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo', 'ig', 
       'indonesian', 'id', 'irish', 'ga', 'italian', 'it', 'japanese', 'ja', 
       'javanese', 'jw', 'kannada', 'kn', 'kazakh', 'kk', 'khmer', 'km', 
       'korean', 'ko', 'kurdish (kurmanji)', 'ku', 'kyrgyz', 'ky', 'lao', 'lo', 
       'latin', 'la', 'latvian', 'lv', 'lithuanian', 'lt', 'luxembourgish', 'lb', 
       'macedonian', 'mk', 'malagasy', 'mg', 'malay', 'ms', 'malayalam', 'ml', 
       'maltese', 'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian', 'mn', 
       'myanmar (burmese)', 'my', 'nepali', 'ne', 'norwegian', 'no', 'odia', 'or', 
       'pashto', 'ps', 'persian', 'fa', 'polish', 'pl', 'portuguese', 'pt', 
       'punjabi', 'pa', 'romanian', 'ro', 'russian', 'ru', 'samoan', 'sm', 
       'scots gaelic', 'gd', 'serbian', 'sr', 'sesotho', 'st', 'shona', 'sn', 
       'sindhi', 'sd', 'sinhala', 'si', 'slovak', 'sk', 'slovenian', 'sl', 
       'somali', 'so', 'spanish', 'es', 'sundanese', 'su', 'swahili', 'sw', 
       'swedish', 'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu', 'te', 'thai', 
       'th', 'turkish', 'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 'ug', 
       'uzbek', 'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh', 
       'yiddish', 'yi', 'yoruba', 'yo', 'zulu', 'zu')

def takecommand(audio_path=None):
    r = sr.Recognizer()
    if audio_path:
        with sr.AudioFile(audio_path) as source:
            print("Processing audio file...")
            audio = r.record(source)
    else:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"The User said: {query}\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"
    return query

def recognize_speech(audio_file):
    r = sr.Recognizer()
    audio_text = ""

    # Check file extension to determine format
    _, file_extension = os.path.splitext(audio_file)

    if file_extension.lower() == '.wav':
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
    elif file_extension.lower() in ['.mp3', '.mp4', '.MPEG']:
        # Convert non-WAV formats to WAV for processing
        sound = AudioSegment.from_file(audio_file)
        audio_path = os.path.splitext(audio_file)[0] + '.wav'
        sound.export(audio_path, format="wav")
        
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
        
        # Clean up temporary WAV file
        os.remove(audio_path)
    else:
        raise ValueError("Unsupported file format. Supported formats: WAV, MP3, MP4, MPEG")

    try:
        audio_text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred during speech recognition: {e}")

    return audio_text
def translate_text(text, source_lang_code, to_lang_code):
    translator = Translator()
    text_to_translate = translator.translate(text, src=source_lang_code, dest=to_lang_code)
    return text_to_translate.text
