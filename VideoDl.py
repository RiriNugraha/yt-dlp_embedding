import yt_dlp
import os

def error_message(message):
    print(f"\033[1;31mError: {message}\033[0m")

def get_video_audio_info(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            video_formats = [f for f in formats if f.get('vcodec') != 'none']
            audio_formats = [f for f in formats if f.get('acodec') != 'none']
            return video_formats, audio_formats
    except Exception as e:
        error_message(f"Gagal mendapatkan informasi dari URL: {str(e)}")
        return None, None

def get_title(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('title', 'Judul tidak ditemukan')
    except Exception as e:
        error_message(f"Gagal mendapatkan judul dari URL: {str(e)}")
        return None

def download_video_audio(url, output_dir):
    video_formats, audio_formats = get_video_audio_info(url)
    if not video_formats or not audio_formats:
        return

    title = get_title(url)

    # Menampilkan kualitas video yang tersedia
    print(f"\033[1;32mKualitas video yang tersedia:\033[0m")
    for i, f in enumerate(video_formats):
        print(f"{i + 1}. {f.get('format')} - {f.get('ext')} - {f.get('height', 'N/A')}p")

    try:
        video_choice = int(input(f"\033[1;34mPilih kualitas video (nomor): \033[0m"))
        selected_video_format = video_formats[video_choice - 1]
    except (ValueError, IndexError):
        error_message("Pilihan tidak valid.")
        return

    # Menampilkan kualitas audio yang tersedia
    print(f"\033[1;32mKualitas audio yang tersedia:\033[0m")
    for i, f in enumerate(audio_formats):
        print(f"{i + 1}. {f.get('format')} - {f.get('ext')} - {f.get('abr', 'N/A')} kbps")

    try:
        audio_choice = int(input(f"\033[1;34mPilih kualitas audio (nomor): \033[0m"))
        selected_audio_format = audio_formats[audio_choice - 1]
    except (ValueError, IndexError):
        error_message("Pilihan tidak valid.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Template nama file sesuai dengan skrip Bash Anda
    output_template = os.path.join(output_dir, '%(title)s-%(uploader)s-%(resolution)s.%(ext)s')

    download_command = {
        'format': f"{selected_video_format.get('format_id')}+{selected_audio_format.get('format_id')}",
        'outtmpl': output_template,
        'quiet': False,
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
        ],
    }

    with yt_dlp.YoutubeDL(download_command) as ydl:
        try:
            ydl.download([url])
            print(f"\033[1;32mDownload selesai: {title}\033[0m")
        except Exception as e:
            error_message(f"Gagal mendownload video + audio: {str(e)}")

def main():
    while True:
        url = input("\033[1;34mMasukkan URL (atau tekan enter untuk keluar): \033[0m")
        if not url:
            print("\033[1;32mTerima kasih! Program selesai.\033[0m")
            break

        output_dir = input("\033[1;34mMasukkan direktori output (default: /storage/emulated/0/Downloads/video): \033[0m")
        output_dir = output_dir or "/storage/emulated/0/Downloads/video"

        download_video_audio(url, output_dir)

if __name__ == "__main__":
    main()