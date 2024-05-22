from contextlib import contextmanager
from nicegui import ui

# styling
_header_row_classes = 'row w-full justify-center items-center'
_header_card_classes = '''
    q-ma-sm col-xs-12 col-sm-2 col-md-2 col-lg-2 no-shadow border-[1px]
    hover:bg-green-500 hover:scale-105 transform duration-500
'''
_header_card_style = 'border-radius: 20px;'
_header_card_img_style = 'height: 20px; min-height: 20px; min-width: 20px; width: 20px'

_body_class = 'row w-full justify-center'
_body_row_classes = 'w-full q-ma-sm justify-center'

_head_column_class = 'col-xs-12 col-sm-8 col-md-8 justify-center w-full'

_footer_classes = 'w-full justify-center'
_footer_img_style = 'height: 20px; min-height: 20px; min-width: 20px; width: 20px'

# information
_headers = ['Home', 'Blog', 'Research', 'Software']

# urls
_github_url = 'https://github.com/wptmdoorn'
_linkedin_url = 'https://www.linkedin.com/in/william-van-doorn/'


@contextmanager
def frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    # ui.colors(primary='#6E93D6', secondary='#53B689',
    #          accent='#111B1E', positive='#53B689')
    # with ui.column().classes('absolute-center items-center h-screen no-wrap p-9 w-full'):
    #   yield

    ui.page_title(f'{navtitle.capitalize()} | William van Doorn')

    with ui.element('div').classes(_body_class).style('font-family: sans-serif;'):
        with ui.element('div').classes(_head_column_class):
            with ui.element('div').classes(_header_row_classes):
                for title in _headers:
                    with ui.card().classes(_header_card_classes).style(_header_card_style).on('click',
                                                                                              lambda title=title: ui.open(f'/{title.lower()}')):
                        with ui.row():
                            ui.image(
                                f'app/static/{title.lower()}.png').style(_header_card_img_style)
                            ui.label(title)

            with ui.row().classes(_body_row_classes):
                yield

    with ui.row().classes(_footer_classes):
        ui.image('app/static/github.png').style(_footer_img_style).on('click',
                                                                      lambda: ui.open(_github_url))
        ui.link('Github', _github_url)
        ui.image('app/static/linkedin.png').style(_footer_img_style).on('click',
                                                                        lambda: ui.open(_linkedin_url))
        ui.link('LinkedIn', _linkedin_url)
