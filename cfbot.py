""" 
Author:彭康杰
id:3121003076
class:25届土木工程3班
createdate:2023-3-17
"""
import time  # 时间库
import os  # 系统库
import ctypes  # 系统库
import sys  # 系统库
import shutil  # 文件复制
import requests  # 请求库
import imgkit  # html转图片库

from PIL import Image, ImageFont, ImageDraw, features  # 绘图库
from datetime import datetime  # 日期库
from pyecharts.components import Table  # 制表库
from pyecharts.options import ComponentTitleOpts, TitleOpts
from codeforces import api  # 调用codeforce api 获取数据

# api获取用户提交数据


def get_submission(user):
    info = api.call('user.status', handle=user)
    return info


# 获取到的用户信息样例
""" 
{'country': 'China', 
'lastOnlineTimeSeconds': 1679113010, 
'rating': 1310, 
'friendOfCount': 16, 
'titlePhoto': 'https://userpic.codeforces.org/2340352/title/565bd419495f7044.jpg', 
'handle': 'Paxton', 
'avatar': 'https://userpic.codeforces.org/2340352/avatar/28668b1bc41dc1de.jpg', 
'contribution': 0, 
'organization': 'GDUT', 
'rank': 'pupil', 
'maxRating': 1426, 
'registrationTimeSeconds': 1638163703, 
'maxRank': 'specialist'}
 """

# 获取到的提交信息样例
""" 
[{'id': 197381144, ----
'contestId': 975, -----
'creationTimeSeconds': 1678801190, 
'relativeTimeSeconds': 2147483647, -----
'problem': {'contestId': 975, 
            'index': 'C', 
            'name': 'Valhalla Siege', 
            'type': 'PROGRAMMING', ----------------
            'points': 1500.0,       ----------------
            'rating': 1400, 
            'tags': ['binary search']}, 
'author': {'contestId': 975, -----------------
            'members': [{'handle': 'Paxton'}], ----------
            'participantType': 'PRACTICE', 
            'ghost': False, 
            'startTimeSeconds': 1525183500}, 
            
'programmingLanguage': 'GNU C++17 (64)', 
'verdict': 'OK', 
'testset': 'TESTS', 
'passedTestCount': 35, 
'timeConsumedMillis': 1404, 
'memoryConsumedBytes': 1638400}] 
"""

""" 
{
'creationTimeSeconds': 1678801190, 
'problem': {
    'contestId': 975, 
    'index': 'C', 'name': 
    'Valhalla Siege', 
    'points': 1500.0, 
    'rating': 1400}, 
'verdict': 'OK'}
"""


# 计算日期差,传入应为字符串类型
def Caltime(date1, date2):
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    return date2-date1

# 处理提交数据，筛选出指定日期至当前日期的所有ac并返回


def Process_SubmissionData():
    p_info = []
    require_date = time.mktime(set_info["require_date"])  # 获取查询时间
    for i in range(len(submission_info)):
        del submission_info[i]['id']  # 删除获取到的无用信息
        del submission_info[i]['relativeTimeSeconds']
        del submission_info[i]['contestId']
        del submission_info[i]['problem']['type']
        # del submission_info[i]['problem']['tags']
        # del submission_info[i]['problem']['points']
        del submission_info[i]['author']
        del submission_info[i]['programmingLanguage']
        del submission_info[i]['testset']
        del submission_info[i]['passedTestCount']
        del submission_info[i]['timeConsumedMillis']
        del submission_info[i]['memoryConsumedBytes']

        if (submission_info[i]["creationTimeSeconds"] >= require_date and submission_info[i]["verdict"] == 'OK'):
            p_info.append(submission_info[i])
        elif (submission_info[i]["creationTimeSeconds"] < require_date):
            break
    return p_info


# 获取用户信息并判断正确性
def get_user():
    while True:
        user_name = input('请输入需要查询的用户名：')
        try:
            info = api.call('user.info', handles=user_name)
            break
        except:
            print("该用户不存在")
    return info


""" 
def check_json():
    with open("python/bot/user.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
    print(user_data)
 """

