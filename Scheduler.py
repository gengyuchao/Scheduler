# -*- coding: UTF-8 -*- 

# 添加系统时间库
import time

# 添加日期库
import datetime

# 添加计算时间库
import calendar

import sys
import os

system_task_id=0

# 分配递增的任务ID
def assign_tasks_id():
    global system_task_id #声明我们在函数内部使用的是在函数外部定义的全局变量system_task_id
    id = system_task_id
    system_task_id += 1
    return id

# 创建一个任务类，包括任务名称，任务执行时间，任务执行函数，任务ID，任务执行状态
class Task:
    id=-1
    status="未执行"
    # 重复间隔
    repeat_interval_s = None

    # # 初始化任务
    # def __init__(self, name, time, func):
    #     self.name = name
    #     self.time = time
    #     self.func = func
    # 创建一个任务
    def create_task(self, name, time, func):
        self.name = name
        self.func = func
        self.update_time(time)
        self.id = assign_tasks_id()
        self.status = "未执行"
        return self
    # 加载任务
    def load_task(self, name, time, func ,id,status):
        self.name = name
        self.time = time
        self.func = func
        self.id = id
        self.status = status
        return self
    # 更新status
    def update_status(self, status):
        self.status = status
        return self
    #更新任务时间
    def update_time(self, input_time=None):
        
        if input_time == None:
            # 当前时间加上输入时间
            # print("input_time " + input_time)
            if self.repeat_interval_s == None :
                self.time = (datetime.datetime.now()).strftime("%H:%M:%S")
                print("Please check interval")
            else:
                self.time = (datetime.datetime.now() + datetime.timedelta(seconds=self.repeat_interval_s)).strftime("%H:%M:%S")
            print("更新任务时间为：" + self.time)

            return self

        # 如果任务执行时间是一个日期，则更新任务执行时间
        if isinstance(input_time, datetime.datetime):
            # print("日期" + self.time)
            # 转换为字符串
            self.time = input_time.strftime("%H:%M:%S")
        # 如果任务执行时间是一个时间戳，则更新任务执行时间
        elif isinstance(input_time, int):
            self.repeat_interval_s = int(input_time)
            # 当前时间加上输入时间
            self.time = (datetime.datetime.now() + datetime.timedelta(seconds=self.repeat_interval_s)).strftime("%H:%M:%S")
        # 如果任务执行时间是一个时间字符串，则更新任务执行时间
        elif isinstance(self.time, str):
            # print("字符串" + self.time)
            # 如果是时间格式，则更新任务执行时间
            if self.time.count(":") == 2:
                self.time = input_time
            else:
                # 如果是时间戳，则更新任务执行时间
                self.repeat_interval_s = int(input_time)
                # 当前时间加上输入时间
                self.time = (datetime.datetime.now() + datetime.timedelta(seconds=self.repeat_interval_s)).strftime("%H:%M:%S")



        return self.time


    




# 创建一个任务列表
tasks = []


# 创建一个文件保存任务信息，追加写入任务信息
def save_task(task):
    # 创建一个文件对象
    f = open("task.txt", "a+")
    # 将任务信息写入文件，分隔符为分号
    f.write(task.name + ";" + task.time + ";" + task.func + ";" + str(task.id) + ";" + task.status + "\n")
    # 关闭文件
    f.close()

# 读取任务信息，返回一个任务列表
def read_task():
    # 创建一个任务列表
    tasks = []
    # 创建一个文件对象
    f = open("task.txt", "r")
    # 读取文件内容
    content = f.read()
    # 关闭文件
    f.close()
    # 将文件内容按行分割
    lines = content.split("\n")
    # 遍历每一行
    for line in lines:
        # 判断是否为空行
        if line != "":
            # 将每一行按分号分割
            line = line.split(";")
            # 将每一行的内容添加到任务列表中
            tasks.append(Task().load_task(line[0], line[1], line[2], int(line[3]), line[4]))
    # 返回任务列表
    return tasks

# 判断时间是否过期
def is_expired(time):
    # 创建一个没有日期的时间对象
    now = datetime.datetime.now().strftime("%H:%M:%S")
    now = datetime.datetime.now().strptime(now, "%H:%M:%S")
    # 将时间字符串转换为时间
    time = datetime.datetime.strptime(time, "%H:%M:%S")
    # 判断时间是否过期
    if now >= time:
        # #打印时间now
        # print(now)
        # #打印时间time
        # print(time)
        # # 打印时间过期
        # print("时间过期")
        return True
    else:
        return False

# 读取文件中的任务信息,对任务列表按时间进行排序，并写入到文件中
def sort_task():
    # 读取任务列表
    tasks = read_task()
    # 对任务列表按时间进行排序
    tasks.sort(key=lambda x: x.time)
    # 清空原文件
    f = open("task.txt", "w")
    f.close()
    # 遍历任务列表
    for task in tasks:
        # 判断任务时间是否已经过期，如果过期则写入history文件中，否则写入task文件中
        if(task.status == "重复"):
            save_task(task)
        elif is_expired(task.time):
            task.status = "执行失败，已过期"
            save_task(task) 
            # save_history(task)
        else:
            save_task(task) 


