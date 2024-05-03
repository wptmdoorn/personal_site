from nicegui import ui


def content() -> None:
    with ui.card().style('min-height: 500px;').classes('col-xs-12 col-sm-12 col-md-3 col-lg-3 w-full'):
        ui.label('Titel')
        ui.separator()
        ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...').style(
            'min-height: 120px')

        with ui.grid(columns=2):
            ui.button('Source', icon='home').props(
                'rounded glossy color=black')
            ui.button('Demo', icon='directions').props(
                'rounded glossy color=black')

    with ui.card().classes('col-xs-12 col-sm-12 col-md-2 col-lg-2'):
        ui.image('https://picsum.photos/id/684/640/360')
        with ui.card_section():
            ui.label(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')

    with ui.card().tight():
        ui.image('https://picsum.photos/id/684/640/360')
        with ui.card_section():
            ui.label(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')

    with ui.card().tight():
        ui.image('https://picsum.photos/id/684/640/360')
        with ui.card_section():
            ui.label(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
