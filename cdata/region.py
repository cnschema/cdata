#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding

import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import argparse
import urlparse
import re
import collections

from core import *
from table import *
from misc import main_subtask
import jieba

LIST_NATIONAL = [
    u'壮族',
    u'满族',
    u'回族',
    u'苗族',
    u'维吾尔族',
    u'土家族',
    u'彝族',
    u'蒙古族',
    u'藏族',
    u'布依族',
    u'侗族',
    u'瑶族',
    u'朝鲜族',
    u'白族',
    u'哈尼族',
    u'哈萨克族',
    u'黎族',
    u'傣族',
    u'畲族',
    u'傈僳族',
    u'仡佬族',
    u'东乡族',
    u'高山族',
    u'拉祜族',
    u'水族',
    u'佤族',
    u'纳西族',
    u'羌族',
    u'土族',
    u'仫佬族',
    u'锡伯族',
    u'柯尔克孜族',
    u'达斡尔族',
    u'景颇族',
    u'毛南族',
    u'撒拉族',
    u'布朗族',
    u'塔吉克族',
    u'阿昌族',
    u'普米族',
    u'鄂温克族',
    u'怒族',
    u'京族',
    u'基诺族',
    u'德昂族',
    u'保安族',
    u'俄罗斯族',
    u'裕固族',
    u'乌孜别克族',
    u'门巴族',
    u'鄂伦春族',
    u'独龙族',
    u'塔塔尔族',
    u'赫哲族',
    u'珞巴族',
    u'各族'
]

PATTERN_NATIONAL = u'({})'.format(u'|'.join(LIST_NATIONAL))
PATTERN_NATIONAL2 = u'({})'.format(u'?|'.join(
    [x for x in LIST_NATIONAL if len(x) > 2]))

SPECIAL_ADDRESS_NAME = [
    # 县
    u"葵潭",
    u"靖海",
    u"隆江",
    u"城月",  # ["城月镇建新路49号", "城月药店第二门市部"]
    u"黄略",  # ["黄略镇南亭圩三角路", "黄略药店5南亭门市部"]
    u"杨柑",  # ["杨柑镇豆坡大石牛", "杨柑药店大石牛门市部"]
    u"黄岭",  # ["杨柑镇豆坡大石牛", "杨柑药店大石牛门市部"]
    u"神泉",  # ["神泉镇新观路八号", "神泉汉龙药店"]

    # 区
    u"新林",  # ["新林区翠岗镇", "新林区旭东药店"]
    u"加格达奇",  # ["加格达奇区曙光康庄小区18#楼车库1-15号", "加格达奇一正中西药店"]
    #
    u"拱北",  # ["拱北夏湾中珠新村二期6号商铺", "守仁药店"]
    u"守仁",
    u"平沙",  # ["平沙所平沙前进分场", "平沙前进药店"]
    u"三灶",  # ["三灶所珠海机场海澄市场", "海澄健恒药店"]
    u"海澄",  # ["三灶所珠海机场海澄市场", "海澄健恒药店"]
    u"大亚湾",  # ["大亚湾霞涌市场", "大亚湾霞涌方方药店"]
    u"乌塘",  # ["乌塘圩", "城月药店乌塘第一门市部"]


    # bad case
    u"大参林",  # ["", "大参林医药集团股份有限公司第六百零九分店"]
    u"龙归",  # ["", "龙归利农药店"]
    u"光明托老",  # ["光明托老中心综合楼商服0113号", "加格达奇区寅河大药房"]
    u"云管端互联网",  # ["", "云管端互联网软件有限公司"]
    u"康美健康云服务有限公司",  # ["", "康美健康云服务有限公司"]
]


def is_special_address(xinput):
    if type(xinput) == list:
        for addr in xinput:
            if not is_special_address(addr):
                return False
        return True
    else:
        if not xinput:
            return True

        regex = ur"[服装店药店药房医院集团有限公司股份有限责任科技第一门市分店总店]+$"
        temp = re.sub(regex, "", xinput)
        if len(temp) <= 3 and not re.search(ur"[圩省市县镇]", temp):
            logging.warn(u"skip {} => {}".format(xinput, temp))
            return True

        m = re.search(ur"^(.{2,6}[镇区])", xinput)
        if m:
            logging.debug(m.group(1))
            return True

        for name in SPECIAL_ADDRESS_NAME:
            if xinput.startswith(name):
                return True

        return False


