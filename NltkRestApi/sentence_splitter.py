import logging
import os
import sys

import nltk
from nltk.tokenize import sent_tokenize

from sanic.response import text
from sanic import Sanic
from sanic.response import json

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

app = Sanic("NLTK RestApi")

@app.route("/sentsplit", methods=["POST",])
async def split_sentence(request):
    input_text = str(request.body, "utf-8", 'ignore')
    trunc_text = (input_text[0:25] + " ... " + input_text[-20:]) if len(input_text)>50 else input_text
    logging.info("input_text={}".format(trunc_text))
    sentences = sent_tokenize(input_text)
    logging.info("len(input_text)={}".format(len(input_text)))
    logging.info("len(sentences) ={}".format(len(sentences)))
    return json(sentences)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
