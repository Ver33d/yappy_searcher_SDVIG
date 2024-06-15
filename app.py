import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from pymilvus import connections, Collection
from tqdm import tqdm
from PIL import Image
from nn_functions import *
import os
import pandas as pd
import numpy as np
import torch
from transformers import AutoModel
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"
model_clip = AutoModel.from_pretrained('jinaai/jina-clip-v1', trust_remote_code=True).to(device)

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
        return [], 0

    # Загрузка всех данных из коллекции
    links_and_descriptions = collection.query("", output_fields=["link", "description"], limit=10000)

    # Создаем список словарей для Flask приложения
    videos = [{"url": item["link"], "tags": [item["description"]]} for item in links_and_descriptions]

    # Возвращаем видео и количество ссылок
    return videos, len(videos)


def insert_video_to_milvus(link, tags, embd):
    # Подключение к Milvus уже должно быть настроено
    collection = Collection("proverka")

    # Проверяем, что tags не None и является списком, иначе присваиваем пустую строку
    tags_string = ', '.join(tags) if tags and isinstance(tags, list) else ''

    # Подготовка данных для вставки
    to_insert = [{"embd": embd, "link": link, "description": tags_string}]

    # Вставка данных в коллекцию
    mr = collection.insert(to_insert)
    print("Insert result:", mr)


@app.route('/', methods=['GET', 'POST'])
def index():
    videos, total_links = get_links_and_descriptions()  # Получаем видео и их количество из Milvus
    print(total_links)
    search_query = request.form.get('search', '')
    filtered_videos = []
    if search_query:
        filtered_videos = [
            video for video in videos if any(search_query in tag for tag in video['tags'])
        ]
    return render_template('index.html', videos=filtered_videos, search_query=search_query, total_links=total_links)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video_url = request.form.get('video-url')
        video_links_file = request.files.get('video-links-file')
        # video_title = request.form.get('video-title')
        video_tags = request.form.get('video-tags')

        if video_links_file:
            # Преобразование загруженного файла в JSON
            links_data = json.load(video_links_file)
            # Обработка каждой записи в JSON файле
            for item in links_data:
                link = item.get('link')
                tags = item.get('tags', None)  # Установка None если теги отсутствуют
                # Извлечение характеристик видео
                embedding = extract_video_features(link, model_clip)
                ocr_text = extract_text_from_video(link)
                print("ocr_text", ocr_text)
                # Вставка данных в Milvus
                insert_video_to_milvus(link, tags, embedding)

        if video_url:
            embedding = extract_video_features(video_url, model_clip)
            # Добавляем запись в Milvus
            insert_video_to_milvus(video_url, video_tags, embedding)

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