def normalize_national(name):
    temp = name
    temp = re.sub(u'东乡族自治县', u'东乡县', temp)
    temp = re.sub(PATTERN_NATIONAL2, '', temp)
    temp = re.sub(PATTERN_NATIONAL, '', temp)

    if len(temp) == 1:
        return name
    else:
        return temp


def normalize_misspell(name):
    name = name.replace(u"恵", u"惠")
    return name


def normalize_province(name):
    name_norm = name

    name_norm = normalize_national(name_norm)
    name_norm = re.sub(ur'(自治区|特别行政区)', '', name_norm)

    if name_norm == u'内':
        name_norm = u'内蒙古'

    if name_norm == u'内蒙':
        name_norm = u'内蒙古'

    name_compact = name_norm
    if len(name_compact) > 2:
        name_compact = re.sub(ur'(省|市)$', '', name_compact)

    return [name_norm, name_compact]


def normalize_city(name):
    name_norm = name

    name_norm = normalize_national(name_norm)
    name_norm = re.sub(ur'^(市辖区|自治区直辖县级行政区划|省直辖县级行政区划|自治旗|自治州|矿区|县|区)$', '', name_norm)  # noqa
    name_norm = re.sub(ur'自治', '', name_norm)

    name_compact = name_norm
    if len(name_compact) > 2:
        name_compact = re.sub(ur'(州|地区|市)$', '', name_compact)

    ret = [name_norm, name_compact]
    if name == u"哈尔滨市":
        ret.append(u"哈尔傧")

    if re.search(ur"市$", name):
        ret.append(re.sub(ur"市$", ur"市区", name))

    return ret


def normalize_district(name):
    name_norm = name

    name_norm = normalize_national(name_norm)

    # logging.info(len(name_norm))

    name_norm = re.sub(ur'(市辖区)', '', name_norm)

    if len(name_norm) > 3:
        name_norm = re.sub(ur'(自治|郊区|城区)', '', name_norm)

    name_compact = name_norm
    if len(name_compact) > 3:
        name_compact = re.sub(ur'(新区|林区|矿区)$', '', name_compact)
    if len(name_compact) > 2:
        name_compact = re.sub(ur'(区|县|市)$', '', name_compact)
    # if name.startswith(u"富拉尔基"):
    #    logging.info( name_compact )

    ret = [name_norm, name_compact]
    # if name == u"增城区":
    #    ret.append(u"增城市")

    if name_norm == name and re.search(ur"区$", name):
        ret.append(name_norm.replace(u"区", u"县"))
        ret.append(name_norm.replace(u"区", u"市"))
    ret.append(re.sub(ur"区$", u"县", name))
    ret.append(re.sub(ur"县$", u"区", name))

    ret.append(normalize_misspell(name_norm))

    return ret


def normalize_address(address, province, city, district):
    assert address is not None

    if not type(address) == unicode:
        address = address.decode("utf-8")

    region_list = []
    if province:
        if not type(province) == unicode:
            province = province.decode("utf-8").strip()
        region_list.append(province)
        region_list.extend(normalize_province(province))

    if city:
        if not type(city) == unicode:
            city = city.decode("utf-8")
        region_list.append(city)
        region_list.extend(normalize_city(city))

    if district:
        if not type(district) == unicode:
            district = district.decode("utf-8")
        region_list.append(district)
        region_list.extend(normalize_district(district))

    ret = {
        "address": address,
        "addressNorm": address,
        "province": province,
        "city": city,
        "district": district,
    }

    region_list = sorted(list(set(region_list)), reverse=True)
    region_list.append(u"区")
    # logging.info(json.dumps(region_list, ensure_ascii=False))
    # logging.info(json.dumps(ret,ensure_ascii=False))

    if region_list:
        regex = u"^({})+".format(u"|".join(region_list))
        # logging.info(regex)
        ret["addressNorm"] = re.sub(regex, "", ret["addressNorm"]).strip()

    return ret


