from flask import Blueprint, request, jsonify, send_file, render_template
from .utils import takecommand, translate_text, dic
from gtts import gTTS
import os
from pydub import AudioSegment

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', languages=dic[::2])

@main.route('/api/source-language', methods=['GET'])
def get_source_languages():
    return jsonify({'languages': dic[::2]})

@main.route('/api/translate', methods=['POST'])
def translate_audio():
    if 'source_lang' not in request.form:
        return jsonify({'error': 'Missing source language'}), 400

    source_lang = request.form['source_lang'].lower()
    if source_lang not in dic:
        return jsonify({'error': 'Invalid source language'}), 400

    source_lang_code = dic[dic.index(source_lang) + 1]
    
    query = None
    if 'audio_file' in request.files and request.files['audio_file'].filename != '':
        audio_file = request.files['audio_file']
        audio_path = 'static/audio.mp3'

        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        audio_file.save(audio_path)

        sound = AudioSegment.from_file(audio_path)
        wav_audio_path = 'static/audio.wav'
        sound.export(wav_audio_path, format="wav")

        query = takecommand(wav_audio_path)

    elif request.form.get('submit_type') == 'speak':
        query = takecommand()

    if query == "None" or query is None:
        return jsonify({'error': 'Failed to recognize speech'}), 400

    to_lang = request.form.get('to_lang', 'english').lower()
    if to_lang not in dic:
        return jsonify({'error': 'Invalid destination language'}), 400

    to_lang_code = dic[dic.index(to_lang) + 1]

    translated_text = translate_text(query, source_lang_code, to_lang_code)

    tts = gTTS(text=translated_text, lang=to_lang_code, slow=False)
    tts.save('static/translated_audio.mp3')

    return jsonify({'translated_text': translated_text})

@main.route('/api/play-translated', methods=['GET'])
def play_translated_audio():
    return send_file('static/translated_audio.mp3', as_attachment=True)
