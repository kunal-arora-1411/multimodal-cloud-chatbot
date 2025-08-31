import pyttsx3

def text_to_speech(text: str, output_file: str) -> str:
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file
