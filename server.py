import re
import ssl
import json
import spacy
import requests
import http.server
import socketserver
import numpy as np

from flask import Flask
from flask import request, jsonify

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

import urllib.request
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

def identify_entities(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(strip=True)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\[[0-9]*\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    global nlp
    doc = nlp(text)
    return [
        { 'text': ent.text, 'label': ent.label_ }
        for ent in doc.ents
    ]

class MyServer(http.server.SimpleHTTPRequestHandler):
    def send(self, response):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        url = data['url']

        print('serving', url)
        entities = identify_entities(url)
        self.send(entities)

server = MyServer
server_addr = ('localhost', 8888)

with socketserver.TCPServer(server_addr, server) as httpd:
    print("serving at port", server_addr)
    httpd.serve_forever()
