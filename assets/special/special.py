import urllib.request
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#读取文本方法
def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

all_lines =  []
#读取文本
excudelist_lines=read_txt_to_array('assets/special/ExcludeList.txt') 

def convert_m3u_to_txt(m3u_content):
    lines = m3u_content
    txt_lines = []
    channel_name = ""

    # 解析 M3U 格式内容
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTM3U"):
            continue
        if line.startswith("#EXTINF"):
            channel_name = line.split(",")[-1].strip()
        elif line.startswith(("http", "https", "rtmp", "p3p", "p2p")):
            txt_lines.append(f"{channel_name},{line}")

    return "\n".join(txt_lines)


def process_url(url):
    try:

        # 创建一个请求对象并添加自定义header
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # 打开URL并读取内容
        with urllib.request.urlopen(req) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            # 逐行处理内容
            lines = text.split('\n')

            # 判断是否是m3u格式，如果是特别处理。↓↓↓↓↓↓↓
            # 如果第一行是 "#EXTM3U"，则判断为 M3U 文件，转换为 TXT 格式
            if lines[0].strip().startswith("#EXTM3U"): 
                newlines = convert_m3u_to_txt(lines)
                lines = newlines.split('\n')  #使用转换后的内容重新赋值给 lines
            # 判断是否是m3u格式，如果是特别处理。↑↑↑↑↑↑↑

            print(f"行数: {len(lines)}")
            for line in lines:
                line = line.strip()
                if  "#genre#" not in line and "," in line and "://" in line and line not in excudelist_lines:
                    # 拆分成频道名和URL部分
                    # channel_name, channel_address = line.split(',', 1)
                    all_lines.append(line.strip())

    except Exception as e:
        print(f"处理URL时发生错误：{e}")


# 定义
urls = [
    "https://ua.fongmi.eu.org/box.php?url=https://xn--dkw0c.v.nxog.top/m/tv",
    "https://ua.fongmi.eu.org/box.php?url=http://%E6%88%91%E4%B8%8D%E6%98%AF.%E6%91%B8%E9%B1%BC%E5%84%BF.com/live.php",
    "https://ua.fongmi.eu.org/box.php?url=http://sinopacifichk.com/tv/live",
    "https://ua.fongmi.eu.org/box.php?url=https://tv.iill.top/m3u/Gather",
]
# 处理
for url in urls:
    if url.startswith("http"):        
        # print(f"time: {datetime.now().strftime("%Y%m%d_%H_%M_%S")}")
        print(f"处理URL: {url}")
        process_url(url)


# 将合并后的文本写入文件
output_file = "assets/special/special.txt"


try:
    # 
    # print(f"time: {datetime.now().strftime("%Y%m%d_%H_%M_%S")}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")
    # print(f"time: {datetime.now().strftime("%Y%m%d_%H_%M_%S")}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")




def encrypt_file_inplace(file_path, key):
    # 生成一个随机的初始化向量（IV）
    iv = os.urandom(16)
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    # 填充明文
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    
    # 创建AES加密器
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # 加密明文
    ciphertext = iv + encryptor.update(padded_plaintext) + encryptor.finalize()
    
    # 使用临时文件存储加密后的内容
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        with open(temp_file_path, 'wb') as f:
            f.write(ciphertext)
    
    # 覆盖原始文件
    os.replace(temp_file_path, file_path)
    
    print(f"文件 {file_path} 已成功加密并覆盖原始文件。")

# 将密码"abcd"（需要是16、24或32字节长度）转换为字节串
# 注意：这里为了示例，简单地将密码重复以匹配AES密钥长度要求
# 在实际应用中，应该使用更安全的密钥生成方法，如密码哈希或密钥派生函数
password = b'abcd' * 8  # 重复密码以匹配AES-256的32字节密钥长度要求

# 指定要加密的文件路径
file_path = 'assets/special/special.txt'  # 替换为你的文件路径

# 调用加密函数
encrypt_file_inplace(file_path, password)
