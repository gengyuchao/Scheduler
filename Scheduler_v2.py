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

# 创建字典，包括任务名称，任务执行时间，任务执行函数，任务ID，任务执行状态

SysTaskList = []

SysTask_demo = {
    "name": "test",
    "time": "0",
    "interval": "15",
    "is_repeat": False,
    "func": "print('Hello')",
    "id": 0,
    "status": "idle"
}
    
# 将上述字典对写入文件
# def write_task_to_file(task):
#     # 创建文件
#     f = open("task.txt", "a")
#     # 写入文件
#     f.write(str(task)+"\n")
#     # 关闭文件
#     f.close()

# 将文件中的任务读取出来

# 从文件中读取字典的值
# def read_task_from_file():
#     task_list = []
#     # 创建文件
#     f = open("task.txt", "r")
#     # 遍历文件
#     for line in f:
#         task_list.append(eval(line))
#     # 关闭文件
#     f.close()

#     return task_list

# write_task_to_file(SysTask_demo)
# # print(SysTask_demo)
# task_list = read_task_from_file()
# print(task_list)

# 任务管理工具

# 拷贝任务
def copy_task(task):
    task_copy = {}
    task_copy['name'] = task['name']
    task_copy['time'] = task['time']
    task_copy['interval'] = task['interval']
    task_copy['is_repeat'] = task['is_repeat']
    task_copy['func'] = task['func']
    task_copy['id'] = assign_tasks_id()
    task_copy['status'] = task['status']
    return task_copy

# 设置任务执行时间
def set_time(task):
    task['time'] = input("请输入任务执行时间：")
    return task

# 设置任务执行间隔
def set_interval(task):
    task['interval'] = input("请输入任务执行间隔：")
    return task

# 设置任务执行函数
def set_func(task):
    task['func'] = input("请输入任务执行函数：")
    return task

# 初始化任务
def init_task(task):
    task['name'] = input("请输入任务名称：")
    task['id'] = assign_tasks_id()
    task['status'] = "stop"
    return task

# 更新重复任务的时间
def update_repeat_task_time(task):
    # 设置时间格式 

    task['time'] = (datetime.datetime.now() + datetime.timedelta(seconds=int(task['interval']))).strftime("%Y-%m-%d %H:%M:%S")
    return task

# 创建一个新的任务
def create_task():
    task = {}
    task = init_task(task)
    task = set_time(task)
    task = set_interval(task)
    task = set_func(task)
    # write_task_to_file(task)
    return task



# 比较当前时间是否比任务时间晚
def is_expired(task):
    # 获取当前时间
    now = datetime.datetime.now()
    # 获取任务时间，如果任务时间格式是"%H:%M:%S"，则默认年月日为当前时间
    if task['time'].find("-") != -1:
        task_time = datetime.datetime.strptime(task['time'], "%Y-%m-%d %H:%M:%S")
    elif task['time'].find(":") != -1:
        # 默认年月日为当前时间
        task_time = datetime.datetime.strptime(str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+task['time'], "%Y-%m-%d %H:%M:%S")
    else:
        task_time = now
  


    # task_time = datetime.datetime.strptime(task['time'], "%H:%M:%S")
    # 打印两个时间
    # print(now)
    # print(task_time)
    # 比较当前时间是否比任务时间晚
    if now >= task_time:
        return True
    else:
        return False


# 遍历任务列表,执行输入的函数

# def list_task(func):
#     for task in SysTaskList:
#         func(task)


# SysTaskList.append(set_time(copy_task(SysTask_demo)))
# SysTaskList.append(set_time(copy_task(SysTask_demo)))
# SysTaskList.append(set_time(copy_task(SysTask_demo)))

# 将任务列表写入文件
def write_task_list_to_file():
    # 创建文件
    f = open("task.txt", "w")
    # 写入文件
    for task in SysTaskList:
        f.write(str(task)+"\n")
    # 关闭文件
    f.close()

# 从文件读出任务列表
def read_task_list_from_file():
    # 创建文件
    f = open("task.txt", "r")
    # 遍历文件
    for line in f:
        SysTaskList.append(eval(line))
    # 关闭文件
    f.close()

# 在窗口右下角显示当前时间
def show_time():
    # 获取当前时间
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 计算文字长度
    length = len(str(now))+1

    # 记录当前光标位置
    print("\033[s\033[1;200H", end="")
    # 写入 length 个 \b
    for i in range(length):
        print("\b", end="")

    print(str(now),end="")
    # 回到原来的位置
    print("\033[u", end="")
    # 向stdout输出
    sys.stdout.flush()

# 在窗口右下角显示当前时间
def show_next_task_info(task):
    # 获取当前时间
    info_str = ("next task:"+task['name']+" "+task['time'])
    # 计算文字长度
    length = len(str(info_str))+1

    # 记录当前光标位置
    print("\033[s\033[1;100H", end="")
    # 写入 length 个 \b
    for i in range(length):
        print("\b", end="")

    print(info_str,end="")
    
    # 回到原来的位置
    print("\033[u", end="")
    # 向stdout输出
    sys.stdout.flush()

# 格式化时间
def format_time(time_str):
    if time_str.find("-") != -1:
        time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    elif time_str.find(":") != -1:
        now = datetime.datetime.now()
        # 默认年月日为当前时间
        time = datetime.datetime.strptime(str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+time_str, "%Y-%m-%d %H:%M:%S")
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    return time_str

# 按照时间对任务列表排序
def sort_task_list(task_list):
    # 遍历任务列表，格式化时间
    for task in task_list:
        task['time'] = format_time(task['time'])
    # 按照时间对任务列表排序
    task_list.sort(key=lambda x: x['time'])
    
    # 打印排序结果的名字和时间
    # for task in task_list:
    #     print(task['name']+" "+task['time'])
    # print("\n")
    return task_list



# 循环执行任务
def run_task():
    while True:
        global SysTaskList
        SysTaskList = sort_task_list(SysTaskList)
        task = None
        for task in SysTaskList:
            if task['status'] == "stop":
                continue
            if is_expired(task):
                print("执行任务："+task['name'])
                exec(task['func'])
                if task['is_repeat'] == False:
                    task['status'] = "stop"
                else:
                    task['status'] = "run"
                    task = update_repeat_task_time(task)
                    break
            else:
                # print("下一个任务时间："+task['name']+" "+task['time'])
                break
        # 如果task 不为空
        if task != None:
            show_next_task_info(task)
        # show_next_task_info(task)
        show_time()
        time.sleep(1)

# list_task()
# write_task_list_to_file()
print("任务列表：")
read_task_list_from_file()
run_task()