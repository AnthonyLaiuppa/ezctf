from __future__ import absolute_import, print_function, unicode_literals
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class EzCtfValidation(unittest.TestCase):
	""" 
	    Very basic demo of post deploy
	    QA testing using Selenium and
	    Unittest.

	    We could add more but just checking
	    that everything is present is sufficient
	    for now.
	"""

	def setUp(self, driver=None):
		self.driver = webdriver.Chrome()

	def test_home(self):
		driver = self.driver
		driver.get("http://ezctf.com")
		assert "Register, Login, Hack the Planet!" in driver.page_source
		sleep(1)

	def test_home_authd(self):
		driver = self.driver		
		driver.get("http://ezctf.com/login")
		login = driver.find_element_by_name("username")
		login.send_keys("test_user")
		login = driver.find_element_by_name("password")
		login.send_keys("password")
		login = driver.find_element_by_name("login").click()
		driver.get("http://ezctf.com")
		assert "Hack the Planet!" in driver.page_source
		sleep(1)

	def test_login(self):
		driver = self.driver
		driver.get("http://ezctf.com/login")
		login = driver.find_element_by_name("username")
		login.send_keys("test_user")
		login = driver.find_element_by_name("password")
		login.send_keys("password")
		login = driver.find_element_by_name("login").click()
		assert "You are now logged in" in driver.page_source
		sleep(1)

	def test_logout(self):
		driver = self.driver
		driver.get("http://ezctf.com/login")
		login = driver.find_element_by_name("username")
		login.send_keys("test_user")
		login = driver.find_element_by_name("password")
		login.send_keys("password")
		login = driver.find_element_by_name("login").click()
		driver.get("http://ezctf.com/logout")
		assert "You are now logged out" in driver.page_source
		sleep(1)

	def test_about(self):
		driver = self.driver
		driver.get("http://ezctf.com/about")
		assert "About ezCTF" in driver.page_source
		sleep(1)

	# Ideally we have it register a user but lets just see if it loads
	def test_register(self):
		driver = self.driver
		driver.get("http://ezctf.com/register")
		assert "Register" in driver.page_source
		sleep(1)

	def test_challenges_page(self):
		driver = self.driver
		driver.get("http://ezctf.com/challenges")
		assert "web1" in driver.page_source
		sleep(1)

	def test_challenge_unauthd(self):
		driver = self.driver
		driver.get("http://ezctf.com/challenge/1/")
		assert "Submit Flag" not in driver.page_source
		sleep(1)

	def test_challenge_authd(self):
		driver = self.driver
		driver.get("http://ezctf.com/login")
		login = driver.find_element_by_name("username")
		login.send_keys("test_user")
		login = driver.find_element_by_name("password")
		login.send_keys("password")
		login = driver.find_element_by_name("login").click()
		driver.get("http://ezctf.com/challenge/1/")
		assert "Submit Flag" in driver.page_source
		sleep(1)

	def test_403(self):
		driver = self.driver
		driver.get("http://ezctf.com/add_challenge")
		assert "Unauthorized" in driver.page_source
		sleep(1)

	def test_404(self):
		driver = self.driver
		driver.get("http://ezctf.com/logi")
		assert "Page Not Found" in driver.page_source
		sleep(1)

	def tearDown(self):
		self.driver.close()

if __name__ == '__main__':
	unittest.main()
