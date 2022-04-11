
import downloader
import argparse
import os


def createOutDir(a_dir_path):
    try:
        os.makedirs(a_dir_path, exist_ok=True)

    except OSError as exc:
        raise

    if not os.access(a_dir_path, os.W_OK):
        raise IOError("No write permission for the destination directory!")


class ReadFromFile(argparse.Action):
    def __call__ (self, parser, namespace, values, option_string = None):
        with values as f:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(f.read().split(), namespace)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description = 'Downloads music from JioSaavn', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-u', '--url', type=str, metavar='', action="append", help='The URL of the song, album or playlist')
    arg_parser.add_argument('-f', '--file', type=open, action=ReadFromFile, metavar='', help='The file containing options')
    arg_parser.add_argument('-o', '--output_dir', type=str, metavar='', nargs='?', default="MusicLibrary", const="MusicLibrary", help='The destination directory to store the downloaded media')

    args = arg_parser.parse_args()

    # Create output directory 
    createOutDir(args.output_dir)
    
    for each_url in args.url:
        each_url = each_url.rstrip()
        #print(each_url)
        song_data, music_type = downloader.get_media_data(each_url)
        #print(song_data)
        d_obj = downloader.Downloader(song_data, music_type, args.output_dir)
        d_obj.downloadMusic()