class RegionEntity():
    def _get_list_province_unique(self, list_cityid):
        cancityidates = set()
        for cityid in list_cityid:
            cancityidates.add(self.data['items'][cityid]['province'])
        if len(cancityidates) == 1:
            [pnorm, pcompact] = normalize_province(list(cancityidates)[0])
            # print pcompact
            return pcompact

    def __init__(self, strict_mode=True):
        data = file2json(file2abspath('region_data.json', __file__))
        counter = collections.Counter()
        self.strict_mode = strict_mode

        self.data = {
            'items': {},  # 原始数据，基于cityid（多种指代，可以市省，市，区县级别）

            # 基于别名的索引， NER使用
            'province': {},  # 无重名
            'city': {},  # 有重名
            'district': {},  # 有重名


            'alias': {},  # 别名索引

            'lookup': collections.defaultdict(set),
        }

        # copy data
        for item in data:
            self.data['items'][item['cityid']] = item

        # process province
        map_province = collections.defaultdict(set)
        for item in data:
            p = item.get('province')
            c = item.get('city')
            d = item.get('district')
            if p and not c:
                # cityid 为省的ID
                item["type"] = "province"
                item["name"] = p
                map_province[p].add(item['cityid'])
        assert 34 == len(map_province), len(map_province)
        # logging.info(json.dumps(list(map_province.keys()), ensure_ascii=False))

        for p in sorted(list(map_province)):
            alias_list = normalize_province(p)
            pnorm = alias_list[1]
            self.data['province'][p] = {
                'province': self._get_list_province_unique(map_province[p]),
                'cityid_list': list(map_province[p]),
                'alias': [p] + alias_list}
            map_province[p] = pnorm
            if pnorm.startswith(u'安徽'):
                logging.info(json.dumps(alias_list))
            # print json.dumps(list(set([p,pnorm,pnorm2])),ensure_ascii=False)

        # process city
        map_city = collections.defaultdict(set)
        for item in data:
            c = item.get('city')
            d = item.get('district')
            if c in [u"市辖区", u"县", u"省直辖县级行政区划", u"自治区直辖县级行政区划"]:
                continue
            """
                {
                    "city": "市辖区",
                    "cityid": "310105",
                    "district": "长宁区",
                    "province": "上海市"
                }

                {
                    "city": "南通市",
                    "cityid": "320601",
                    "district": "市辖区",
                    "province": "江苏省"
                },
            """

            if c and not d:
                item["type"] = "city"
                item["name"] = c
                map_city[c].add(item['cityid'])
                if len(map_city[c]) != 1:
                    logging.error(json.dumps(item, ensure_ascii=False))
                    logging.error(len(map_city[c]))
                    assert len(map_city[c]) == 1

        assert 333 == len(map_city), len(map_city)
        # logging.info(json.dumps(list(map_city.keys()), ensure_ascii=False))

        for p in sorted(list(map_city)):
            alias_list = normalize_city(p)
            assert pnorm
            # print p, '-->',pnorm, '-->', pcompact
            self.data['city'][p] = {
                'province': self._get_list_province_unique(map_city[p]),
                'cityid_list': list(map_city[p]),
                'alias': [p] + alias_list}
        assert len(map_city) == len(self.data['city']), len(self.data['city'])

        # process district
        map_district = collections.defaultdict(set)
        for item in data:
            d = item.get('district')
            if d in [u"市辖区"]:
                # check above 市辖区 is used both as value of city and district
                # simply drop them since they already defined in city level
                continue

            if d:
                item["type"] = "district"
                item["name"] = d
                map_district[d].add(item['cityid'])
        assert 2820 == len(map_district), len(map_district)

        for p in sorted(list(map_district)):
            alias_list = normalize_district(p)
            # print p, '-->',pnorm, '-->', pcompact
            cityid_list = list(map_district[p])
            if len(cityid_list) > 1:
                # logging.info( len(cityid_list) )
                # logging.info( p )
                pass

            self.data['district'][p] = {
                'province': self._get_list_province_unique(map_district[p]),
                'cityid_list': cityid_list,
                'alias': [p] + alias_list}

        # process duplicated name 别名索引
        for index in ['province', 'city', 'district']:
            for name, data in self.data[index].items():
                for alias in set(data['alias']):
                    # if alias.startswith(u"清"):
                    #    logging.info(alias)
                    self.data['lookup'][alias].update(data['cityid_list'])

        for alias, alias_cityid_list in self.data['lookup'].items():
            alias_cityid_list_unique = set(alias_cityid_list)
            if len(alias_cityid_list_unique) > 1:
                # logging.debug(u"{} {}".format(alias, len(alias_cityid_list_unique)))
                # print alias
                for code in alias_cityid_list_unique:
                    # print json.dumps(self.data['items'][code], ensure_ascii=False)
                    pass

        # 有唯一省的地点名， 歧义地点名不管
        for alias, alias_cityid_list in self.data['lookup'].items():
            alias_cityid_list_unique = set(alias_cityid_list)
            province = self._get_list_province_unique(alias_cityid_list_unique)
            if province:
                self.data['alias'][alias] = province

        # with codecs.open(getTheFile('libcity_cn.new.json'),'w',encoding='utf-8') as f:
        #    json.dump(self.data, f,ensure_ascii=False, indent=4)
        # 统计
        for index in self.data:
            counter[index] = len(self.data[index])

        # validation
        for alias, entities in self.data['lookup'].items():
            if len(alias) == 1:
                logging.error(json.dumps(
                    entities, ensure_ascii=False, indent=4, sort_keys=True))
                if self.strict_mode:
                    exit()

            if alias in [u'自治']:
                logging.error(json.dumps(
                    entities, ensure_ascii=False, indent=4, sort_keys=True))
                if self.strict_mode:
                    exit()

            if len(entities) > 1:
                counter["one-alias-many-entities"] += 1
                # logging.info(u"{}[{}] {}".format(alias, len(entities), u",".join([x["name"]+x["type"] for x in entities])))

        # prepare for NER
        for index in ['province', 'city', 'district']:
            for name, data in self.data[index].items():
                for alias in set(data['alias']):
                    if re.search(ur"[省市县]$", alias):
                        jieba.add_word(alias, 10000000)
                    elif re.search(ur"[区]$", alias):
                        jieba.add_word(alias, 1000000)
                    else:
                        jieba.add_word(alias, 100000)

                        for suffix in u"路镇乡圩河区村":
                            jieba.add_word(u"{}{}".format(
                                alias, suffix), 1000000)

        names = file2iter(file2abspath('region_dict.txt', __file__))
        for name in names:
            jieba.add_word(name.strip(), 1)

        # jieba.del_word(u"广州药业")

    def normalize_region_name(self, name, xtype):
        if not hasattr(self, "normalizeRegion_mapped"):
            setattr(self, "normalizeRegion_mapped", collections.Counter())
        mapped = getattr(self, "normalizeRegion_mapped")

        name = re.sub(u"[省市]+$", "", name)

        if name in [u"市辖区"]:
            return name

        if name in ["", u"省市"]:
            return ""

        # rewrite
        if name in [u"内蒙", u"蒙古"]:
            name = u"内蒙古"

        cityid_list = self.data["lookup"].get(name)
        if not cityid_list:
            logging.error("cannot find reigion name")
            logging.error(name)
            logging.error(xtype)
            if self.strict_mode:
                exit(0)

        matched = []
        for cityid in cityid_list:
            item = self.data["items"][cityid]
            if item["type"] == xtype:
                matched.append(item)

        for item in matched:
            if item["name"] == name:
                return name

        for item in matched:
            if item["name"] != name:
                msg = u"normalized {} ->{}".format(name, item["name"])
                if msg not in mapped:
                    mapped[msg] += 1
                    logging.info(msg)
            return item["name"]

    def guess_province(self, addresses):
        for address in addresses:
            if not address:
                continue

            if address.startswith(u"内蒙"):
                return u"内蒙古"

            for index in ['province', 'city']:
                for name in self.data[index]:
                    for alias in set(self.data[index][name]['alias']):
                        if address.startswith(alias):
                            # print address, '-->', name, self.data[index][name]['province']
                            return self.data[index][name].get('province')

            for index in ['province', 'city']:
                for name in self.data[index]:
                    for alias in set(self.data[index][name]['alias']):
                        if re.search(ur'（{}）'.format(alias), address):
                            # print address, '-->', name, self.data[index][name]['province']
                            return self.data[index][name].get('province')

            for alias in self.data['alias']:
                if address.startswith(alias):
                    return self.data['alias'][alias]
                if re.search(ur'（{}）'.format(alias), address):
                    return self.data['alias'][alias]

        print 'guess_province failed', json.dumps(addresses, ensure_ascii=False)
        return u""

    def guess_all(self, addresses):

        # 解析实体 NER
        matched_alias = []
        candidates_name_weight = collections.Counter()
        matched_alias_cityid_list = {}

        visited_seg = []
        for address in addresses:
            if not type(address) == unicode:
                address = address.decode("utf-8")

            # skip shot name
            if len(address) < 3:
                continue

            # skip name without blacklist
            regex = ur"^[^省市县]{2,3}([庄村镇乡])"
            if re.search(regex, address):
                # logging.info(u"skip村镇乡 {}".format(address))
                continue

            regex = ur"^[^省市县]{2,5}([街路巷弄组]|大道|花园|市场)"
            if re.search(regex, address):
                # logging.info(u"skip村镇乡 {}".format(address))
                continue

            seg_list = list(jieba.cut(address, cut_all=False, HMM=False))
            logging.debug("Full Mode: " + "/ ".join(seg_list))

            # merge the first two seg if their combined into an alias
            if len(seg_list) > 1:
                # 清/ 新县/ 太和镇/ 滨江路/ 东/ 三/ 街/ 13/ 号/ 首层/ 5/ 号/ 铺
                # 恵/ 东县/ 大岭/ 镇/ 新园/ 路/ 145/ 号
                temp = u"{}{}".format(seg_list[0], seg_list[1])
                # logging.info(temp)
                temp = normalize_misspell(temp)
                if self.data["lookup"].get(temp):
                    logging.info(temp)
                    temp_list = [temp]
                    temp_list.extend(seg_list[2:])
                    seg_list = temp_list

                    logging.debug("After Merge: " + "/ ".join(seg_list))

                # 中山/ 市南区/ 寮/ 后/ 村/ 龙子/ 街/ 14/ 号
                if re.search(ur"^[省市县]", seg_list[1]):
                    temp = u"{}{}".format(seg_list[0], seg_list[1][0])
                    # logging.info(temp)
                    if self.data["lookup"].get(temp):
                        # logging.info(temp)
                        temp_list = [temp, seg_list[1][1:]]
                        temp_list.extend(seg_list[2:])
                        seg_list = temp_list

                        logging.debug("After Merge: " + "/ ".join(seg_list))

            is_continuous_match = True
            for idx, seg in enumerate(seg_list):
                logging.debug(seg)
                if seg in visited_seg:
                    continue
                else:
                    visited_seg.append(seg)

                cityid_list = self.data["lookup"].get(seg)
                logging.debug(cityid_list)

                # if idx > 0:
                # skip name without whitelist
                # regex = ur"(.{2,6}(自治)?[省市县]|^.{2,6}(自治)?[省市县区])"
                # if not re.search(regex, address):
                # logging.info(u"skip省市县区 {}".format(address))
                #    break

                if not cityid_list and len(seg) > 2 and idx == 0:
                    temp = re.sub(u"(市|县|经济特区).?$", "", seg)
                    cityid_list = self.data["lookup"].get(temp)
                    # logging.info(temp)

                if cityid_list:
                    # logging.info(seg)
                    matched_alias.append(seg)

                    matched_alias_cityid_list[seg] = cityid_list
                    weight_default = 1.0 / len(cityid_list)
                    for cityid in cityid_list:

                        name = self.data["items"][cityid]["name"]
                        candidates_name_weight[name] += weight_default

                        # dirty hack 2017-04-01
                        # add seg one more time if the address starts with it
                        # a very strong indicator
                        if is_continuous_match:
                            candidates_name_weight[name] += weight_default
                        if idx == 0:
                            logging.debug("idx0")
                            candidates_name_weight[name] += 2 * weight_default
                            if re.search(ur"[省市县]$", seg):
                                logging.debug("省市县")
                                candidates_name_weight[name] += 2 * \
                                    weight_default
                            elif re.search(ur"[区]$", seg):
                                logging.debug("区")
                                candidates_name_weight[name] += 1 * \
                                    weight_default

                        if seg == name:
                            pass
                        elif seg[-1] == name[-1]:  # kind of matched by alias
                            pass
                        elif seg in name:  # kind of matched by alias
                            logging.debug("seg is part of name")
                            candidates_name_weight[name] /= 2
                        else:
                            logging.debug("seg is different from name ")
                            candidates_name_weight[name] /= 4

                else:
                    is_continuous_match = False
                    if not re.search(ur"([县州]|公司)", address):
                        break

        # logging.info(json.dumps(matched_alias, ensure_ascii=False))

        # select the best entity (most specific, most fit)
        # 统计支持率
        best_entity = None
        best_match_score = 0
        # logging.info(json.dumps(candidates_name_weight, ensure_ascii=False))
        for seg in matched_alias:
            for city_id in matched_alias_cityid_list[seg]:
                entity = self.data["items"][city_id]
                # logging.info(json.dumps(entity.values(), ensure_ascii=False))
                match_score = sum([w for x, w in candidates_name_weight.items() if x in entity.values()])
                logging.debug(match_score)
                logging.debug(json.dumps(entity, ensure_ascii=False))
                if match_score > best_match_score:
                    best_entity = entity
                    best_match_score = match_score
                    logging.debug(json.dumps(best_entity, ensure_ascii=False))

        # print 'guess_province failed', json.dumps(addresses, ensure_ascii=False)
        # if best_entity:
        #     if len(addresses) == 2:
        #         msg = u"\t".join(any2unicode([ addresses[1],
        #                     addresses[0],
        #                     best_entity["province"],
        #                     best_entity.get("city", u""),
        #                     best_entity.get("district", u""),
        #                     best_entity["type"]
        #                 ]))
        #         print msg
        return best_entity


