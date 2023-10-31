from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
from datetime import datetime


app = Flask(__name__)

client = MongoClient('mongodb+srv://nadaanis526:nada2626anis@cluster0.zp4go5w.mongodb.net/')
db = client.dbprojects


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/detail/<keyword>')
def detail(keyword):
    api_key = 'd9a2b6df-742f-4f05-bde8-e57b408cc750'
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()
    return render_template(
        'detail.html',
        word=keyword,
        definitions=definitions,
        status=request.args.get('status_give', 'new')
    )


@app.route('/api/save_word', methods=['POST'])
def save_word():
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')
    doc = {
        'word': word,
        'definitions': definitions,
        'date': datetime.now().strftime('%Y''-''%m''-''%d')
    }
    db.words.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': f'the word, {word}, was saved!!!',
    })


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    return jsonify({
        'result': 'success',
        'msg': f'the word {word} was deleted'
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)