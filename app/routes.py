from flask import Blueprint, request, jsonify, send_file, render_template
from .utils import recognize_speech, translate_text, dic  
from gtts import gTTS
import os
import traceback

main = Blueprint('main', __name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
current_audio_path = None  # To store the current audio file path

@main.route('/')
def index():
    languages = dic[::2]
    return render_template('index.html', languages=languages)

@main.route('/api/source-language', methods=['GET'])
def get_source_languages():
    languages = dic[::2]
    return render_template('source_languages.html', languages=languages)

@main.route('/api/recognize-speech', methods=['POST'])
def recognize_speech_endpoint():
    global current_audio_path
    try:
        # Check if audio file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400

        audio_file = request.files['file']

        # Save the uploaded audio file
        audio_path = os.path.join(ROOT_DIR, 'uploads', audio_file.filename)
        audio_file.save(audio_path)

        # Recognize speech from the uploaded audio file
        recognized_text = recognize_speech(audio_path)

        # Delete the uploaded audio file after processing
        os.remove(audio_path)

        if recognized_text == "":
            return jsonify({'error': 'Failed to recognize speech'}), 400

        current_audio_path = audio_path  # Store for translation if needed
        return jsonify({'recognized_text': recognized_text}), 200

    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

@main.route('/api/translate', methods=['POST'])
def translate_audio():
    global current_audio_path
    try:
        if not current_audio_path:
            print("Error: No audio file to translate")
            return jsonify({'error': 'No audio file to translate'}), 400

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

        translated_text = translate_text(current_audio_path, source_lang_code, to_lang_code)

        tts = gTTS(text=translated_text, lang=to_lang_code, slow=False)
        audio_path = os.path.join(ROOT_DIR, 'static', 'translated_audio.mp3')
        tts.save(audio_path)

        return jsonify({
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
    global current_audio_path
    current_audio_path = None
    return jsonify({'message': 'Audio file reset successful'}), 200
