# import json # Only needed if you want to save the response as a JSON file
import os
import time
from datetime import timedelta

from deepgram import Deepgram
from dotenv import dotenv_values
from tinytag import TinyTag


config = dotenv_values(".env")
DEEPGRAM_API_KEY = config["DEEPGRAM_API_KEY"]


input_folder = "./input/"
output_folder = "./output/"
valid_extensions = [
    ".mp3",
    ".wav",
    ".m4a",
]  # Add or modify the file extensions as needed
cost_per_minute = 0.0043  # Nova model

# Create folders if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(input_folder, exist_ok=True)


# Deepgram API
def transcribe_audio(file_path, file_extension):
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    mimetype = f"audio/{file_extension[1:]}"  # Remove the dot from the file extension

    with open(file_path, "rb") as audio:
        source = {"buffer": audio, "mimetype": mimetype}
        options = {
            "paragraphs": True,
            "punctuate": True,
            "model": "nova",
            "language": "en-US",
        }

        print("Requesting transcript...")
        response = dg_client.transcription.sync_prerecorded(source, options)
        # Use paragraphs
        paragraphs_data = response["results"]["channels"][0]["alternatives"][0][
            "paragraphs"
        ]["paragraphs"]
        return paragraphs_data
        # No paragraphs
        # transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]


def main():
    transcription_count = 0
    total_cost = 0
    total_time = 0

    print("--------------------------------")  # Add horizontal line at the start

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file has a valid audio file extension
        file_extension = os.path.splitext(filename)[1]
        if file_extension in valid_extensions:
            file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(
                output_folder, f"{os.path.splitext(filename)[0]}_transcript.txt"
            )

            # Transcribe the audio file
            start_time = time.time()
            paragraphs_data = transcribe_audio(file_path, file_extension)
            end_time = time.time()

            processing_time = timedelta(seconds=end_time - start_time)
            total_time += processing_time.total_seconds()

            # Extract hours, minutes, and seconds from the processing_time
            hours, remainder = divmod(processing_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{int(processing_time.microseconds / 10000):02d}"

            # Get the duration using TinyTag
            audio = TinyTag.get(file_path)
            duration = audio.duration / 60  # Convert seconds to minutes

            # Calculate the cost
            cost = duration * cost_per_minute
            total_cost += cost

            # Save the transcription to the output folder
            separator = "\n--------------------------------\n"

            with open(output_file_path, "a", encoding="utf-8") as f:
                f.write(separator)
                for paragraph in paragraphs_data:
                    sentences = paragraph["sentences"]
                    for sentence in sentences:
                        f.write(sentence["text"] + " ")
                    f.write("\n\n")
                f.write(separator)
                f.write(f"\nCost: ~${cost:.4f}\n")
                f.write(f"Time: {formatted_time}\n")

            transcription_count += 1
            print(
                f"Transcript #{transcription_count} for '{filename}' "
                f"has been saved. Cost: ~${cost:.4f} "
                f"Time taken: {formatted_time}"
            )
        else:
            print(f"{filename} has an unsupported file extension. Skipping...")

    print(f"\nFinished processing {transcription_count} audio files.\n")
    print(f"Total cost: ~${total_cost:.4f}")
    total_time_formatted = f"{int(total_time // 3600):02d}:{int((total_time % 3600) // 60):02d}:{int(total_time % 60):02d}.{int((total_time % 1) * 100):02d}"
    print(f"Total time: {total_time_formatted}")

    print("--------------------------------")  # Add horizontal line at the end


if __name__ == "__main__":
    main()
