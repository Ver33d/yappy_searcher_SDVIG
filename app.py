from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from pymilvus import connections, Collection
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
IMG_FOLDER = os.path.join("static", "photo")


def get_links_and_descriptions():
    # Устанавливаем соединение с Milvus
    connections.connect(alias="default", host="127.0.0.1", port="19530")

    # Получаем объект коллекции
    collection = Collection("proverka")

    if collection.is_empty:
        print("Коллекция пуста")
        return []

    # Загрузка всех данных из коллекции
    links_and_descriptions = collection.query("", output_fields=["link", "description"], limit=100)

    # Создаем список словарей для Flask приложения
    videos = [{"url": item["link"], "tags": [item["description"]]} for item in links_and_descriptions]

    return videos


@app.route('/', methods=['GET', 'POST'])
def index():
    videos = get_links_and_descriptions()  # Получаем видео из Milvus
    print(videos)
    search_query = request.form.get('search', '')
    if search_query:
        filtered_videos = [
            video for video in videos if any(search_query in tag for tag in video['tags'])
        ]
    else:
        filtered_videos = videos
    return render_template('index.html', videos=filtered_videos, search_query=search_query)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video_file = request.files.get('video-file')
        video_url = request.form.get('video-url')
        video_title = request.form.get('video-title')
        video_tags = request.form.get('video-tags')

        if not video_title:
            return "Название ролика обязательно", 400

        if video_file:
            video_file.save(f"uploads/{video_file.filename}")

        return f"Данные загружены. Название: {video_title}, URL: {video_url}"

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
