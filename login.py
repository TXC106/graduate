from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def spider_deal(usr, pwd):
	url = 'http://202.115.133.173:805/Login.html'

	options = Options()    # 初始设置参数变量
	options.add_argument('--headless')	 # 不输出图形
	options.add_argument('--no-sandbox')
	# options.binary_location = r'E:\\tmp\\bin\\chrome.exe'
	# driver = webdriver.Chrome(options=options,executable_path="/usr/local/share/chromedriver.exe")
	# driver = webdriver.Chrome("E:\\tmp\\Application\\chrome.exe")
	driver = webdriver.Chrome(options=options)
	# driver = webdriver.Chrome()
	try:
		driver.get(url)

	# 输入账户密码
		driver.find_element_by_id('txtUser').send_keys(usr)
		driver.find_element_by_id('txtPWD').send_keys(pwd)
		# 登录
		driver.find_element_by_class_name('btn_login').click()
		# 加载
		time.sleep(0.5)
	except:
		print("登陆失败")
		driver.quit()
		# status = {
		# 	'status': -1,
		# 	'description': '账户密码不正确或响应超时'}
		# return status
	# try:
	# 	driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[3]/div[2]/div[2]/ul/li[1]/a').click()
	# except:
	# 	print("账户密码不正确或响应超时 ", time.ctime())
	# 	driver.quit()
	# 	return 0
	# driver.switch_to_window(driver.window_handles[1])
	# # 获取url
	# get_url = driver.current_url
	# driver.get(get_url)
	# res = driver.page_source
	return driver

	# driver.switch_to_window(driver.window_handles[0])
	# driver.quit()
	#
	#
	# return res
	# # return get_url


def main():
	usr = '201712090414'
	pwd = '420502199704251123'
	print(spider_deal(usr, pwd))
	# print("爬取到的链接地址为： " + spider_deal(usr, pwd) + time.ctime())

	# while True:
	# 	usr = input("请输入账户账号：")
	# 	pwd = input("请输入账户密码：")
	# 	print("正在爬取，请稍等......")
	#
	# 	if spider_deal(usr,pwd) == 0:
	# 		if input("------------>是否重试 (输入0退出)：") == '0':
	# 			break
	# 	else:
	# 		print("爬取到的链接地址为： " + spider_deal(usr,pwd) + time.ctime())
	# 		if input("------------>是否继续爬取 (输入0退出)：") == '0':
	# 			break


if __name__ == '__main__':
	main()