# 设置工作模式，暂时仅有日期设置


def set_workmod():
    info = {}
    # 需要查询的日期范围
    while True:
        check = input("需要查询的日期(yyyy-mm-dd):")
        check = check+" 00:00:00"
        try:
            date = time.strptime(check, "%Y-%m-%d %H:%M:%S")
            info["require_date"] = date
            # print(info["requeir_date"])
            break
        except ValueError:
            print("日期格式错误，请重新输入")
    return info


# 动态获取绝对路径
def load_txt(file):
    module_path = os.path.dirname(__file__)  # 获取当前文件所在的绝对路径
    filename = os.path.join(module_path, file)  # 拼接当前路径和相对路径
    return filename  # 打开并读取文件内容


# 获取文字尺寸，动态定位
def get_size(draw, x, y, text, font, direction):
    return draw.textbbox(xy=(x, y), text=text, font=font, direction=direction)
# textbbox方法返回一个四元组(left, top, right, bottom)，表示文本相对于锚点坐标xy在图像上所占用区域矩形框左上角和右下角坐标。


def generate_image():
    generate_table()  # 生成提交表格图片
    # ---------下载头像
    response = requests.get(
        url=user_info[0]['titlePhoto'], timeout=10, headers=headers, stream=True)
    content = response.content
    with open(load_txt('picture\\head_photo.png'), "wb") as f:
        f.write(content)

    # -----------------------------文件路径、颜色、坐标------------------------------------
    generate_path = load_txt('')         # 图片生成路径
    logo_path = load_txt('picture\\cf_logo.png')  # logo路径
    bg_path = load_txt('picture\\bg.png')         # 背景图路径
    font_path = load_txt('LXWK.ttf')     # 字体路径
    hd_path = load_txt('picture\\head_photo.png')
    table_path = load_txt('picture\\table.png')

    logo_x = 15    # logo坐标
    logo_y = 0
    user_x = 430   # 用户信息坐标
    user_y = 10
    table_x = 40
    table_y = 80
    font_color = (0, 0, 0)  # 字体颜色

    # ------------------------------加载图片与字体-----------------------------------------
    user_font = ImageFont.truetype(font=font_path, size=20)  # 创建字体对象
    # ------
    cf_logo = Image.open(logo_path)  # 创建 image 对象
    bg = Image.open(bg_path)
    head_photo = Image.open(hd_path)
    table_photo = Image.open(table_path)
    # ------
    cf_logo.convert("RGBA")   # 设置图像模式为RGBA
    bg.convert("RGBA")        # 设置图像模式为RGBA
    head_photo.convert("RGBA")        # 设置图像模式为RGBA
    table_photo.convert("RGBA")
    # ------
    head_photo = head_photo.resize(size=(70, 70))
    # -------------------------------预处理背景尺寸------------------------------------------
    table_size = table_photo.size
    bg_size = bg.size

    new_size = (bg_size[1], bg_size[1]+(table_size[1]+100-bg_size[1]))
    bg = bg.resize(size=new_size)

    # ------------------------------绘制logo及个人信息--------------------------------------
    bg.paste(im=cf_logo, box=(logo_x, logo_y))   # 粘贴logo
    bg.paste(im=head_photo,
             box=(logo_x+cf_logo.size[0]+30, logo_y+5))   # 粘贴用户头像
    bg.paste(im=table_photo, box=(table_x, table_y))
    # ---
    draw = ImageDraw.Draw(bg)                    # 实例化可以在指定图像上画图的 Draw 对象
    # ---
    draw.text(xy=(user_x, user_y),
              text="用户名:" + str(user_info[0]['handle']),
              fill=font_color,
              font=user_font)   # 以用户信息坐标绘制用户名

    user_size = get_size(draw, user_x, user_y, "用户名:" +
                         str(user_info[0]['handle']), user_font, 'ltr')       # 计算用户名字符长宽
    # ---
    # print(user_size[0], user_size[1], user_size[2], user_size[3])
    # ---
    draw.text(xy=(user_x, user_size[3]+5), text="当前rating:"+str(user_info[0]
              ['rating']), fill=font_color, font=user_font)             # 计算得rating坐标后将其绘制

    # -----------------------
    # 保存图片于指定路径
    bg.save(fp=generate_path + 'generate\\'+user_info[0]['handle'] + '.png')


