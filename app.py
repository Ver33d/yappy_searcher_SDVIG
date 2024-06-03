from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
IMG_FOLDER = os.path.join("static", "photo")


videos = [
       {
           "url": "https://cdn-st.rutubelist.ru/media/0f/48/8a1ff7324073947a31e80f71d001/fhd.mp4",
           "tags": ["постановка", "юмор", "комедия"]
       },
       {
           "url": "https://cdn-st.rutubelist.ru/media/bf/ee/85fb6b80491db79e8baebe5c9d80/fhd.mp4",
           "tags": ["образ", "селебрити", "кроссовки"]
       },
       {
           "url": "https://cdn-st.rutubelist.ru/media/8c/58/96608b7a4834883ea2dd1c884c63/fhd.mp4",
           "tags": ["Бейрут", "Ливан"]
       },
       {
           "url": "https://cdn-st.rutubelist.ru/media/2f/4f/6b969c8c4a2aafcfca057b2a99a2/fhd.mp4",
           "tags": ["спорт", "футбол", "роналду"]
       },

   ]


@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search', '')
    if search_query:
        filtered_videos = [
            video for video in videos if any(search_query in tag for tag in video['tags'])
        ]
    else:
        filtered_videos = videos
    return render_template('index.html', videos=filtered_videos, search_query=search_query)



if __name__ == "__main__":
    app.run(debug=True)