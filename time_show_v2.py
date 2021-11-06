import tkinter

"""
tk 可拖动窗口Demo
双击关闭程序
"""


class DragWindow:
    def __init__(self):
        self.root = tkinter.Tk()

        self.x, self.y = 0, 0
        self.window_size = '300x200'

        # 设置隐藏窗口标题栏和任务栏图标
        self.root.overrideredirect(True)
        # 窗口透明度60%
        self.root.attributes("-alpha", 0.4)
        # 设置窗口大小、位置 长x宽+x+y
        self.root.geometry(f"{self.window_size}+10+10")
        # 设定背景颜色
        self.root.configure(bg="blue")

        # 窗口移动事件
        self.root.bind("<B1-Motion>", self.move)
        # 单击事件
        self.root.bind("<Button-1>", self.get_point)
        # 双击事件
        self.root.bind("<Double-Button-1>", self.close)

    def move(self, event):
        """窗口移动事件"""
        new_x = (event.x - self.x) + self.root.winfo_x()
        new_y = (event.y - self.y) + self.root.winfo_y()
        s = f"{self.window_size}+{new_x}+{new_y}"
        self.root.geometry(s)

    def get_point(self, event):
        """获取当前窗口位置并保存"""
        self.x, self.y = event.x, event.y

    def run(self):
        self.root.mainloop()

    def close(self, event):
        self.root.destroy()


if __name__ == "__main__":
    window = DragWindow()
    window.run()

