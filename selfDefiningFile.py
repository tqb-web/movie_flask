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


def generate_fibonacci(n):
    fibonacci_sequence = [0, 1]  # 初始的斐波那契序列

    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    while len(fibonacci_sequence) < n:
        next_number = fibonacci_sequence[-1] + fibonacci_sequence[-2]
        fibonacci_sequence.append(next_number)

    return fibonacci_sequence

# 打印前 10 个斐波那契数
n = 10
fibonacci_sequence = generate_fibonacci(n)
print(f"前 {n} 个斐波那契数列为: {fibonacci_sequence}")