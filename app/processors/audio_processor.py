from pathlib import Path
import subprocess

class AudioProcessor:
    def __init__(self, input_audio, output_dir):
        self.input_audio = Path(input_audio)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_demucs(self):
        """Process audio using Demucs to separate vocals"""
        try:
            # Use default model (htdemucs) without MP3 output to avoid diffq dependency
            subprocess.run([
                "demucs",
                "--two-stems=vocals",
               # "-n", "mdx_extra_q",
                "-o", str(self.output_dir),
                str(self.input_audio)
            ], check=True)
            print("Demucs processing completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during Demucs execution: {e}")
            return False

    def get_vocals_path(self):
        """Get path to the separated vocals file"""
        # Path for htdemucs model output
        vocals_path = self.output_dir / "htdemucs" / Path(self.input_audio.stem) / "vocals.wav"
        if vocals_path.exists():
            print(f"Vocals found at: {vocals_path}")
            return str(vocals_path)
        print("Vocals file not found")
        return None

    def get_no_vocals_path(self):
        """Get path to the no-vocals (instrumental) file"""
        # Path for htdemucs model output
        no_vocals_path = self.output_dir / "htdemucs" / Path(self.input_audio.stem) / "no_vocals.wav"
        if no_vocals_path.exists():
            print(f"No-vocals track found at: {no_vocals_path}")
            return str(no_vocals_path)
        print("No-vocals file not found")
        return None

    def cleanup(self):
        """Remove temporary audio files"""
        if self.input_audio.exists():
            self.input_audio.unlink()
        print("Temporary audio files cleaned up")