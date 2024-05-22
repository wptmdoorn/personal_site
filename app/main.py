import theme
import os
import importlib
import json

from nicegui import app, ui
from utils.researchgate import get_profile

app.add_static_files('static', 'app/static')

for blog in os.listdir('app/blogs'):
    print(blog)
    app.add_static_files(f'/{blog}', f'app/blogs/{blog}')


@ui.page('/')
def index_page() -> None:
    with theme.frame('home'):
        from pages import home
        home.content()


@ui.page('/{page}')
def page(page: str) -> None:
    if os.path.exists(f'app/pages/{page}.py'):
        page_module = importlib.import_module(f'pages.{page}')

        with theme.frame(page):
            page_module.content()


@ui.page('/blog/{page}')
def blog_page(page: str) -> None:
    print('hello')
    print(page)

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


get_profile('William-Doorn')
ui.run(title='William van Doorn')
