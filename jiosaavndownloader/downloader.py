from api_src import jiosaavn
import mutagen.mp4
import imghdr
import requests
import os
import re
import enum
import ntpath
import errno
import tqdm


class MusicType(enum.Enum):
   SINGLE = 1
   ALBUM = 2
   PLAYLIST = 3

class Downloader:
    def __init__(self, a_json_data, a_music_type, a_out_dir):
        self.json_data = a_json_data
        self.music_type = a_music_type
        self.output_dir = a_out_dir

    def getLegalPathString(self, a_path_str):
        # Define replacements here
        # Format: "_char_<char_name>_"
        substitutes = {
            # Linux/Unix/Mac
            "/"  : "_char_fslash_", 
            "\\" : "_char_bslash_", 

            # Windows
            "<"  : "_char_lt_",
            ">"  : "_char_gt_",
            ":"  : "_char_colon_",
            "\"" : "_char_dquote_",
            "|"  : "_char_pipe_",
            "?"  : "_char_question_",
            "*"  : "_char_asterisk_"
        }

        for k, v in substitutes.items():
            a_path_str = a_path_str.replace(k, v)

        return a_path_str
    
    def getValidAndUniqueFileName(self, a_file_name):
        title_str = ntpath.basename( a_file_name ) # 'ntpath' provides platform independent functionality
        sanitized_title = self.getLegalPathString( title_str )
        a_file_name = a_file_name.replace(title_str, sanitized_title)
        file_name, ext = os.path.splitext( a_file_name)

        counter = 2
        while os.path.exists(a_file_name):
            a_file_name = file_name + " (" + str(counter) + ")" + ext
            counter += 1
        return a_file_name 

    def downloadWithProgress(self, file_name, object_url):
        ret_val = True
        resp = requests.get( object_url, stream=True )
        total_size_in_bytes= int(resp.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(file_name, 'wb') as fh:
            for chunk_data in resp.iter_content(block_size):
                progress_bar.update(len(chunk_data))
                fh.write(chunk_data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print(f"ERROR, something went wrong while downloading '{file_name}'")
            ret_val = False

        fh.close()
        return ret_val


    def downloadMusic(self):
        if self.music_type == MusicType.SINGLE:
            self.downloadAndAddMetadata(self.output_dir, None, 1, 1)
        elif self.music_type == MusicType.ALBUM or self.music_type == MusicType.PLAYLIST:
            out_sub_dir_pl_alb = os.path.join(self.output_dir, f'{self.getLegalPathString(self.json_data["name"]) if self.music_type == MusicType.ALBUM else self.json_data["listname"]} ({self.json_data["year"] if self.music_type == MusicType.ALBUM else "Playlist" })')
            os.makedirs(out_sub_dir_pl_alb, exist_ok=True)
            
            # Download album cover art
            cover_img = requests.get( self.json_data["image"], stream=True )
            img_file_name_tmp = os.path.join(out_sub_dir_pl_alb, "tmp_albm_img.unknown")
            img_fh = open(img_file_name_tmp, "wb")
            img_fh.write(cover_img.content)
            img_fh.close()
            # Detect actual extension
            img_file_name = os.path.join(out_sub_dir_pl_alb, f'Cover.{imghdr.what(img_file_name_tmp)}')
            os.rename(img_file_name_tmp, img_file_name)

            i = 1
            for song_obj in self.json_data["songs"]:
                self.downloadAndAddMetadata(out_sub_dir_pl_alb, song_obj, i, len(self.json_data["songs"]))
                i = i + 1

    def downloadAndAddMetadata(self, out_dir, song_obj, tr_no, total_tr):
        if self.music_type == MusicType.SINGLE and song_obj == None:
            song_obj = self.json_data

        # Download audio file
        max_str_len = len(str(total_tr))
        track_prefix = str(tr_no).zfill(max_str_len) if max_str_len > 1 else  str(tr_no).zfill(2)
        audio_file = f'{track_prefix}. {song_obj["song"]}.m4a'
        audio_file = os.path.join(out_dir, audio_file)
        # Get unique name if the name already exists
        audio_file = self.getValidAndUniqueFileName(audio_file)
        print(f"Downloading file '{audio_file}' ...")
        if self.downloadWithProgress(audio_file, song_obj["media_url"]):
            print(f"File '{audio_file}' downloaded successfully")
        else:
            print(f"File '{audio_file}' could not be downloaded!")

        # Download song cover art
        cover_img = requests.get( song_obj["image"], stream=True )
        img_file_name_tmp = os.path.join(out_dir, "tmp_song_img.unknown")
        img_fh = open(img_file_name_tmp, "wb")
        img_fh.write(cover_img.content)
        img_fh.close()
        # Detect actual extension
        act_img_ext = imghdr.what(img_file_name_tmp)
        if act_img_ext:
            img_file_name = os.path.join(out_dir, f'SongCover.{act_img_ext}')
            os.rename(img_file_name_tmp, img_file_name)
            cover_format = mutagen.mp4.MP4Cover.FORMAT_PNG
            if act_img_ext.casefold() == "jpeg".casefold() or act_img_ext.casefold() == "jpg":
                cover_format = mutagen.mp4.MP4Cover.FORMAT_JPEG
            
        else:
            img_file_name = img_file_name_tmp
            print(f"Could not download Cover file! Adding album art to mp4 metadata will be skipped")

        audio_fh = open(audio_file, "rb+")
        m4a_metadata = mutagen.mp4.MP4(audio_file)
        m4a_metadata['\xa9nam'] = song_obj["song"]
        m4a_metadata['\xa9alb'] = song_obj["album"]
        m4a_metadata['\xa9ART'] = song_obj["primary_artists"]
        m4a_metadata['aART'] = song_obj["primary_artists"]
        m4a_metadata['\xa9day'] = song_obj["year"]
        m4a_metadata['cprt'] = song_obj["copyright_text"]
        m4a_metadata['\xa9cmt'] = "Downloaded from JioSaavn"
        # Add lyrics if it available
        if song_obj["lyrics"]:
            formatted_lyrics = song_obj["lyrics"]
            formatted_lyrics = re.sub(r'<br */? *>', os.linesep, formatted_lyrics)
            m4a_metadata['\xa9lyr'] = formatted_lyrics

        m4a_metadata['trkn'] = [(tr_no, total_tr)]
        if act_img_ext:
            with open(img_file_name, 'rb') as img_fh:
                albumart = mutagen.mp4.MP4Cover(img_fh.read(), imageformat=cover_format)
                m4a_metadata.tags['covr'] = [albumart]

        m4a_metadata.save()
        audio_fh.close()
        print(f"Added metadata to '{audio_file}'")

        # Cleanup
        os.remove(img_file_name)



from traceback import print_exc

def get_media_data(my_req):
    lyrics = True
    query = my_req

    if 'saavn' not in query:
        return jiosaavn.search_for_song(query,lyrics,True), 
    try:
        if '/song/' in query:
            song_id = jiosaavn.get_song_id(query)
            song = jiosaavn.get_song(song_id,lyrics)
            return song, MusicType.SINGLE

        elif '/album/' in query:
            id = jiosaavn.get_album_id(query)
            album = jiosaavn.get_album(id,lyrics)
            #return songs
            return album, MusicType.ALBUM

        elif '/playlist/' or '/featured/' in query:
            id = jiosaavn.get_playlist_id(query)
            songs = jiosaavn.get_playlist(id,lyrics)
            return songs, MusicType.PLAYLIST

    except Exception as e:
        print_exc()
        error = {
            "status": True,
            "error":str(e)
        }
        return error
    return None
