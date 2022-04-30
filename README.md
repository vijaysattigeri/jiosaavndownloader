# jiosaavndownloader
Downloads high quality songs from JioSaavn

## Description
The application downloads the songs(single, album & playlist) from JioSaavn and adds all the necessary metadata to the downloaded media. This application uses the unofficial API [JioSaavnAPI](https://github.com/cyberboysumanjay/JioSaavnAPI) written by [Sumanjay](https://github.com/cyberboysumanjay)

The media will be downloaded and placed in the specified(through -o) directory.

## Installation
1. Clone the repository (for latest source) OR download the release source

> git clone https://github.com/vijaysattigeri/jiosaavndownloader

2. [Optional] Create a python virtual environment and activate it

3. Install local package through pip

> pip3 install .

OR
Install requirements manually. (If you don't want to install this package by pip)

> pip3 install -r requirements.txt


4. You're all set.

## Usage
1. If installed through pip

        jiosaavndownloader -h
        usage: jiosaavndownloader [-h] [-v] -u  [-f] [-o ] [-a ]

        Downloads music from JioSaavn

        optional arguments:
            -h, --help            show this help message and exit
            -v, --version         show program's version number and exit
            -u , --url            The URL of the song, album, playlist or artist(default: None)
            -f , --file           The file containing options (default: None)
            -o [], --output_dir []
                                The destination directory to store the downloaded media (default: MusicLibrary)
            -a [], --append []  Appends/updates the music library instead of duplicate downloading (default: False)

        -------------------------------------------------------------------------------------
        Ex:
        > jiosaavndownloader -u https://www.jiosaavn.com/song/feel-nothing/GTATcjpKUGY


2. If not installed and in source code directory

        python -m jiosaavndownloader -h
        usage: __main__.py [-h] [-v] -u  [-f] [-o ] [-a ]

        Downloads music from JioSaavn

        optional arguments:
            -h, --help            show this help message and exit
            -v, --version         show program's version number and exit
            -u , --url            The URL of the song, album, playlist or artist(default: None)
            -f , --file           The file containing options (default: None)
            -o [], --output_dir []
                                The destination directory to store the downloaded media (default: MusicLibrary)
            -a [], --append []  Appends/updates the music library instead of duplicate downloading (default: False)

        -------------------------------------------------------------------------------------
        Ex:
        > python -m jiosaavndownloader -u https://www.jiosaavn.com/song/feel-nothing/GTATcjpKUGY
      
      
## License
The project itself is licensed under **Mozilla Public License Version 2.0** and the API is licensed under **MIT**