# 调用pyecharts生成table表格并转换为图片
def generate_table():
    rows = []  # 存储行数据
    headers = ["id", "name", "Rating", "tags", "date"]  # 定义列数据

    for i in range(len(processed_info)):                           # 遍历题目数据生成行数据
        timestamp = int(processed_info[i]['creationTimeSeconds'])  # ac时间戳
        dt = datetime.fromtimestamp(timestamp)  
        date = dt.strftime('%Y-%m-%d')                             # ac时间戳转日期
        # -----
        id = str(processed_info[i]['problem']['contestId']) + \
            str(processed_info[i]['problem']['index'])             # 题目id
        rating = '----'                                            # 题目rating
        tags = ''                                                  # 题目标签
        temp = str(processed_info[i]['problem']['name'])           # 题目完整名称
        name = ''
        for j in range(len(temp)):               # 题目名称改写
            name = name + temp[j]
            if ((j+1) % 20 == 0 and j != 0):     # 每20个字符换行
                name = name+'\n'
        
        # -----
        for j in range(len(processed_info[i]['problem']['tags'])):
            if len(processed_info[i]['problem']['tags']) == 0:
                break
            tags = tags+processed_info[i]['problem']['tags'][j]+','  # 标签拼接
            if ((j+1) % 3 == 0 and j != 0):  # 每3个标签换行
                tags = tags+'\n'
        if ('rating' in processed_info[i]['problem']):  # 存在部分题目无rating
            rating = processed_info[i]['problem']['rating']
        rows.append([id, name, rating, tags, date])

    table = Table()
    table.add(headers, rows)

    problem_num = len(rows)   # 题目数量
    date = time.strftime("%Y-%m-%d", set_info['require_date'])
    sub_title = date+' 起截至 '+datetime.now().date().strftime("%Y-%m-%d") + \
        ' 共ac '+str(problem_num)+' 道题'
    # ----------------------------设置表格样式--------------------------------
    table.set_global_opts(title_opts=ComponentTitleOpts(subtitle=sub_title, subtitle_style={
                          'fontSize': 20, 'color': '#000000', 'fontFamily': 'LXGW WenKai'}))   # 设置表格标题
    table.render(load_txt("generate\\table_base.html"))     # 生成html文件
    # --------------------------html转图片------------------------------
    # wkhtmltoimage.exe路径
    path_wkimg = load_txt('wkhtmltox\\bin\\wkhtmltoimage.exe')
    cfg = imgkit.config(wkhtmltoimage=path_wkimg)            # 配置imgkit
    imgkit.from_file(load_txt('generate\\table_base.html'),
                     load_txt('picture\\table.png'), config=cfg)   # 生成图片


def check_environment():
    print('正在检查必要环境')
    if features.check('raqm') == False:
        print("缺少raqm")
        time.sleep(2)
        if ctypes.windll.shell32.IsUserAnAdmin() == False:
            print("将请求管理员权限以安装raqm，安装完成后将自动重启代码")
            time.sleep(2)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
            time.sleep(2)
            sys.exit()
        shutil.copy(load_txt('fribidi-0.dll'), sys.path[4])
        shutil.copy(load_txt('libraqm.dll'), sys.path[4])
        if features.check('raqm') == False:
            print('raqm安装失败，可能是文件夹权限问题导致')
        else:
            print("已自动安装raqm")
    else:
        print('environment OK')
        time.sleep(2)


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43"
}

if __name__ == '__main__':
    start_time = time.time()  # 开始计时
    check_environment()   # 检查环境
    set_info = set_workmod()   # 设置工作模式
    user_info = get_user()  # 获取用户信息
    submission_info = get_submission(user_info[0]['handle'])  # 获取用户提交记录
    processed_info = Process_SubmissionData()   # 处理提交记录
    generate_image()  # 生成图片
    print('生成图片成功，用时：', time.time()-start_time, 's')
