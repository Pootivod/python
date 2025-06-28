from dotenv import load_dotenv
import sys
import os
import traceback
import requests
import io
import json
from yt_dlp import YoutubeDL
from PIL import Image, ImageOps
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TYER, COMM, TXXX, WOAS, APIC
from mutagen.mp3 import MP3

if __name__ == "__main__":
        url = sys.argv[1] if len(sys.argv) > 1 else input("Enter YouTube URL: ")
        if not url.replace("www.", "").startswith(tuple(ytb_link)):
            print("Invalid YouTube URL. Please provide a valid link.")
            sys.exit(1)
        download_url(url)

class Download:
    load_dotenv("./configs/.env")
    root = os.getenv("ROOT")
    download3 = root + os.getenv("DOWNLOAD3")
    download4 = root + os.getenv("DOWNLOAD4")
    ytb_link = ["https://youtube.com/watch?v=", "https://music.youtube.com/watch?v=", "https://music.youtube.com/playlist?list=", "https://youtube.com/playlist?list=", "https://youtu.be/"]

    ydl_opts = {
        'ffmpeg_location' : "/usr/bin/ffmpeg",  # Path to ffmpeg executable
        'no_post_overwrites': True,
        'ignoreerrors': True,
        'format': 'bestvideo+bestaudio',  # Select best audio quality
        'outtmpl': download3 + '/%(title)s.%(ext)s',  # Save file with the title of the video
        'postprocessors': [{  # Add post-processor to convert to mp3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    def __init__(self, url):
        self.url = url

    

    def get_thumbnail(info):
        url = info.get('thumbnail')
        image = Image.open(io.BytesIO(requests.get(url).content))
        #new_size = (600,600)
        #image = image.resize(new_size, Image.LANCZOS) 
        output_buffer = io.BytesIO()
        image.save(output_buffer, format="JPEG") 
        return output_buffer.getvalue() 

    def resize_image(image_data, new_size=(600, 600)):
        # Преобразуем байты изображения в объект Image
        image = Image.open(io.BytesIO(image_data))

        # Изменяем размер изображения
        resized_image = image.resize(new_size, Image.LANCZOS)

        # Конвертируем измененное изображение обратно в байты
        output_buffer = io.BytesIO()
        resized_image.save(output_buffer, format="JPEG")  # Сохраняем в формате JPEG
        return output_buffer.getvalue()

    def with_stupid_borders(image):
        pixels = image.load()
        width, height = image.size

        # Проверка цвета первой колонки слева
        left_border_color = pixels[0, 0]
        is_left_border = all(pixels[0, y] == left_border_color for y in range(height))

        if not is_left_border:
            print("Левой заливки нет — обрезка не требуется.")
            return image

        print(f"Левая заливка найдена (цвет: {left_border_color}), обрезаю...")

        # Обрезаем по центру квадрат размером height x height
        left = (width - height) // 2
        top = 0
        right = left + height
        bottom = height

        cropped_img = image.crop((left, top, right, bottom))
        return cropped_img


    def get_squre_image(image_data, border_color=(255, 255, 255)):
        # Преобразуем байты изображения в объект Image
        image = Image.open(io.BytesIO(image_data))

        # Проверяем, нужно ли обрезать тупые границы
        image = with_stupid_borders(image)

        # Обрезаем изображение до квадрата относительно центра
        width, height = image.size

        # Определяем размер стороны нового квадрата
        new_size = max(width, height)

        # Вычисляем отступы (чтобы картинка оказалась по центру)
        left = (new_size - width) // 2
        top = (new_size - height) // 2
        right = new_size - width - left
        bottom = new_size - height - top

        cropped_image = ImageOps.expand(image, border=(left, top, right, bottom), fill=border_color)

        # Конвертируем обрезанное изображение обратно в байты
        output_buffer = io.BytesIO()
        cropped_image.save(output_buffer, format='JPEG')  # Используем исходный формат
        return output_buffer.getvalue()

    def download_url(url, mode='mp3'):
        failed_downloads = []
        try:
            with YoutubeDL (ydl_opts) as dwld:
                if "playlist" in url:
                    playlist = dwld.extract_info(url, download=False)['entries']
                    list = ["https://music.youtube.com/watch?v=" + track["id"] for track in playlist]
                else:
                    list = [url]
                for url in list:
                    info = dwld.extract_info(url, download=False)

                    path = download3 + '/' + info['title'] + f'.{mode}'
                    if not os.path.exists(path):
                        dwld.download(url)

                    if not os.path.exists(path):
                        failed_downloads.append((url, info['title']))
                        continue
                        
                    thumb_data = None

                    if info.get("thumbnail"):
                        thumb_data = get_thumbnail(info)
                        thumb_data = get_squre_image(thumb_data)

                    audio = MP3(path, ID3=ID3)
                    if not audio.tags:
                        audio.add_tags()
                    list = ['adam', 'eva', 'kain']
                    audio.tags.add(TIT2(encoding=3, text=info['title']))                      # Название
                    audio.tags.add(TPE1(encoding=3, text=' & '.join(info.get('artists', [info.get('uploader', '')])) ))                   # Автор канала
                    audio.tags.add(TALB(encoding=3, text=info.get('album', '')))  # Альбом / плейлист
                    audio.tags.add(TCON(encoding=3, text=info.get('categories', [''])[0]))        # Жанр
                    audio.tags.add(TYER(encoding=3, text=info['upload_date'][:4]))            # Год публикации
                    audio.tags.add(COMM(encoding=3, lang='eng', desc='Comment', text=f"Source: {url}"))  # Комментарий
                    audio.tags.add(TXXX(encoding=3, desc='YouTube URL', text=url))    # Свое поле
                    audio.tags.add(WOAS(encoding=3, url=url))                         # Официальная ссылка

                    if thumb_data:
                        audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='High quality cover', data=thumb_data))
                        audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=0, desc='Medium quality Cover', data=resize_image(thumb_data, (320, 320))))
                        audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=1, desc='Icon quality cover', data=resize_image(thumb_data, (64, 64))))
                    audio.save()
        except Exception as e:
            traceback.print_exc()
        print("Download completed.")
        for url, title in failed_downloads:
            print(f"Failed to download {title} from {url}. Please check the URL or try again later.")
        