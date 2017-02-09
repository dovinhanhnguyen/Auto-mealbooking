import mechanize
import cookielib
import datetime

def InitBrowser( browser ):
	"""Set cookie jar and robot.txt handling
	InitBrowser( browser )
	"""

	cookie_jar = cookielib.LWPCookieJar()
	browser.set_cookiejar(cookie_jar)

	browser.set_handle_robots(False)

	return

def ConfigUser( config_file ):
	"""Simple password storage"""

	f = open(config_file, 'r')

	return f.read().splitlines()

def LogIn( browser, raven_url, login_form_name, id_control, pwd_control, username, password ):
	"""Log in via Raven
	LogIn( browser, booking_url, login_form_name, id_control, pwd_control, username, password )
	"""

	browser.open(raven_url)
	browser.select_form(name=login_form_name)
	browser.form.set_value(username, name=id_control)
	browser.form.set_value(password, name=pwd_control)
	browser.submit()

	return

def WhichMeal():
	"""Need this because hall depends on weekday"""

	today_date = datetime.date.today()
	
	if (today_date.weekday() == 1) or (today_date.weekday() == 3) or (today_date.weekday() == 6):
		return 'First Hall'
	elif today_date.weelday() == 5:
		return 'Cafeteria Hall'
	
	else:
		return 'Abort'

def MealBooking( browser, booking_url, edit_control, update_control, subscribe_control ):
	"""Book today first hall
	MealBooking( browser, booking_url, edit_control, update_control, subscribe_control )
	"""

	browser.open(booking_url)
	request = browser.click_link(text='Bookings')
	browser.open(request)
	if WhichMeal() == 'Abort':
		return
	else:
		request = browser.click_link(text=WhichMeal())
		browser.open(request)

	today_date = datetime.date.today()
	request = browser.click_link(text=today_date.strftime('%A %-d %B %Y'))
	browser.open(request)
	
	deadline_passed = False
	"select browser.form"
	for form in browser.forms():
		for control in form.controls:
			if control.name == subscribe_control:
				deadline_passed = True
				browser.form = form
				break
			if control.name == edit_control:
				browser.form = form
				break
	
	if deadline_passed == False:
		browser.form.find_control(edit_control).selected = True
		browser.submit()
		"new HTML page now so need to select browser.form again"
		for form in browser.forms():
			for control in form.controls:
				if control.name == update_control:
					browser.form = form
					break
		browser.form.find_control(update_control).selected = True
		browser.submit()
	else:
		browser.form.find_control(subscribe_control).selected = True
		browser.submit()
		"new HTML page now so need to select browser.form again"
		for form in browser.forms():
			for control in form.controls:
				if control.name == subscribe_control:
					browser.form = form
					break
		browser.form.find_control(subscribe_control).selected = True
		browser.submit()

	return

def LogOut( browser ):
	request = browser.click_link(text='Logout')
	browser.open(request)
	request = browser.click_link(text='logout from the central authentication service')
	browser.open(request)

	return
