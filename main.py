import mechanize
import header

br = mechanize.Browser()

header.InitBrowser(br)

config = header.ConfigUser('config.txt')

header.LogIn(br, 'https://raven.cam.ac.uk/auth/login.html', 'credentials', 'userid', 'pwd', config[0], config[1])

header.MealBooking(br, 'https://www.mealbookings.cai.cam.ac.uk', config[2], config[3], 'edit', 'update', 'addwait')

header.LogOut(br)
