from nicegui import ui


def content() -> None:
    ui.html('<h2> William van Doorn </h2>').style('font-weight:700; font-size:2rem')

    with ui.element('div').classes('row').style('font-size:1.1rem'):
        with ui.element('div').classes('col-xs-12 col-md-8'):
            ui.label(
                '''Hi, I’m William. I’m currently a resident in clinical chemistry at Maastricht University Medical Center. 
                I also have a passion for building (digital) stuff.''').style('margin-bottom: 1rem')

            ui.label('''This website is my personal corner on the web, 
                     where I share my writing, projects, tutorials, and whatever else inspires me. 
                     You can explore my blog or check out the projects page to see some of 
                     my open-source work.''').style('margin-bottom: 1rem')

            ui.label('''This site is completely ad-free, with no affiliate links, 
                     tracking, or paywalls—just a space for me to express myself and 
                     share what I’ve learned. My goal is to inspire others to create 
                     their own digital spaces and explore their creativity.''').style('margin-bottom: 1rem')

            ui.label(
                '''Feel free to contact me by email at wptmdoorn at gmail.com!''')

        with ui.element('div').classes('col-xs-12 col-md-4').style('order: 1'):
            ui.image(
                'app/static/home_profile.png')
