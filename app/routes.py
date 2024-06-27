from flask import Blueprint, request, jsonify, send_file, render_template
from .utils import takecommand, translate_text, dic
from gtts import gTTS
import os
from pydub import AudioSegment

main = Blueprint('main', __name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@main.route('/')
def index():
    languages = dic[::2]  
    return render_template('index.html', languages=languages)

@main.route('/api/source-language', methods=['GET'])
def get_source_languages():
    languages = dic[::2]  
    return render_template('source_languages.html', languages=languages)

@main.route('/api/translate', methods=['POST'])
def translate_audio():
    try:
        if 'source_lang' not in request.form:
            print("Error: Missing source language")
            return render_template('error.html', error='Missing source language'), 400

        source_lang = request.form['source_lang'].lower()
        if source_lang not in dic:
            print(f"Error: Invalid source language - {source_lang}")
            return render_template('error.html', error='Invalid source language'), 400

        source_lang_code = dic[dic.index(source_lang) + 1]
        
        query = None
        translated_text = ''

        if 'audio_file' in request.files and request.files['audio_file'].filename != '':
            audio_file = request.files['audio_file']
            audio_path = os.path.join(ROOT_DIR, 'static', 'audio.mp3')

            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            audio_file.save(audio_path)

            sound = AudioSegment.from_file(audio_path)
            wav_audio_path = os.path.join(ROOT_DIR, 'static', 'audio.wav')
            sound.export(wav_audio_path, format="wav")

            query = takecommand(wav_audio_path)

        elif request.form.get('submit_type') == 'speak':
            query = takecommand()

        if query == "None" or query is None:
            print("Error: Failed to recognize speech")
            return render_template('error.html', error='Failed to recognize speech'), 400

        to_lang = request.form.get('to_lang', 'english').lower()
        if to_lang not in dic:
            print(f"Error: Invalid destination language - {to_lang}")
            return render_template('error.html', error='Invalid destination language'), 400

        to_lang_code = dic[dic.index(to_lang) + 1]

        translated_text = translate_text(query, source_lang_code, to_lang_code)

        tts = gTTS(text=translated_text, lang=to_lang_code, slow=False)
        tts.save(os.path.join(ROOT_DIR, 'static', 'translated_audio.mp3'))

        return render_template('translate_result.html', translated_text=translated_text)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('error.html', error='An unexpected error occurred'), 500


@main.route('/api/play-translated', methods=['GET'])
def play_translated_audio():
    audio_file_path = os.path.join(ROOT_DIR, 'static', 'translated_audio.mp3')
    return send_file(audio_file_path)

