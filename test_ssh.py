import paramiko
import sys

hostname = "192.168.159.128"
username = "wangping"
password = "123456"

try:
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"正在连接到 {hostname}...")
    client.connect(hostname, username=username, password=password, timeout=10)
    
    print("连接成功！")
    
    # 执行简单命令
    stdin, stdout, stderr = client.exec_command("uname -a")
    output = stdout.read().decode()
    print(f"系统信息: {output}")
    
    stdin, stdout, stderr = client.exec_command("lsb_release -a")
    output = stdout.read().decode()
    print(f"Ubuntu版本: {output}")
    
    stdin, stdout, stderr = client.exec_command("free -h")
    output = stdout.read().decode()
    print(f"内存信息: {output}")
    
    stdin, stdout, stderr = client.exec_command("df -h")
    output = stdout.read().decode()
    print(f"磁盘信息: {output}")
    
    client.close()
    print("测试完成！")
    
except Exception as e:
    print(f"连接失败: {e}")
    sys.exit(1)