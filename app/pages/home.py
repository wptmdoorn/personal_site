from nicegui import ui


def content() -> None:
    ui.html('<h2> William van Doorn </h2>').style('font-weight:700; font-size:2rem')

    with ui.element('div').classes('row').style('font-size:1.1rem'):
        with ui.element('div').classes('col-xs-12 col-md-8'):
            ui.label(
                '''Hey, I'm William. Currently I am a resident in clinical chemistry at the Maastricht University
                    Medical Center.''').style('margin-bottom: 1rem')
            ui.label('Importantly, I love building (digital) things.').style(
                'margin-bottom: 1rem; font-style: italic; font-weight: bold')

            ui.label('''This is my spot on the web for writing, projects, tutorials,
                        and anything else I want to put out there. Check out the blog, or take a
                        look at the projects page to see my (open-source) work.''').style('margin-bottom: 1rem')

            ui.label('''This site has no ads, no affiliate links, no tracking or analytics,
                        no sponsored posts, and no paywall. My motivation for this site is to have a
                        space for self-expression and to share what I've learned with the world.
                        I hope I will inspire others to make their own creative corner on the web as well.''').style('margin-bottom: 1rem')

            ui.label(
                '''Feel free to contact me by email at wptmdoorn at gmail.com!''')

        with ui.element('div').classes('col-xs-12 col-md-4').style('order: 1'):
            ui.image(
                'app/static/home_profile.png')
