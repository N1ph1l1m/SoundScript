<h1>SoundScript</h1>
<p>SoundScript is a project developed to convert speech to text using advanced voice recognition technologies. The program's interface is based on the Tkinter library, which provides an intuitive and easy-to-use graphical interface. The voice-to-text conversion technology is based on the <a href="https://github.com/openai/whisper">Whisper</a> model from OpenAI, which guarantees high recognition accuracy and reliability. SoundScript provides users with a convenient tool for efficient and accurate conversion of audio recordings into text documents, facilitating the tasks of transcribing and analyzing audio data.</p>

<h2>Approach</h2>    

![image](https://github.com/user-attachments/assets/57838958-53b7-4071-a562-9bbd34efc123)
<p>A Transformer sequence-to-sequence model is trained on various speech processing tasks, including multilingual speech recognition, speech translation, spoken language identification, and voice activity detection. These tasks are jointly represented as a sequence of tokens to be predicted by the decoder, allowing a single model to replace many stages of a traditional speech-processing pipeline. The multitask training format uses a set of special tokens that serve as task specifiers or classification targets.</p>

<h2>Available models and languages</h2>
<p>
  There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model; actual speed may vary depending on many factors including the available hardware.
</p>

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |


The `.en` models for English-only applications tend to perform better, especially for the `tiny.en` and `base.en` models. We observed that the difference becomes less significant for the `small.en` and `medium.en` models.

Whisper's performance varies widely depending on the language. The figure below shows a performance breakdown of `large-v3` and `large-v2` models by language, using WERs (word error rates) or CER (character error rates, shown in *Italic*) evaluated on the Common Voice 15 and Fleurs datasets. Additional WER/CER metrics corresponding to the other models and datasets can be found in Appendix D.1, D.2, and D.4 of [the paper](https://arxiv.org/abs/2212.04356), as well as the BLEU (Bilingual Evaluation Understudy) scores for translation in Appendix D.3.

![WER breakdown by language](https://github.com/openai/whisper/assets/266841/f4619d66-1058-4005-8f67-a9d811b77c62)


<h2> 1. Installation with virtual environments</h2>
<ul>
  <p>Open the terminal (command prompt).</p>
  <p>Navigate to your project directory.</p>
  <p>Create a virtual environment using the command</p>
  
    python -m venv venv
  <p>Activate the virtual environment:</p>
    <p>For Windows</p>
    
    venv\Scripts\activate
  <p>For macOS/Linux</p>
    
    source venv/bin/activate
  <h2> Installing Packages from requirements.txt:</h2>
  <p>Ensure the virtual environment is active (the virtual environment's name, such as (venv), should be displayed in the terminal).</p>
  <p>Install all the required packages using the command</p>

    pip install -r requirements.txt
</ul>

<h2> 2. Installing the ffmpeg component</h2>
  <p>It also requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:</p>
   
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg

    # on Arch Linux
    sudo pacman -S ffmpeg
    
    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg
    
    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg
    
    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
<p>Or You can install FFmpeg manually by downloading it from the official website: https://www.ffmpeg.org/download.html. </p>
<p>Alternatively, you can clone the FFmpeg repository using the command:</p>

    git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
<p>In the bin folder, copy the three files: <ul>
  <li>ffmpeg.exe;</li>
   <li>ffplay.exe;</li>
  <li>ffprobe.exe.</li>
  </ul>
and place them in the Scripts folder of your Python environment.</p>
