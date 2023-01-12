import sys
import os
# ------------------------------------------------------------- #
TORRENT_DIR = r"C:\Users\LEGION\AppData\Roaming\uTorrent"
# ------------------------------------------------------------- #
def exit_utorrent():
    os.system('TASKKILL /IM "utorrent.exe" /T /F')

def rename_files(dir):
    movie_name = os.path.basename(dir)

    for file in os.listdir(dir):
        ext = file.split(".")[-1]
        src = os.path.join(dir, file)

        if (ext in {"mp4", "srt"}):
            dst = os.path.join(dir, f"{movie_name}.{ext}")
            os.rename(src, dst)
        else:
            os.remove(src)

def remove_torrent_file(file_name):
    file_name += ".torrent" 
    file_path = os.path.join(TORRENT_DIR, file_name)
    os.remove(file_path)
# ------------------------------------------------------------- #
if (__name__ == "__main__"):
    try:
        input("Close UTrorrent ")
        
        movie_dir = sys.argv[1]
        file_name = sys.argv[2]

        if (os.path.isdir(movie_dir)):
            rename_files(movie_dir)

    except Exception as e:
        input(str(e))
# ------------------------------------------------------------- #