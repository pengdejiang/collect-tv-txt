from ftplib import FTP, all_errors
import os
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
# 创建一个FTP对象
ftp = FTP()
connected = False

try:
    # 连接到FTP服务器
    ftp.connect('183.230.145.221', 9991)  # 指定主机和端口号
    ftp.login('pengdejiang1', '754264')  # 指定用户名和密码
    connected = True
    logging.info('成功连接到FTP服务器')
    
    # 设置为被动模式
    ftp.set_pasv(True)  # 将FTP连接设置为被动模式
    logging.info('FTP连接已设置为被动模式')
    
    ftp.cwd('/github-jump')  # 切换到FTP服务器的指定目录
    logging.info(f'已切换到FTP服务器的目录: /luffy9847-out')

    # 设置本地目录以查找文件
    local_directory = 'assets/special/'  # 当前目录，你可以根据需要修改
    logging.info(f'本地目录设置为: {local_directory}')

    # 遍历本地目录以查找所有名称包含特定字符串的文件
    patterns = {'special.txt'}
    for filename in os.listdir(local_directory):
        if any(pattern in filename for pattern in patterns):
            # 构建文件的完整路径
            file_path = os.path.join(local_directory, filename)
            
            # 检查是否是一个文件（而不是目录）
            if os.path.isfile(file_path):
                # 打开文件并上传
                with open(file_path, 'rb') as f:
                    # 使用STOR命令上传文件
                    ftp.storbinary(f'STOR {filename}', f)
                    logging.info(f"{filename} 上传成功！")

except all_errors as e:
    logging.error(f"FTP 错误: {e}")
    if connected and ftp.file is not None:
        logging.error(f"FTP 响应代码: {ftp.getresp()}")
    else:
        logging.error("无法获取 FTP 响应，因为连接未建立或已关闭。")
finally:
    if connected:
        try:
            ftp.quit()  # 关闭FTP连接
            logging.info('FTP连接已关闭')
        except:
            logging.warning('在关闭FTP连接时发生异常，但已忽略')
