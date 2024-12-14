import yt_dlp
import os

def error_message(message):
    print(f"\033[1;31mError: {message}\033[0m")

def download_audio(url, output_dir, format_choice):
    if format_choice == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(uploader)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format_choice == "m4a":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(uploader)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }
    elif format_choice == "opus":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(uploader)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
            }],
        }
    else:
        error_message("Format tidak valid.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            error_message(f"Gagal mendownload audio: {e}")

def main():
    while True:
        url = input("\033[1;34mMasukkan URL (atau tekan enter untuk keluar): \033[0m")
        if not url:
            print("\033[1;32mTerima kasih! Program selesai.\033[0m")
            break

        output_dir = input("\033[1;34mMasukkan direktori output (default: /storage/emulated/0/Downloads/audio): \033[0m")
        output_dir = output_dir or "/storage/emulated/0/Downloads/audio"

        os.makedirs(output_dir, exist_ok=True)

        print("\033[1;32mFormat yang tersedia:\033[0m")
        print("----------------------------------------")
        print("\033[1;36m1. MP3\033[0m")
        print("\033[1;36m2. M4A\033[0m")
        print("\033[1;36m3. OPUS\033[0m")
        print("----------------------------------------")

        format_number = input("\033[1;34mPilih format audio (nomor): \033[0m")
        format_choice = {
            '1': 'mp3',
            '2': 'm4a',
            '3': 'opus'
        }.get(format_number, None)

        if format_choice:
            download_audio(url, output_dir, format_choice)
        else:
            error_message("Pilihan format tidak valid.")

if __name__ == "__main__":
    main()