import RPi.GPIO as GPIO
import time
import logging
from datetime import datetime

# 设置 GPIO 模式
GPIO.setmode(GPIO.BCM)

# 定义 GPIO 引脚
UP_PIN = 23
ENTER_PIN = 24

# 设置 GPIO 为输出模式
GPIO.setup(UP_PIN, GPIO.OUT)
GPIO.setup(ENTER_PIN, GPIO.OUT)

# 初始化日志
logging.basicConfig(filename='./run.log', level=logging.INFO)

def log_action(action):
    """记录动作到日志文件并打印"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{timestamp} - {action}"
    print(message)
    logging.info(message)

def press_button(pin):
    """按下指定按钮（GPIO 引脚）"""
    GPIO.output(pin, GPIO.LOW)  # 按下
    time.sleep(0.2)             # 持续 0.2 秒
    GPIO.output(pin, GPIO.HIGH) # 松开
    time.sleep(0.03)            # 稍作延迟，模拟按键松开

def enter_password(password):
    """输入指定的密码"""
    log_action(f"开始输入密码：{password}")
    for i, digit in enumerate(password):
        if i == 0:
            # 初始按下两次 ENTER
            press_button(ENTER_PIN)
            press_button(ENTER_PIN)

        # 按 UP 调整当前位
        for _ in range(int(digit) + 1):
            press_button(UP_PIN)

        # 按 ENTER 确认当前位 / 提交密码
        press_button(ENTER_PIN)
        if i + 1 == 6:
            press_button(ENTER_PIN)

    # 根据密码长度决定按多少次 ENTER 提交
    if len(password) < 6:
        press_button(ENTER_PIN)

    log_action(f"完成密码输入：{password}")
    press_button(ENTER_PIN)

def generate_and_enter_passwords(start_password, end_password):
    """自动输入指定范围的密码"""
    # 确定密码位数
    start_length = len(str(start_password))
    end_length = len(str(end_password))
    if start_length != end_length:
        raise ValueError("start_password 和 end_password 的长度必须一致！")

    # 转换为整数范围
    start = int(start_password)
    end = int(end_password)

    # 遍历范围并输入密码
    for number in range(start, end + 1):
        password = str(number).zfill(start_length)  # 填充为固定长度的密码
        enter_password(password)

if __name__ == "__main__":
    try:
        # 手动指定输入范围
        start_password = "46770"  # 示例：4位密码从 0000 开始
        end_password = "99999"    # 示例：到 9999 结束

        # 调用函数输入指定范围的密码
        generate_and_enter_passwords(start_password, end_password)

    except KeyboardInterrupt:
        print("中断程序...")
        GPIO.output(23, GPIO.HIGH)  # 恢复状态
        GPIO.output(24, GPIO.HIGH)  # 恢复状态

