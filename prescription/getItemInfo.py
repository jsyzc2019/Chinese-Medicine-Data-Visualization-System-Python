import requests
from bs4 import BeautifulSoup
import jieba

jieba_data = {'干姜', '柴胡', '佛手', '木蝴蝶', '土茯苓', '朱砂', '茺蔚子', '夏枯草', '甘草', '蒲黄', '海螵蛸',
              '巴戟天', '天葵子', '蝉蜕', '蜈蚣', '谷芽', '大血藤', '秦艽', '金钱白花蛇', '垂盆草', '白头翁', '木鳖子',
              '鸡冠花', '益母草', '鹿衔草', '绵萆薢', '羚羊角', '商陆', '牛蒡子', '芒硝', '路路通', '葛根', '金荞麦',
              '荆芥', '全蝎', '红花', '青果', '芦根', '皂角刺', '核桃仁', '酸枣仁', '苦楝皮', '山楂', '桂枝', '太子参',
              '滑石', '罗布麻叶', '漏芦', '玄参', '牛黄', '侧柏叶', '石菖蒲', '鸡内金', '重楼', '五味子', '浙贝母',
              '千年健', '三棱', '海金沙', '辛夷', '天南星', '鸡蛋花', '乌梅', '白鲜皮', '紫苏子', '海马', '狼毒',
              '土木香', '山楂叶', '杜仲叶', '补骨脂', '芥子', '鹿茸', '京大戟', '蟾酥', '当归', '甘松', '五加皮',
              '白术', '银杏叶', '枇杷叶', '天花粉', '赤芍', '龙胆', '独活', '自然铜', '火麻仁', '黄芩', '鸦胆子',
              '降香', '月季花', '罗汉果', '青皮', '水红花子', '山柰', '北沙参', '马勃', '杜仲', '韭菜子', '蛤蚧',
              '土鳖虫', '檀香', '冬虫夏草', '穿心莲', '白茅根', '枸骨叶', '小蓟', '没药', '红芪', '西洋参', '瞿麦',
              '青葙子', '关黄柏', '炉甘石', '莪术', '黄精', '鸡血藤', '草乌', '绞股蓝', '蔓荆子', '大枣', '前胡',
              '高良姜', '香附', '川楝子', '钩藤', '丹参', '珍珠母', '使君子', '委陵菜', '乌梢蛇', '薄荷', '大腹皮',
              '香加皮', '阿魏', '拳参', '枸杞子', '仙鹤草', '胖大海', '伸筋草', '百部', '远志', '红景天', '秦皮',
              '淫羊藿', '山药', '僵蚕', '竹茹', '石斛', '柏子仁', '栀子', '川芎', '桑枝', '粉葛', '白芷', '威灵仙',
              '王不留行', '麦芽', '灯心草', '何首乌', '常山', '马钱子', '山茱萸', '瓦楞子', '旋覆花', '椿皮', '海藻',
              '车前子', '厚朴', '茯苓', '百合', '苦参', '莱菔子', '五倍子', '石膏', '化橘红', '天麻', '木香', '砂仁',
              '延胡索', '防己', '猪苓', '牛膝', '白芍', '麻黄', '南板蓝根', '八角茴香', '花椒', '薤白', '人参', '菝葜',
              '半夏', '豆蔻', '马兜铃', '棕榈', '楮实子', '大青叶', '卷柏', '凌霄花', '苏木', '相思子', '虫白蜡',
              '黄芪', '赤小豆', '南鹤虱', '桃仁', '虎杖', '牵牛子', '地骨皮', '蓖麻子', '榧子', '白蔹', '鹤虱',
              '红豆蔻', '川乌', '冬葵果', '稻芽', '鱼腥草', '槐花', '石决明', '赭石', '麦冬', '朱砂根', '金银花',
              '地榆', '菊花', '藁本', '泽泻', '牡丹皮', '土贝母', '土荆皮', '胡黄连', '青礞石', '大黄', '仙茅',
              '南沙参', '薏苡仁', '络石藤', '菟丝子', '沉香', '续断', '地黄', '蒺藜', '射干', '白扁豆', '银柴胡',
              '芫花', '九里香', '苍术', '蛤壳', '罂粟壳', '广藿香', '番泻叶', '乌药', '洋金花', '天竺黄', '莲子心',
              '甘遂', '桑寄生', '南五味子', '白附子', '生姜', '香橼', '白薇', '肿节风', '青黛', '郁李仁', '郁金',
              '蕲蛇', '磁石', '紫石英', '紫草', '牡蛎', '香薷', '枳实', '粉萆薢', '诃子', '天仙子', '胡椒', '金礞石',
              '板蓝根', '肉豆蔻', '肉桂', '山慈菇', '丁香', '豨莶草', '雄黄', '白前', '乳香', '灵芝', '苦杏仁', '槟榔',
              '升麻', '蒲公英', '金钱草', '通草', '陈皮', '水飞蓟', '水牛角', '葶苈子', '芦荟', '红大戟', '金樱子',
              '三七', '复盆子', '木贼', '决明子', '莲子', '紫苏梗', '胡芦巴', '老鹳草', '丝瓜络', '白矾', '猪牙皂',
              '木通', '荷叶', '广金钱草', '玉竹', '淡竹叶', '枫香脂', '桑椹', '柿蒂', '鸡屎藤', '蛇蜕', '黄连',
              '小茴香', '青蒿', '龙眼肉', '山银花', '山麦冬', '芡实', '玄明粉', '麝香', '鸡骨草', '草果', '斑蝥',
              '合欢花', '忍冬藤', '佩兰', '川木香', '车前草', '白花蛇舌草', '血竭', '锁阳', '刀豆', '徐长卿', '儿茶',
              '桑白皮', '蛇床子', '桔梗', '冰片', '白及', '禹州漏芦', '狗脊', '吴茱萸', '牡荆叶', '槲寄生', '水蛭',
              '川贝母', '女贞子', '紫苏叶', '党参', '青风藤', '川木通', '荜茇', '红参', '绵马贯众', '刺五加', '山豆根',
              '茜草', '腊梅花', '细辛', '阿胶', '天山雪莲', '款冬花', '姜黄', '知母', '益智', '大蓟', '西红花',
              '草豆蔻', '白果', '茵陈', '石韦', '北豆根', '平贝母', '泽兰', '半边莲', '川牛膝', '龟甲', '羌活',
              '野菊花', '枳壳', '附子', '巴豆', '千金子', '余甘子', '地肤子', '槐角', '地龙', '苍耳子', '玫瑰花',
              '桑螵蛸', '肉苁蓉', '天冬', '木瓜', '闹羊花', '明党参', '瓜蒌', '谷精草', '骨碎补', '桑叶', '鳖甲',
              '两面针', '淡豆豉', '紫菀', '昆布', '连翘', '黄柏', '防风'}


