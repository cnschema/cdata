#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from cdata.summary import *  # noqa

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class SummaryTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_misc(self):
        person = {
            "name": u"张三",
            "accomplishment": u"三好学生"
        }
        ret = summarize_entity_person(person)
        assert u"张三，主要成就：三好学生。" == ret

        person = {
            "name": u"张三",
            "accomplishment": u"三好学生",
            "artName": [u"张老三"]
        }
        ret = summarize_entity_person(person)
        assert u"张三，号张老三，主要成就：三好学生。" == ret

        person = {
            "name": u"张三",
            "accomplishment": u"三好学生",
            "artName": []
        }
        ret = summarize_entity_person(person)
        assert u"张三，主要成就：三好学生。" == ret

    def test_real_data(self):
        person = {
        "description": u"黄健中，1941年12月29日出生于印度尼西亚泗水，国家一级导演、编剧、艺术指导。1979年，黄健中与张铮联合执导爱情片《小花》，该片获得第三届电影百花奖上获最佳故事片奖 。1982年，黄健中独立执导首部电影作品——爱情片《如意》。1985年，凭借家庭剧《良家妇女》获得第二十五届卡罗维·发利国际电影节主要奖[2-3] 。1990年，拍摄警匪剧《龙年警官》，该片获得第十四届大众电影百花奖最佳故事片奖。1991年，拍摄家庭剧《过年》，该片获得第十五届大众电影百花奖最佳故事片奖。1995年，执导剧情片《大鸿米店》[4-6] 。1998年，拍摄爱情片《红娘》，该片获得第二十二届大众电影百花奖最佳故事片奖[7-8] 。2001年，执导古装武侠剧《笑傲江湖》 。2003年，与佐藤纯弥联合执导家庭犯罪剧《世纪末的晚钟》[10-12] 。2005年，国家广播电影电视总局授予黄健中“优秀电影艺术家”称号 。2006年，执导古装历史剧《越王勾践》 。2009年，拍摄历史战争剧《大秦帝国之裂变》，该片获得第25届中国电视金鹰奖[14-17] 。2011年，执导古装剧《大风歌》[18-19] 。2013年，执导古装神话剧《蓬莱八仙》[20-22] 。",
        "birthPlace": u"印度尼西亚泗水",
        "name": u"黄健中",
        "image": u"http://c.hiphotos.baidu.com/baike/w%3D268%3Bg%3D0/sign=9ac8a3ed33adcbef01347900949449e0/aec379310a55b319a1ae185c41a98226cffc1747.jpg",
        "accomplishment": u"第4届东京国际电影节评委奖第11届中国电影金鸡奖最佳导演奖第12届中国电影金鸡奖最佳编剧奖",
        "birthDate": u"1941年12月29日",
        "keywords": [u"导演", u"娱乐人物", u"人物"],
        "nationality": u"中国",
        "alternateName": ["HuangJianzhong", "Huang Jianzhong"],
        "authorOf": u"过年、龙年警官、越王勾践、大风歌",
        "@id": u"d67f8dc6-3775-3e4a-9d67-84bb4007d6d1",
        "@type": ["Person", "Thing"],
        "occupation": u"导演、编剧、艺术指导，" # Extra comma for punctuation testing
        }
        ret = summarize_entity_person(person)
        logging.info(ret)
        assert u"黄健中，1941年12月29日出生于印度尼西亚泗水，中国导演、编剧、艺术指导，主要作品：过年、龙年警官、越王勾践、大风歌。" == ret

        person = {
        "name": u"陈小群",
        "gender": u"女",
        "image": u"http://e.hiphotos.baidu.com/baike/w%3D268%3Bg%3D0/sign=3c89cd72acc379317d68812fd3ffd078/b90e7bec54e736d16b57837c98504fc2d5626979.jpg",
        "description": u"女，抒情女高音歌唱家，现任上海音乐学院声乐系教授、硕士生导师；先后担任文化部举办的国际声乐比赛全国选拔赛、中国音乐家协会举办的“金钟奖”全国声乐比赛、全国大学生艺术歌曲比赛等比赛评委。",
        "@type": ["Person", "Thing"],
        "ethnicGroup": u"汉族",
        "keywords": [u"音乐", u"行业人物", u"歌手", u"教育", u"娱乐人物", u"人物", u"书籍"],
        "nationality": u"中国",
        "@id": u"66548f8a-3f9e-37ca-afb1-e2e96fdb083b",
        "alumniOf": u"上海音乐学院",
        "occupation": u"教授"
        }
        ret = summarize_entity_person(person)
        assert u"陈小群，中国教授。" == ret

        # Test for bracket, unknown birth date, courtesy name
        person = {
        "@id": u"2d8d5ed9-108b-3621-86bd-6c67fbbf0896",
        "@type": u"Person,Thing",
        "accomplishment": u"袭龙城，收复河朔、河套地区，击败单于",
        "birthDate": u"不详",
        "birthPlace": u"河东平阳（今山西临汾市）",
        "courtesyName": u"仲卿",
        "deathDate": u"公元前106年（汉武帝元封五年）",
        "description": u"卫青，字仲卿，河东平阳人",
        "dynasty": u"西汉",
        "ethnicGroup": u"汉族",
        "image": "http://c.hiphotos.baidu.com/baike/w%3D268%3Bg%3D0/sign=dce9ce450f3387449cc5287a6934bec4/d53f8794a4c27d1ef8d6abd118d5ad6eddc43836.jpg",
        "name": u"卫青",
        "posthumousName": u"烈"
        }

        summary = u"卫青，字仲卿，西汉人，出生于河东平阳，主要成就：袭龙城，收复河朔、河套地区，击败单于。"
        assert summary == summarize_entity_person(person)

if __name__ == '__main__':
    unittest.main()
