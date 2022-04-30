
from jiosaavndownloader import downloader, __version__
import argparse
import os


def create_out_dir(a_dir_path):
    try:
        os.makedirs(a_dir_path, exist_ok=True)

    except OSError as exc:
        raise

    if not os.access(a_dir_path, os.W_OK):
        raise IOError("No write permission for the destination directory!")


def str_to_bool(str_val):
    if isinstance(str_val, bool):
        return str_val
    if str_val.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif str_val.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class ReadFromFile(argparse.Action):
    def __call__ (self, parser, namespace, values, option_string = None):
        with values as f:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(f.read().split(), namespace)


def main():
    arg_parser = argparse.ArgumentParser(description = 'Downloads music from JioSaavn', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    arg_parser.add_argument('-u', '--url', type=str, metavar='', action="append", help='The URL of the song, album or playlist', required=True)
    arg_parser.add_argument('-f', '--file', type=open, action=ReadFromFile, metavar='', help='The file containing options')
    arg_parser.add_argument('-o', '--output_dir', type=str, metavar='', nargs='?', default="MusicLibrary", const="MusicLibrary", help='The destination directory to store the downloaded media')
    arg_parser.add_argument('-a', '--append', type=str_to_bool, metavar='', nargs='?', default=False, const=True, help='Appends/updates the music library instead of duplicate downloading')
    
    args = arg_parser.parse_args()
    
    # Create output directory 
    create_out_dir(args.output_dir)
    
    d_obj = downloader.Downloader(args.url, args.output_dir, args.append)
    d_obj.downloadMusic()


if __name__ == '__main__':
    main()

