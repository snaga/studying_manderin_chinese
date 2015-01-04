import os

os.system("env > env.txt")
os.system("python --version > python.txt")
os.system("ls -l /home/vcap/app/.heroku/python/bin /bin /usr/bin > ls.txt")

PORT = int(os.getenv('VCAP_APP_PORT', '8000'))

print("serving at port", PORT)

cmd = "python manage.py runserver 0.0.0.0:" + str(PORT)

os.system("echo " + cmd + " > cmd.txt")
os.system(cmd)