# 添加任务函数
def add_task():
    while(True):
        # 输入任务名称
        name = input("请输入任务名称：")
        # 如果输入的任务名称为空，则提示重新输入
        if name == "":
            # print("任务名称不能为空，请重新输入！")
            # continue
            print("直接执行程序")

        # 输入任务执行时间
        time = input("请输入任务执行时间，格式为： 时:分:秒：")
        
        
        # 如果时间信息未填写，使用默认时间
        if time == "":
            time = "00:00:00"
        else:
                # 如果输入的任务执行时间格式不正确，则提示重新输入
            if time.count(":") != 2 and time.isdigit() == False:
                print("任务执行时间格式不正确，请重新输入！")
                continue
            if time.isdigit() == True:
                print("任务执行时间格式为数字")
                time = time
        

        # 输入任务执行函数
        func = input("请输入任务执行函数：")
        # 任务不能为空
        if func == "":
            print("任务执行函数不能为空，请重新输入！")
            continue

        # 创建一个任务对象
        task = Task().create_task(name, time, func)

        # 输入任务状态是否为重复
        status = input("请输入任务状态，是否重复[Y/n/'']：")
        # 如果输入的任务状态不正确，则提示重新输入
        if status == "y" or status == "Y" :
            print("设置为重复任务！")
            task.update_status("重复")
        elif status == "n" or status == "N" or status == "":
            print("设置为非重复任务！")
        else:
            print("格式错误")
            continue

        # 添加任务到任务文件中
        save_task(task)
        # 显示添加成功
        print("====添加成功====")

# 从文件中删除任务函数
def delete_task(del_task):
    # 读取任务列表
    tasks = read_task()
    # 清除任务文件中的任务信息
    f = open("task.txt", "w")
    f.close()
    # 遍历任务列表
    for task in tasks:
        # 判断是否是要删除的任务
        if task.id != del_task.id:
            # 将新的任务列表写入文件
            save_task(task)

# 存放已执行任务到history.txt文件中
def save_history(task):
    # 创建一个文件对象
    f = open("history.txt", "a")
    # 将任务信息写入文件，分隔符为分号
    f.write(task.name + ";" + task.time + ";" + task.func + ";" + str(task.id) + ";" + task.status + "\n")
    # 关闭文件
    f.close()



# 创建一个系统任务，每隔1秒执行一次
def scheduler():
    i = 0
    while True:
        time.sleep(1)
        # 读取任务列表
        tasks = read_task()
        # 遍历任务列表
        for task in tasks:
            will_execute = False

            # 判断时间是否是默认时间
            if task.time == "00:00:00":
                # 如果是默认时间，则立即执行任务
                task.status = "正在执行"
                will_execute = True
            else:
                if task.time.count(":") != 2:
                    task.update_time(task.time)
                    print("获取到数字任务信息：" + task.time)
                    
                # 如果不是是时间格式且不是默认时间，则判断是否已经过期
                if is_expired(task.time):
                    if(task.status == "重复"):
                        # 如果任务状态为重复，则修改任务时间再添加到任务列表中
                        task.update_time(task.repeat_interval_s)
                        print("重复任务，修改时间为：" + task.time)
                    else:
                        # 如果任务状态不为重复，则将任务状态修改为正在执行
                        task.status = "正在执行"

                    will_execute = True

            

            # 如果任务状态为正在执行，则开始执行任务
            if will_execute == True:

                print("任务：" + task.func + " 假装执行成功！")
                # task.func()
                exec(task.func)

                 # 将任务信息写入历史文件
                save_history(task)       
                # 打印任务执行信息
                print("任务：" + task.name + task.status + "!")
                if(task.status != "重复"):
                    # 将任务状态改为已执行
                    task.status = "执行成功"
                    # 删除任务
                    delete_task(task)

            # 更新任务信息
            delete_task(task)
            if(task.status == "重复"):
                # 将任务添加到任务列表中
                save_task(task)
         
            # 将任务重新排序并写入文件
            sort_task()


            



        # 每十个循环打印一次
        if i % 1 == 0:
            # 在中断最上面一行显示当前时间
            print("\033[s\033[0;0H \r系统正在运行中... " + time.strftime("%H:%M:%S", time.localtime()) + "\033[u", end="")
            # 将任务重新排序并写入文件
            sort_task()
            # 读取任务列表
            tasks = read_task()
            # 打印任务列表
            print("任务列表：")
            for task in tasks:
                print(task.name + " " + task.time)
        i=i+1


# 检查任务文件是否存在，如果不存在则创建
if not os.path.exists("task.txt"):
    f = open("task.txt", "w")
    f.close()

import  threading
# 创建一个线程，用于定时执行任务
t = threading.Thread(target=scheduler)
# 指定线程的编码格式为utf-8
t.setDaemon(True)
print("线程名称：", t.name)
print("线程ID：", t.ident)
# 启动线程
t.start()

# 创建一个线程，打开一个系统命令行程序，用于添加任务
t1 = threading.Thread(target=add_task)
# 指定线程的编码格式为utf-8
print("线程名称：", t1.name)
print("线程ID：", t1.ident)
# 启动线程
t1.start()

# 等待线程执行完毕
t.join()
t1.join()




# 通过命令行输入任务名称，任务执行时间，任务执行函数
# python3 Scheduler.py task_name 2018-12-12 12:12:12 task_func


