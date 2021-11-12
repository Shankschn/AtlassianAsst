import logging
import os
import time

# 第一步，创建一个logger
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)  # Log等级总开关
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d', time.localtime(time.time()))
# 当前脚本所在路径
log_path = os.path.dirname(os.path.realpath(__file__)) + '/logs/'

if not os.path.exists(log_path):
    os.makedirs(log_path)

log_file = log_path + rq + '.log'
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志


def d(msg):
    print(msg)
    logger.debug(msg)


def i(msg):
    print(msg)
    logger.info(msg)


def w(msg):
    print(msg)
    logger.warning(msg)


def e(msg):
    print(msg)
    logger.error(msg)


def c(msg):
    print(msg)
    logger.critical(msg)
