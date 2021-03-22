from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import sqlite3

def create():
    """Tạo file db thêm dữ liệu lấy từ https://github.com/awesome-jobs/vietnam/issues cho vào bảng jobs"""
    conn = sqlite3.connect("jobspython.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE jobs(number int, name text, url text)""")
    conn.commit()
    for i in range(1, 11):
        r = requests.get(
            "https://api.github.com/repos/awesome-jobs/vietnam/issues?page={}".format(i)
        )
        data = json.loads(r.text)
        if data == []:
            break
        for job in data:
            conn = sqlite3.connect("jobspython.db")
            c = conn.cursor()
            a = """INSERT INTO jobs VALUES ({}, '{}', '{}');""".format(
                job["number"], job["title"], job["html_url"]
            )
            c.execute(a)
            conn.commit()
        data = []

def web(request):
    result = []
    create()
    conn = sqlite3.connect("jobspython.db")
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    ans = c.fetchall()
    for id, title, link in ans:
        job = "{}: {}\n".format(id, title)
        result.append([job, link])
    c.execute("DROP TABLE jobs")
    return render(request, 'index.html', context={'content': result})

# Create your views here.
