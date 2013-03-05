#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 工作流程
# 软件的显示语言为中文。文档可以为中文或者英文。
# TODO: 写处理选项的程序，Python有专门的处理选项的库，
# 可以参考其官方文档
# 处理选项
# -c 配置文件名称
# -u 用户数据库名称
# -m 压力测试模型
# -l 输出日志文件名称，无此选项表示输出到屏幕
# -h 显示帮助
# NOTE: 需要检测配置文件是否存在，不存在则提示错误并退出


# 需要统计的信息
# 成功发送的邮件数量
success_delivery=0
# 失败发送的邮件数量
failed_delivery=0
# 发送邮件的总容量
delivery_size=0
# 失败SMTP登录的数量
failed_smtp_login=0
# 其他的服务器异常
smtp_expeption=0
# 成功下载的邮件数量
success_retrieval=0
# 下载邮件的总容量
retrieval_size=0
# 失败IMAP登录的数量
failed_imap_login=0


# 分成3个进程/线程
# 进程1：启动SMTP压力测试
# 进程2：启动IMAP压力测试
# 进程3：每隔一段时间统计一次信息，并存储到日志文件中
# 等待进程结束
# flush到日志文件
# 程序结束
