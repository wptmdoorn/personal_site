from nicegui import ui, app, run
# from pytube import YouTube
from io import BytesIO
import base64
import sys
from pytubefix import YouTube

SOFTWARE_TYPE = "NICEGUI"


def _task(l, i):
    output = BytesIO()

    YouTube(l).streams.filter(
        subtype="mp4",
        progressive=True
    )[i].stream_to_buffer(output)

    return output


def content():
    app.storage.user['ready'] = False
    app.storage.user['resolutions'] = []
    app.storage.user['resolution'] = -1
    app.storage.user['title'] = None
    app.storage.client['stream'] = None

    video_output = BytesIO()

    @ui.refreshable
    def video_information():
        if not app.storage.user['title']:
            return

        else:
            ui.label(app.storage.user['title']).style('font-size: 20px')
            ui.select(app.storage.user['resolutions'],
                      value=app.storage.user['resolutions'][0],
                      label='Resolution and Size').classes('w-80').bind_value_to(
                          app.storage.user, 'resolution'
            )

            ui.button('Download',
                      on_click=download_mp4)

    def retrieve_mp4():
        # video = YouTube(link.value)

        # streams = video.streams.filter(
        #    file_extension="mp4",
        #    progressive=True
        # )

        yt = YouTube(link.value)
        print(yt.title)

        streams = yt.streams.filter(
            subtype="mp4",
            progressive=True
        )

        app.storage.user['title'] = yt.title
        app.storage.user['resolutions'] = {
            i: f'{s.resolution} - {round(s.filesize_mb, 2)} MB' for i, s in enumerate(streams)}

        video_information.refresh()

        app.storage.user['ready'] = True

    async def download_mp4():
        _loadlabel = ui.label('Loading video...')
        _loadspinner = ui.spinner(size='lg')

        output = await run.cpu_bound(_task, link.value, app.storage.user['resolution'])

        app.storage.user['ready'] = False

        _loadlabel.set_visibility(False)
        _loadspinner.set_visibility(False)

        ui.label('Video downloaded, download starting!').style(
            'font-size: 20px')

        return ui.download(output.getvalue(), 'output.mp4')

    with ui.column().classes('items-center justify-center'):
        link = ui.input('Youtube URL', placeholder='Enter the YouTube URL')

        ui.button('Submit',
                  on_click=retrieve_mp4).bind_visibility_from(link, 'value')

        video_information()
