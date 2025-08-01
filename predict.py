import os
from cog import BasePredictor, Input, Path
from TTS.api import TTS
from moviepy.editor import TextClip, CompositeVideoClip

class Predictor(BasePredictor):
    def setup(self):
        # Load TTS model
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=True)

    def predict(
        self,
        script: str = Input(description="Enter your voiceover script"),
        width: int = Input(default=1080),
        height: int = Input(default=1920),
        duration: int = Input(default=8, description="Video duration in seconds")
    ) -> Path:
        # Step 1: Generate speech
        audio_path = "pam2_voice.wav"
        self.tts.tts_to_file(text=script, file_path=audio_path)

        # Step 2: Create simple animated text for video
        clip = TextClip(script, fontsize=70, color='white', size=(width, height)).set_duration(duration)
        video = CompositeVideoClip([clip])
        video_path = "pam2_output.mp4"
        video.write_videofile(video_path, fps=24)

        return Path(video_path)
