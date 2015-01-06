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

    def __init__(self, hanji, pinyin, audio):
        self.hanji = hanji
        self.pinyin = pinyin
        self.audio = audio
