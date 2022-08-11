# 使用场景
"""
想获取实验室的一台华为Atlas 200的IP，其接到一台千兆的交换机中，此时我接网线到这台交换机上，然后获取了网络前缀xxx.xxx.xxx.
之后循环判断哪些能ping通，然后再判断ssh能否登录即可
"""
import threading
import subprocess
import paramiko

class MyThread(threading.Thread):
    def __init__(self, threadID, judge_url, user_name, port, passwd) -> None:
        super(MyThread, self).__init__()
        self.threadID = threadID
        self.judge_url = judge_url
        self.user_name = user_name
        self.port = port
        self.passwd = passwd
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    def run(self) -> None:
        start_index = self.threadID * 5
        for i in range(start_index, start_index+5):
            url = self.judge_url + str(i)
            p = subprocess.Popen("ping -n 1 {0} \n".format(url), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            if p.returncode==0:
                print(url+"\t通")
                try:
                    self.ssh_client.connect(hostname=url, port=self.port, username=self.user_name, password=self.passwd, timeout=5, look_for_keys=False, allow_agent=False)
                    print("this it!\t" + url)
                except Exception as e:
                    continue
            else:
                print(url+"\t不通")
        self.ssh_client.close()

judge_url = "xxx.xxx.xxx."
user_name = "xxx"
passwd = "xxx"
port = 22

thread_list = []
for i in range(50):
    thread_list.append(MyThread(i, judge_url, user_name, port, passwd))
for i in range(50):
    thread_list[i].start()