def getByURL(url):
    prescription_info = {'名称': '', '拼音': '', '分类': '', '组成': '',
                         '用法': '', '功用': '', '主治': '', '病机': '',
                         '运用': '', '附方': '', '方歌': '', '附注': '',
                         '出处': '', '图片路径': '', '药材': ''
                         }
    url = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    img_url = soup.find('div', {'id': 'solutionmod-pic-section'}).find('img').get('src')  # 获取方剂的图片路径
    prescription_info.update({'图片路径': img_url})
    info_list = (soup.find('div', {'class', 'px-5'})
                 .find('div', {'class': 'small'})
                 .find_all('div', {'class': ['border-bottom', 'border-light', 'py-3']}))
    for info in info_list:
        try:
            title = info.find('strong').get_text().strip()  # 每条概述的标题
            text = info.get_text().strip().replace(title, '')  # 每条概述标题对应的详细信息(除去了该概述的标题)
            if title == '组成':
                ts = jieba.lcut(text)
                yc_db = []
                for d in ts:
                    if d in jieba_data:  # 如果该分词出来的词语在 jieba库中，才新增数据，用于确定该方剂由哪些药材组成
                        yc_db.append(d)
                yc_db_text = ','.join(yc_db)
                prescription_info.update({'药材': yc_db_text})  # 更新方剂的药材组成

            prescription_info.update({title: text})  # 更新方剂属性信息

        except AttributeError as e:
            print('Error!', e)
            continue

    return prescription_info
