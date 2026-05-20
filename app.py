import argparse
import os
from flask import Flask, render_template

app = Flask(__name__)

WORD_DEFINITIONS = {
    "abandon": "to leave something behind or stop supporting completely",
    "ability": "the skill or power to do something",
    "adventure": "an exciting or unusual experience",
    "balance": "a steady position without falling",
    "capture": "to catch or take control of something",
    "change": "to make something different",
    "clarity": "the quality of being clear and easy to understand",
    "comfort": "a state of physical ease and relaxation",
    "culture": "the ideas and customs of a group of people",
    "decide": "to choose one option after thinking about it",
    "delight": "a feeling of great pleasure or happiness",
    "discover": "to find or learn something for the first time",
    "effort": "physical or mental energy used to do something",
    "enable": "to make something possible or easier",
    "energy": "the ability to do work or cause change",
    "engine": "a machine that converts energy into motion",
    "example": "something that shows what is typical or possible",
    "experience": "knowledge gained from doing things",
    "global": "relating to the whole world",
    "growth": "the process of increasing in size or ability",
    "happy": "feeling or showing joy and pleasure",
    "honest": "telling the truth and acting sincerely",
    "imagine": "to form a picture or idea in your mind",
    "journey": "a trip from one place to another",
    "justice": "fair treatment according to the law",
    "knowledge": "facts and information learned through study",
    "language": "a system of words used to communicate",
    "learn": "to gain knowledge or skill from experience",
    "legacy": "something handed down from the past",
    "limit": "the greatest amount or degree allowed",
    "local": "related to a nearby place",
    "memory": "the ability to remember information",
    "mentor": "a trusted guide or adviser",
    "method": "a way of doing something",
    "moment": "a very short period of time",
    "nature": "the physical world, including plants and animals",
    "notice": "to become aware of something",
    "object": "a thing that can be seen or touched",
    "opinion": "a personal belief or judgment",
    "peace": "a state without war or trouble",
    "people": "human beings in general",
    "planet": "a large body that moves around a star",
    "positive": "thinking in a hopeful and confident way",
    "practice": "to do something repeatedly to improve",
    "question": "a sentence used to ask for information",
    "reason": "a cause or explanation for something",
    "refresh": "to make something feel new or energetic",
    "respect": "a feeling of admiration for someone",
    "result": "what happens because of an action",
    "review": "to look at something again carefully",
    "reward": "something given for good work or behavior",
    "science": "the study of the natural world",
    "service": "help or work done for others",
    "simple": "easy to understand or do",
    "skill": "a learned ability to do something well",
    "smile": "a happy expression made with the mouth",
    "strength": "the power to do something physical or mental",
    "success": "the achievement of a goal",
    "talent": "a natural ability to do something well",
    "thanks": "a polite expression of gratitude",
    "think": "to use your mind to form ideas",
    "travel": "to go from one place to another",
    "unique": "being the only one of its kind",
    "value": "the importance or worth of something",
    "vision": "a clear idea of what something should be",
    "voice": "the sound made when speaking or singing",
    "wonder": "a feeling of surprise and admiration",
    "world": "the planet and all the people on it",
    "worthy": "deserving respect or attention",
    "yellow": "the color between green and orange",
    "youth": "the time of being young",
    "zeal": "great energy or enthusiasm for a goal",
    "zone": "an area with a particular characteristic"
}

WORD_LIST = list(WORD_DEFINITIONS.keys())
DAILY_WORD_COUNT = 5

@app.route('/')
def index():
    return render_template(
        'index.html',
        word_list=WORD_LIST,
        word_definitions=WORD_DEFINITIONS,
        daily_word_count=DAILY_WORD_COUNT,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the English word reminder app.')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', 5000)), help='Port to bind the server to')
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port)
