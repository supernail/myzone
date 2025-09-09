#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教师工作量计算器（修正版）
规则：
1. 课程负责人工作量 = 每门课程固定学时 * 课程数量 + 分段函数(教师团队人数)
2. 课程导师工作量   = 0.718458244 × 学生人数
3. 教师总工作量     = 负责人 + 导师
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- 核心算法 ----------
def director_hours(courses: int, tutors: int) -> float:
    """课程负责人工作量"""
    base_hours = courses * 5  # 每门课程固定5学时
    if tutors <= 5:
        return base_hours + tutors * 1.0
    elif tutors <= 15:
        return base_hours + 10 + (tutors - 5) * 0.7
    elif tutors <= 30:
        return base_hours + 17 + (tutors - 15) * 0.5
    else:
        return base_hours + 24.5 + (tutors - 30) * 0.3

def tutor_hours(students: int) -> float:
    """课程导师工作量"""
    return max(0, students) * 0.718458244

def total_workload(courses: int, tutors: int, students: int) -> float:
    """教师总工作量"""
    return director_hours(courses, tutors) + tutor_hours(students)

# ---------- GUI 入口 ----------
def gui_main():
    def calc(event=None):
        try:
            courses = int(courses_var.get()) if courses_var.get() else 0
            t = int(tutor_var.get()) if tutor_var.get() else 0
            s = int(stu_var.get()) if stu_var.get() else 0
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")
            return

        d = director_hours(courses, t)
        tu = tutor_hours(s)
        tot = total_workload(courses, t, s)

        res.set(f"负责人：{d:.2f} 学时\n导师：{tu:.2f} 学时\n总工作量：{tot:.2f} 学时")

    root = tk.Tk()
    root.title("教师工作量计算器")
    root.resizable(False, False)

    courses_var, tutor_var, stu_var, res = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

    ttk.Label(root, text="课程数量：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    ttk.Entry(root, textvariable=courses_var).grid(row=0, column=1, padx=10)

    ttk.Label(root, text="课程导师人数：").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ttk.Entry(root, textvariable=tutor_var).grid(row=1, column=1, padx=10)

    ttk.Label(root, text="选课学生人数：").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    ttk.Entry(root, textvariable=stu_var).grid(row=2, column=1, padx=10)

    ttk.Button(root, text="计算", command=calc).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Label(root, textvariable=res, foreground="red", justify="left").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.bind('<Return>', calc)  # 绑定 Enter 键

    root.mainloop()

# ---------- 双入口 ----------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        gui_main()