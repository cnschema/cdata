#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from cdata.region import RegionEntity  # noqa

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class EntityTestCase(unittest.TestCase):
    def setUp(self):
        self.ner = RegionEntity()
        pass

    def test_misc(self):
        ret = self.ner.normalize_region_name(u"市辖区", "province")
        assert ret == u"市辖区", u"[]".format(ret)
        # TODO self.ner.normalize_region_name(u"安huisheng", "province")
        assert u"安徽省" == self.ner.normalize_region_name(u"安徽", "province")
        assert u"内蒙古自治区" == self.ner.normalize_region_name(u"内蒙古", "province")
        assert u"哈尔滨市" == self.ner.normalize_region_name(u"哈尔滨", "city")
        assert u"乌鲁木齐市" == self.ner.normalize_region_name(u"乌鲁木齐", "city")
        assert u"道里区" == self.ner.normalize_region_name(u"道里区", "district")
        assert u"海淀区" == self.ner.normalize_region_name(u"海淀区", "district")
        assert u"海淀区" == self.ner.normalize_region_name(u"海淀", "district")
        assert u"浦东新区" == self.ner.normalize_region_name(u"浦东", "district")
        assert u"浦东新区" == self.ner.normalize_region_name(u"浦东新区", "district")

        assert u"上海" == self.ner.guess_province([u"上海西红柿集团"])
        assert u"上海" == self.ner.guess_province([u"浦东新区软件园"])
        assert u"辽宁" == self.ner.guess_province([u"朝阳市软件园"])
        assert u"内蒙古" == self.ner.guess_province([u"内蒙古自治区乌兰察布市丰镇市新标路丰美北小区232号"])
        assert u"天津" == self.ner.guess_province([u"天津市食品药品监督管理局"])
        assert u"内蒙古" == self.ner.guess_province([u"内蒙乌兰察布市丰镇市新标路丰美北小区232号"])

    def test_guess_all(self):

        city_info = self.ner.guess_all([u"内蒙古自治区乌兰察布市丰镇市新标路丰美北小区232号"])
        assert u"district" == city_info.get("type")
        assert u"内蒙古自治区" == city_info.get("province")
        assert u"乌兰察布市" == city_info.get("city")
        assert u"丰镇市" == city_info.get("district")

        city_info = self.ner.guess_all([u"高州市平山木禾塘大塘村"])
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        city_info = self.ner.guess_all([u"珠海市拱北新市花园16栋102铺"])
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        city_info = self.ner.guess_all([u"南溪镇扬美刘大道中段老祠村道脚008号"])
        assert None is city_info

        city_info = self.ner.guess_all(["新塘镇大敦村", "增城市新塘众生药店"])
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        city_info = self.ner.guess_all(["曲江县马坝城南", "曲江县马坝镇金良兽药店"])
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        city_info = self.ner.guess_all(["镇平路４６号、４８号", "汕头经济特区粤东药品公司镇平商店"])
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["遂溪县河头镇文明街12号", "遂溪县河头回春堂药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = [u"延寿镇南东风路", u"旺旺兽药店（延寿县）"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"黑龙江省" == city_info.get("province")

        inputdata = ["", "富拉尔基秀坤百货商店药品专柜"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"黑龙江省" == city_info.get("province")

        inputdata = ["兴隆工商局家属楼", "巴彦县鑫丰兽药饲料商店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"黑龙江省" == city_info.get("province")

        inputdata = ["下城子镇中心街", "穆棱市下城子镇宋大夫兽药饲料店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"黑龙江省" == city_info.get("province")

        inputdata = ["加格达奇区前进路（红旗东风一号楼）", "加格达奇区温馨大药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"黑龙江省" == city_info.get("province")
        assert u"district" == city_info.get("type")
        assert u"加格达奇区" == city_info.get("name")

        inputdata = ["", "北京神州汽车租赁有限公司深圳雅园分公司"]
        city_info = self.ner.guess_all(inputdata)
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["横山横安路镇政府出租屋第一间", "廉江市横山济生堂药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["水东镇东阳北街50号", "水东镇长安药店（已迁入三角所）"]
        city_info = self.ner.guess_all(inputdata)
        assert None is city_info

        inputdata = ["龙门县龙城林园街33号", "龙城新利药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["黄石街道", "龙川县药材公司黄石药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["", "盘锦阳光大药房医药连锁有限公司清远麦围店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["", "盘锦阳光大药房医药连锁有限公司清远市清城区城市广场店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["四会市东城区四会大道南时代商贸广场141号（首层）", "广州仁参医药连锁有限公司四会时代分店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["中山市南朗镇岭南小区", "中山市南朗镇启发农药化肥店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["信宜市镇隆圩解放街29号", "信宜市镇隆回春药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["乳源县大桥镇乳阳林业局溪头河西区域避暑林庄温泉大饭店主楼一楼", "东阳光药零售连锁（东莞）有限公司南岭店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["从化市太平镇神岗木棉村永三社（龟塘）", "从化市太平民健药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["荔城镇和平路33号首层", "增城市荔城育善堂药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")
        assert u"广州市" == city_info.get("city")

        inputdata = ["清新县太和镇滨江路东三街13号首层5号铺", "清新县太和安顺堂药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["广州市番禺区小谷围街广州大学城外环西路230号广大商业中心A区首层1015", "桂林市春和堂医药连锁有限责任公司广州大学城分店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["深圳市龙岗区龙岗街道南联社区向银路与怡丰路交叉路口南龙综合楼首层之三", "太仓市三庆医药连锁有限公司深圳南联店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["中山市南区寮后村龙子街14号", "中山市南区仁德堂药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["", "珠海嘉伦药业集团光彩大药房连锁有限公司红旗分店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"city" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["东区新街村", "同江市龙鑫堂大药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"黑龙江省" == city_info.get("province")

        inputdata = ["新兴县河头镇河头街65号", "新兴县河头镇同源堂药店"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")

        inputdata = ["怀集怀城镇河南第二卫生站"]
        city_info = self.ner.guess_all(inputdata)
        assert u"district" == city_info.get("type")
        assert u"广东省" == city_info.get("province")


if __name__ == '__main__':
    unittest.main()
