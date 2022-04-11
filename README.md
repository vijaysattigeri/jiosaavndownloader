# jiosaavndownloader
Downloads high quality songs from JioSaavn

## Description
The application downloads the songs(single, album & playlist) from JioSaavn and adds all the necessary metadata to the downloaded media. This application uses the unofficial API [JioSaavnAPI](https://github.com/cyberboysumanjay/JioSaavnAPI) written by [Sumanjay](https://github.com/cyberboysumanjay)

The media will be downloaded and placed in a directory called `MusicLibrary` which will be created in present working directory.

## Installation
1. Clone the repository

> git clone https://github.com/vijaysattigeri/jiosaavndownloader

2. [Optional] Create a python virtual environment and activate it

3. Install requirements OR install local package through pip

> pip3 install -r requirements.txt

    OR 

> pip3 install .

4. You're all set.

## Usage

    python jiosaavndownloader -h
    usage: jiosaavndownloader [-h] [-u] [-f] [-o ]

    Downloads music from JioSaavn

    optional arguments:
        -h, --help            show this help message and exit
        -u , --url            The URL of the song, album or playlist (default: None)
        -f , --file           The file containing options (default: None)
        -o [], --output_dir []
                              The destination directory to store the downloaded media (default: MusicLibrary)

      -------------------------------------------------------------------------------------
      Ex:
      > python jiosaavndownloader -u https://www.jiosaavn.com/song/feel-nothing/GTATcjpKUGY
      
      
## License
The project itself is licensed under **Mozilla Public License Version 2.0** and the API is licensed under **MIT**
