from django.db import models
from xpinyin import Pinyin

def pinyin(s):
    p = Pinyin()
    s2 = p.get_pinyin(unicode(s), ' ', show_tone_marks=True)
    return s2

# Create your models here.
class Word:
    hanji = None
    pinyin = None
    audio = None
    ja = None

    def __init__(self, hanji, pinyin, audio, ja):
        self.hanji = hanji
        self.pinyin = pinyin
        self.audio = audio
        self.ja = ja
