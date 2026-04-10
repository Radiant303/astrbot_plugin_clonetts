import base64
from io import BytesIO
from pydub import AudioSegment
def mp3_base64_to_wav_base64(mp3_b64: str) -> str:
    mp3_data = base64.b64decode(mp3_b64)
    audio = AudioSegment.from_file(BytesIO(mp3_data), format="mp3")
    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    return base64.b64encode(wav_io.getvalue()).decode()