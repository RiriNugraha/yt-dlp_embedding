import yt_dlp
import os

def error_message(message):
    print(f"\033[1;31mError: {message}\033[0m")

def get_info(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            error_message(f"Gagal mendapatkan informasi dari URL: {e}")
            return None

def get_title(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Unknown Title')
        except Exception as e:
            error_message(f"Gagal mendapatkan judul dari URL: {e}")
            return None

def show_options():
    print("\033[1;32mItem yang bisa didownload:\033[0m")
    print("----------------------------------------")
    print("\033[1;36m1. Video\033[0m")
    print("\033[1;36m2. Audio\033[0m")
    print("\033[1;36m3. Video + Audio\033[0m")
    print("----------------------------------------")

def download_item(url, item_type, output_dir):
    if item_type == "video":
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(uploader)s-%(resolution)s.%(ext)s'),
        }
    elif item_type == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(uploader)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif item_type == "video_audio":
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(uploader)s-%(resolution)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
    else:
        error_message("Pilihan tidak valid.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            error_message(f"Gagal mendownload: {e}")

def main():
    while True:
        url = input("\033[1;34mMasukkan URL (atau tekan enter untuk keluar): \033[0m")
        if not url:
            print("\033[1;32mTerima kasih! Program selesai.\033[0m")
            break

        output_dir = input("\033[1;34mMasukkan direktori output (default: /storage/emulated/0/Downloads/dvd): \033[0m")
        output_dir = output_dir or "/storage/emulated/0/Downloads/dvd"

        os.makedirs(output_dir, exist_ok=True)

        show_options()

        item_number = input("\033[1;34mPilih item yang ingin didownload (nomor): \033[0m")
        item_type = {
            '1': 'video',
            '2': 'audio',
            '3': 'video_audio'
        }.get(item_number, None)

        if item_type:
            download_item(url, item_type, output_dir)
        else:
            error_message("Pilihan tidak valid.")

if __name__ == "__main__":
    main()