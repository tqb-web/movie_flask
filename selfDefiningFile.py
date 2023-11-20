## 相关模块引入
import pandas as pd

## jiaba分词添加自定义词典，以保证电影名称分词正确
## 自定义词典构建时，分别写入 名词 词频 词性(词性，可以省略，但建议自定义写出，方便后续使用)
# 读取原数据库
storage_df = pd.read_csv('./movie.csv', encoding='utf-8')
movieNameLst = [name for name in storage_df['movie_cname']]

# 构建自定义词典
with open('./selfDefiningTxt.txt', 'w', encoding='utf-8') as f:
    for name in movieNameLst:
        f.write(name + ' 100 tqb')
        f.write('\n')

# 获取用户输入的两个数字
num1 = float(input("请输入第一个数字: "))
num2 = float(input("请输入第二个数字: "))

# 计算两个数字的和
sum = num1 + num2

# 输出结果
print(f"{num1} + {num2} = {sum}")

