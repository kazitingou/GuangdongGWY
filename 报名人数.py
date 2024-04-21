import requests
import ast
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

# 创建cookies字典
cookies = {
    'JSESSIONID': '自己添加这一段',   #每隔一段时间他会变
    '_gscu_260182935': '和这一段',      #写过一次就不会变了 
    '../issoYH_MASS_TOKEN': '还有这一段',  #每隔一段时间他会变
}

# 创建headers字典
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Origin': 'https://ggfw.hrss.gd.gov.cn',
    'Referer': '这一段也需要一直改',  #改这一段
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand)";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# 构建 data 字典用于post请求的参数
data = {
  'bfa001': '2412121',
  'bab301': '20', #20揭阳 19潮州  04汕头 想要什么省份自己查
  'page': '1',
  'rows': '1250'
}

# 选择地区
choose = 0 #0揭阳 1汕头 2潮州
if choose == 0:
    #揭阳目标岗位代码，手动填入
    job_code = ['2412121200014','2412121200001','2412121200015','2412121200036','2412121200075','2412121200086','2412121200068','2412121200082','2412121200102','2412121200136','2412121200183','2412121200185']
    # 揭阳限定应届生
    limited_codes = ['2412121200015', '2412121200082', '2412121200102', '2412121200185']
    data['bab301'] = '20'
elif choose == 1:
    #汕头目标岗位代码
    job_code = ['2412121040013','2412121040038','2412121040062','2412121040159','2412121040163','2412121040452','2412121040535','2412121040551','2412121040557','2412121040812','2412121040845','2412121040850','2412121040855','2412121040887','2412121040949','2412121040994','2412121041030','2412121041033','2412121041034','2412121041038','2412121041058','2412121041128','2412121041150','2412121041153','2412121041177','2412121041189','2412121041190','2412121041198','2412121041203']
    # 汕头
    limited_codes = ['2412121041198','2412121041203']
    data['bab301'] = '04' 
elif choose == 2:
    #潮州目标岗位代码
    job_code = ['2412121190001','2412121190020','2412121190027','2412121190098','2412121190109','2412121190117','2412121190214']
    # 潮州
    limited_codes = []
    data['bab301'] = '19'


# 发送请求
response = requests.post('https://ggfw.hrss.gd.gov.cn/sydwbk/exam/details/spQuery.do', cookies=cookies, headers=headers, data=data).text

# 使用 ast.literal_eval() 将字符串转换为对象
str_obj = response
obj = ast.literal_eval(str_obj)['rows']
# print(obj)  # 输出对象



tab = {
    'bfe301': '岗位代码', 
    'aab004' : '招聘单位',
    'aab019' : '聘用人数',
    'aab119': '报名人数', 
    'bfe3a4': '招聘岗位', 
}


#选择目标岗位
# aim_job = obj  
aim_job = []
for o in obj:
    if o['bfe301'] in job_code:
        aim_job.append(o)

print(aim_job)

# 提取绘制柱状图所需的数据，并合并单位和岗位
job_labels = [f"{job['aab004']} - {job['bfe3a4']} - {job['aab019']}" for job in aim_job]
applicants = [int(job['aab119']) for job in aim_job]

# 制成柱状图
plt.figure(figsize=(14, 8))

# 为 Limited Codes 的柱状条设置颜色 应届为蓝，非为青
colors = ['b' if job['bfe301'] in limited_codes else 'c' for job in aim_job]
bars = plt.bar(job_labels, applicants, color=colors)

# 在每个柱形上方显示数字标签
for bar, label, applicant in zip(bars, job_labels, applicants):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(applicant), ha='center', va='bottom')


# 设置柱状图的其他参数
plt.xlabel('单位名称 - 招聘岗位 - 聘用人数')
plt.ylabel('申请人数')
plt.title('不同岗位的申请人数')
plt.xticks(rotation=45, ha="right") 

plt.tight_layout() 
plt.show()