def task_guess_all(args=None):
    city_data = RegionEntity()
    # confused
    addresses = ["太平区红河七街区７１１栋６单元１楼１号", "哈尔滨人民同泰医药连锁店宏伟分店"]
    # missed
    addresses = ["龙江路之路村集资楼1号楼4号门市", "合作区德仁堂药店"]
    addresses = ["", "北京同仁堂广州药业连锁有限公司农林店"]
    addresses = ["北京海淀区阜成路52号（定慧寺）", "北京大学肿瘤医院"]
    addresses = ["水东镇东阳北街50号", "水东镇长安药店（已迁入三角所）"]
    addresses = ["保定市长城北大街头台村2109号门脸", "保定市莲池区中昊翔启蒙大药房"]

    result = city_data.guess_all(addresses)
    if result:
        logging.info(json.dumps(result, ensure_ascii=False))
        logging.info(render_result(result, addresses[1], addresses[0]))


def render_result(result, name=None, address=None):
    data = [name,
            address,
            result["province"],
            result.get("city", u""),
            result.get("district", u""),
            result["type"]]
    data = [x for x in data if x]
    msg = u"\t".join(any2unicode(data))
    return msg


def task_guess_all_batch(args):
    ner = RegionEntity()
    filename = "../tests/ex3-region-test.xls"
    filename = file2abspath(filename)
    excel_data = excel2json(filename, non_empty_col=-1)
    sheet_data = excel_data["data"].values()[0]
    sheet_fields = excel_data["fields"].values()[0]
    test_results = []

    for item in sheet_data:
        addresses = [item["address"], item["name"]]
        addresses = [x for x in addresses if x]
        result = ner.guess_all(addresses)
        msg = u"\n============\nexpect{}\nfound{}".format(
                json.dumps(item, ensure_ascii=False),
                json.dumps(result, ensure_ascii=False))
        logging.info(msg)

        one_result = {}
        test_results.append(one_result)

        # new entry
        if item["type"] == "" and result:
            logging.warn(render_result(result))

        match_errors = []
        if not result:
            result_type = "none"
        else:
            result_type = result["type"]

        if item["type"] != result_type:
            match_errors.append("type")
            one_result["type_diff"] = "{}->{}".format(item["type"], result_type)

        if result:
            if item["province"] != result["province"]:
                match_errors.append("province")

            if item["type"] in ["city", "district"]:
                if item["city"] != result.get("city", ""):
                    match_errors.append("city")

            if item["type"] in ["district"]:
                if item["district"] != result.get("district", ""):
                    match_errors.append("district")

        one_result["match_error_count"] = len(match_errors)
        one_result["result_type"] = result_type

    logging.info("accuracy = {} match_error_count_0/all".format(
        1.0 * len([x for x in test_results if x["match_error_count"] == 0])/len(test_results)))
    stat(test_results, [], ["match_error_count", "type_diff", "result_type"])


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)  # noqa

    main_subtask(__name__)

"""
    python cdata/region.py task_guess_all_batch

    python cdata/region.py task_guess_all
"""
