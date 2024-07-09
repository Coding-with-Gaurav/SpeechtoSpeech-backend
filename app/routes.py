from flask import Blueprint, request, jsonify, send_file, render_template
from .utils import takecommand, translate_text, dic
from gtts import gTTS
import os
import traceback

main = Blueprint('main', __name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
current_query = None  # To store the current recognized query

@main.route('/')
def index():
    languages = dic[::2]
    return render_template('index.html', languages=languages)

@main.route('/api/source-language', methods=['GET'])
def get_source_languages():
    languages = dic[::2]
    return render_template('source_languages.html', languages=languages)

@main.route('/api/start-recording', methods=['POST'])
def start_recording():
    global current_query
    try:
        current_query = takecommand()
        if current_query == "None" or current_query is None:
            print("Error: Failed to recognize speech")
            return jsonify({'error': 'Failed to recognize speech'}), 400

        return jsonify({'recognized_text': current_query}), 200
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

@main.route('/api/translate', methods=['POST'])
def translate_audio():
    global current_query
    try:
        if not current_query:
            print("Error: No recognized text to translate")
            return jsonify({'error': 'No recognized text to translate'}), 400

        source_lang = request.form.get('source_lang', 'english').lower()
        if source_lang not in dic:
            print(f"Error: Invalid source language - {source_lang}")
            return jsonify({'error': 'Invalid source language'}), 400

        source_lang_code = dic[dic.index(source_lang) + 1]

        to_lang = request.form.get('to_lang', 'english').lower()
        if to_lang not in dic:
            print(f"Error: Invalid destination language - {to_lang}")
            return jsonify({'error': 'Invalid destination language'}), 400

        to_lang_code = dic[dic.index(to_lang) + 1]

        print(f"Recognized text: {current_query}")
        translated_text = translate_text(current_query, source_lang_code, to_lang_code)

        tts = gTTS(text=translated_text, lang=to_lang_code, slow=False)
        audio_path = os.path.join(ROOT_DIR, 'static', 'translated_audio.mp3')
        tts.save(audio_path)

        return jsonify({
            'recognized_text': current_query,
            'translated_text': translated_text,
            'audio_path': 'static/translated_audio.mp3'
        }), 200

    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

@main.route('/api/play-translated', methods=['GET'])
def play_translated_audio():
    audio_file_path = os.path.join(ROOT_DIR, 'static', 'translated_audio.mp3')
    return send_file(audio_file_path)

@main.route('/api/reset', methods=['POST'])
def reset():
    global current_query
    current_query = None
    return jsonify({'message': 'Query reset successful'}), 200
