import io
import json
import os
from collections import defaultdict


class datasource(object):

    DATA_DIR = 'data'
    CHENGYU_JSON = 'chengyu.json'
    EMOJI_CN_JSON = 'emoji.cn.json'
    TONE_JSON = 'tone.json'
    CN_COMMA = '，'

    def __init__(self):
        this = os.path.dirname(os.path.abspath(__file__))
        self.base = os.path.join(this, self.DATA_DIR)
        self.load_chengyu()
        self.load_emoji()
        self.load_tone()
        self.reverse_emoji()

    def load_chengyu(self):
        self.chengyu_list = []

        file = os.path.join(self.base, self.CHENGYU_JSON)
        with io.open(file, 'r') as f:
            for line in f:
                chengyu = json.loads(line)
                self.chengyu_list.append(chengyu)

    def load_emoji(self):
        self.emoji_map = {}

        file = os.path.join(self.base, self.EMOJI_CN_JSON)
        with io.open(file, 'r') as f:
            for line in f:
                emoji_item = json.loads(line)
                if not emoji_item['words']:
                    continue

                self.emoji_map[emoji_item['emoji']] = emoji_item

    def load_tone(self):
        self.tone_map = {}

        file = os.path.join(self.base, self.TONE_JSON)
        with io.open(file, 'r') as f:
            self.tone_map = json.load(f)

    def split_chengyu_pinyin(self, origin):
        rs = []
        last = ''
        for c in origin:
            if c == ' ':
                rs.append(last)
                last = ''
            elif c == self.CN_COMMA:
                rs.append(last)
                rs.append(c)
                last = ''
            else:
                last += c
        if last:
            rs.append(last)
        elif origin[-1] == ' ':
            rs.append('')
        return rs

    def clean_tone(self, origin):
        rs = None
        for i, c in enumerate(origin):
            if c in self.tone_map:
                if rs is None:
                    rs = list(origin)
                rs[i] = self.tone_map[c]
        if rs is None:
            return origin
        return ''.join(rs)

    def reverse_emoji(self):
        self.cn_emoji_map = defaultdict(list)
        self.pinyin_emoji_map = defaultdict(list)

        for emoji, emoji_item in self.emoji_map.items():
            for word_item in emoji_item['words']:
                self.cn_emoji_map[word_item['word']].append(emoji_item)
                self.pinyin_emoji_map[word_item['pinyin']].append(emoji_item)
                pinyin = self.clean_tone(word_item['pinyin'])
                if pinyin != word_item['pinyin']:
                    self.pinyin_emoji_map[pinyin].append(emoji_item)


DataSource = datasource()
