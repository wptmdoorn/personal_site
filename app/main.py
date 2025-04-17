import uvicorn
from base64 import b64encode
import theme
import os
import importlib
import json
from utils.startup import register_dash_apps
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jinja2
from nicegui import app, ui
from utils.obtain_research import get_publication_list
from utils.blog import get_blog_metadata
from jinja_markdown2 import MarkdownExtension

app.add_static_files('static', 'app/static')
fapp = FastAPI()

# Load env and run app
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Static site - FastAPI
templates = Jinja2Templates(directory="app/templates")
jinja_env = jinja2.Environment(
    loader=jinja2.loaders.FileSystemLoader("app/templates"))
jinja_env.add_extension(MarkdownExtension)
# jinja_env.get_template
fapp.mount("/static", StaticFiles(directory="app/static"), name="static")

objects = {
    "home": {
        "software_example": json.loads(open('app/data/software.json').read())[0:2],
        "blog_example": get_blog_metadata()[0:2],
        "research_example": get_publication_list()[0:2],
    },
    "blog": {
        "blog_list": get_blog_metadata()
    },
    "research": {
        "publications": get_publication_list()
    },
    "software": {
        "software_list": json.loads(open('app/data/software.json').read())
    }
}


@app.get("/")
async def return_home(request: Request):
    print('hello')
    return templates.TemplateResponse(
        request=request, name="home.html",
        context=objects["home"],
    )


@app.get("/{page}", response_class=HTMLResponse)
async def return_static(request: Request, page: str):
    print(f'called!! p: {page}')
    print(page)
    page = page.lower()
    page = page if page != "" else "home"
    if page in ["home", "blog", "software", "research"]:
        return templates.TemplateResponse(
            request=request, name=f"{page}.html",
            context=objects[page],
        )

# Dynamic site - NiceGUI

# Register DASH apps
register_dash_apps()

# Register blogs
for blog in os.listdir('app/blogs'):
    app.add_static_files(f'/{blog}', f'app/blogs/{blog}')


@app.get('/blog/{page}', response_class=HTMLResponse)
def blog_page(request: Request, page: str):
    if os.path.exists(f'app/blogs/{page}'):
        with open(f'app/blogs/{page}/blog.md', encoding='utf-8') as f:
            data = f.read().split('---')
            metadata, content = json.loads(data[1]), "".join(data[2:])

            print(content)

            return jinja_env.get_template("blog_individual.html").render(
                {"metadata": metadata, "content": content},
            )


@ui.page('/software/{page}')
def software_page(page: str) -> None:
    if os.path.exists(f'app/software/{page}'):
        page_module = importlib.import_module(f'software.{page}.main')

        if page_module.SOFTWARE_TYPE == 'DASH':
            ui.open(f'/software/dash/{page}')

        elif page_module.SOFTWARE_TYPE == 'NICEGUI':
            with theme.frame(page):
                page_module.content()


ui.run_with(app=fapp,
            title='William van Doorn',
            favicon=f'''data: image/png;base64,{b64encode(
           open('app/static/home_profile.png', 'rb').read()).decode('utf-8')}''',
            storage_secret=os.getenv('STORAGE_SECRET') or 'storage_secret')

if __name__ == "__main__":
    uvicorn.run("main:fapp", host="0.0.0.0", port=8080,
                lifespan='on', use_colors=True, reload=True,)
