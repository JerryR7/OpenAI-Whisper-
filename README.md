# OpenAI Whisper Transcription Tool

## Overview

The OpenAI Whisper Transcription Tool is a Python application that leverages the OpenAI Whisper API to transcribe audio files. This tool allows you to specify the language, choose whether to generate a timeline, and then initiate the transcription process.

## Prerequisites

Before using this tool, ensure you have completed the following steps:

1. Register for an OpenAI account and obtain an API key.

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/JerryR7/OpenAI-Whisper-Transcription-Tool.git
   ```

2. Configure the API key: Open the `transcribe.py` file and provide your OpenAI API key in the `openai.api_key` variable.

3. If you have the pre-built executable version:

   - Navigate to the `dist` folder.
   - Run the executable program to start the transcription tool.

   ```bash
   cd dist
   ./transcribe (or transcribe.exe on Windows)
   ```

   Follow the on-screen prompts to select the audio file, choose the language, and decide whether to generate a timeline for transcription.

4. If you want to run the tool from source:

   - Run the transcription tool:

     ```bash
     python transcribe.py
     ```

   Follow the on-screen prompts to select the audio file, choose the language, and decide whether to generate a timeline for transcription.

5. The transcription result will be displayed in the console.

## License

This code is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

If you encounter any issues or wish to improve this tool, feel free to submit issues or send pull requests. We welcome your contributions!

## Contact

If you have any questions or need assistance, please don't hesitate to contact us.

## Acknowledgments

Special thanks to OpenAI for providing a powerful speech transcription API.

We hope this tool helps you transcribe audio files efficiently using OpenAI Whisper. Feel free to customize and extend the code to suit your specific requirements.
