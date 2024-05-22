from nicegui import ui
import json


def content() -> None:
    software_list = json.loads(open('app/data/software.json').read())

    # s = software_list[0]

    with ui.element('div').classes('row w-full justify-center'):
        for s in software_list:
            with ui.card().classes('col-xs-12 col-sm-5 col-md-5 col-lg-5 q-ma-sm'):
                ui.label(s['name']).style('font-weight: bold')
                ui.separator()
                ui.label(s['description']).style(
                    'min-height: 120px')

                with ui.grid(columns=2).classes('row w-full justify-center items-center'):
                    if s['source'] != -1:
                        ui.button('Source', icon='home').props(
                            'rounded glossy color=grey').on_click(lambda: ui.open(s['source']))
                    if s['demo'] != -1:
                        ui.button('Demo', icon='directions').props(
                            'rounded glossy color=grey').on_click(lambda: ui.open(s['demo']))
