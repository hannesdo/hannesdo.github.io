import os, sys, json, re
import pathlib
from jinja2 import Environment, BaseLoader
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

now_Pacific = datetime.now(ZoneInfo('US/Pacific'))

print("STATUS : Script started")

## Check for current cwd
print(os.getcwd())

## Change cwd to path of .py file
p = os.path.abspath(__file__)
dname = os.path.dirname(p)
os.chdir(dname)
print(os.getcwd())

## Load database from JSON file

with open(Path.cwd() / 'db.json', encoding="utf-8") as f:
    database = json.load(f)

## Load template from file

with open(Path.cwd() / "templates" / "index.html", encoding="utf-8") as f:
    template_full = f.read()
header = template_full.split("<main>")[0]
footer = template_full.split("</main>")[1]

with open(Path.cwd() / "public" / "index.html", encoding = "utf-8", mode = "w") as f:
    f.write(template_full)

## Generate pages

page_input = {
    "research" : {
        "publications" : database["publishedPapers"],
        "working_projects" : database["workingPapers"],
    },
    #"code_and_data" : {
    #    "projects" : database["projects"],
    #},
    #"talks_and_classes" : {
    #    "talks" : database["talks"],
    #    "classes" : database["teaching"], 
    #},
    "blog_posts" : {
        "articles" : database["articles"],
    }
}

for label, data in page_input.items():
    with open(Path.cwd() / 'templates' / f'{label}.html', encoding="utf-8") as f:
        template_html = f.read()

    template_html = header + template_html + footer

    template = Environment(loader=BaseLoader()).from_string(template_html)

    render = template.render(data)

    with open(Path.cwd() / "public" / f"{label}.html", encoding = "utf-8", mode = "w") as f:
        f.write(render)

print("STATUS : Pages generated")

## Generate resume

with open(Path.cwd() / 'templates' / 'resume.html', encoding="utf-8") as f:
    template_html = f.read()

template = Environment(loader=BaseLoader()).from_string(template_html)

render = template.render({
    "resume" : database,
    "date" : now_Pacific.date().strftime("%B %d, %Y")
    })

with open(Path.cwd() / "public" / 'resume.html', encoding = "utf-8", mode = "w") as f:
    f.write(render)

print("STATUS : Resume generated")

print("STATUS : Script finished!")