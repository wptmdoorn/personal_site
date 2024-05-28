from base64 import b64encode
import theme
import os
import importlib
import json
from utils.startup import register_dash_apps
from dotenv import load_dotenv

from nicegui import app, ui

app.add_static_files('static', 'app/static')


# Home Page

@ui.page('/')
def index_page() -> None:
    with theme.frame('home'):
        from pages import home
        home.content()

# Sub Pages


@ui.page('/{page}')
def page(page: str) -> None:
    if os.path.exists(f'app/pages/{page}.py'):
        page_module = importlib.import_module(f'pages.{page}')

        with theme.frame(page):
            page_module.content()

# Blogs


@ui.page('/blog/{page}')
def blog_page(page: str) -> None:

    if os.path.exists(f'app/blogs/{page}'):
        with open(f'app/blogs/{page}/blog.md', encoding='utf-8') as f:
            data = f.read().split('---')
            metadata, content = json.loads(data[1]), "".join(data[2:])

            with theme.frame(f'Blog - {metadata["short_title"]}'):
                ui.label(f'This blog was first published on {metadata["pub_date"]} ' +
                         f'and last updated on {metadata["last_mod"]}').style('font-size: 12px; font-style: italic; font-color: grey')
                ui.markdown(content).classes('w-full')
    else:
        with theme.frame('Blog'):
            ui.markdown('# Blog post not found')

# Software Pages


@ui.page('/software/{page}')
def software_page(page: str) -> None:
    if os.path.exists(f'app/software/{page}'):
        page_module = importlib.import_module(f'software.{page}.main')

        if page_module.SOFTWARE_TYPE == 'DASH':
            ui.open(f'/software/dash/{page}')

        elif page_module.SOFTWARE_TYPE == 'NICEGUI':
            with theme.frame(page):
                page_module.content()

# Register DASH apps and blogs


register_dash_apps()
for blog in os.listdir('app/blogs'):
    app.add_static_files(f'/{blog}', f'app/blogs/{blog}')

# Load env and run app
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

print(
    f'Running app with storage secret: {os.getenv("STORAGE_SECRET")[:5]}...'
)

ui.run(title='William van Doorn',
       favicon=f'''data: image/png;base64,{b64encode(
           open('app/static/home_profile.png', 'rb').read()).decode('utf-8')}''',
       storage_secret=os.getenv('STORAGE_SECRET'))
