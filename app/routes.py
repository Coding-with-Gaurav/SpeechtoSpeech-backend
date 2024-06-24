import os
from flask import Blueprint, jsonify, request, send_file, current_app, render_template
from pydub import AudioSegment
from app.utils import recognize_speech, translate_text, synthesize_speech, get_supported_languages

bp = Blueprint('routes', __name__)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'mpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/translate', methods=['POST'])
def translate_speech():
    if 'source_language' not in request.form or 'target_language' not in request.form:
        return jsonify({'error': 'Source and target languages must be specified'}), 400

    source_language = request.form['source_language']
    target_language = request.form['target_language']

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if not allowed_file(audio_file.filename):
        return jsonify({'error': 'Invalid file format. Allowed formats are: wav, mp3, mp4'}), 400
    
    # Save the uploaded file to a temporary location or directly use it
    audio_path = os.path.join(current_app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(audio_path)

    if not os.path.exists(audio_path):
        return jsonify({'error': 'Failed to save uploaded file'}), 500

    # Convert audio to wav format using pydub
    audio = AudioSegment.from_file(audio_path)
    wav_path = os.path.splitext(audio_path)[0] + '.wav'
    audio.export(wav_path, format='wav')

    # Process the converted wav audio file
    try:
        text = recognize_speech(wav_path)
        translated_text = translate_text(text, source_language, target_language)
        output_audio_path = synthesize_speech(translated_text, target_language)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if not os.path.exists(output_audio_path):
        return jsonify({'error': 'Speech synthesis failed'}), 500

    return send_file(output_audio_path, as_attachment=True)

@bp.route('/languages', methods=['GET'])
def supported_languages():
    languages = get_supported_languages()
    return jsonify(languages)
