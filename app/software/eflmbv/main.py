from nicegui import ui, app, run
from pytube import YouTube
from io import BytesIO
from .api import download_bv_data

SOFTWARE_TYPE = "NICEGUI"

site_text = """
### EFLM - Biological Variation Database - Downloader

The European Federation of Clinical Chemistry and Laboratory Medicine (EFLM) Biological Variation Database is managed by the EFLM Working Group on Biological Variation (WG-BV) and the Task Group for the Biological Variation Database (TG-BVD).

Following the 1st Strategic Conference of the EFLM defining Analytical Performance Specifications in November 2014, the EFLM Task and Finish Group for the Biological Variation Database (TFG-BVD) was established, with the objective to appraise the quality of BV data that is publicly available. Its terms of reference were to develop a critical appraisal list for the evaluation of BV studies, to use this to assess the existing literature on BV and to extract essential information from those papers and to summarize the results. The result of this work is the EFLM Biological Variation Database.

The EFLM Biological Variation Database is run by the TG-BVD, which is located within the WG-BV in the EFLM.

**If using data from this website for any purpose, it should be referenced as:  
_Aarsand AK, Fernandez-Calle P, Webster C, Coskun A, Gonzales-Lao E, Diaz-Garzon J, Jonker N, Simon M, Braga F, Perich C, Boned B, Marques-Garcia F, Carobene A, Aslan B, Sezer E, Bartlett WA, Sandberg S.
The EFLM Biological Variation Database. https://biologicalvariation.eu/ [time of access]._**
"""


def content():
    app.storage.user['ready'] = False
    app.storage.user['resolutions'] = []
    app.storage.user['resolution'] = -1
    app.storage.user['title'] = None
    app.storage.client['stream'] = None

    async def download():
        _loadlabel = ui.label('Loading BV data...')
        _loadspinner = ui.spinner(size='lg')

        output = await run.cpu_bound(download_bv_data)

        _loadlabel.set_visibility(False)
        _loadspinner.set_visibility(False)

        return ui.download(output.getvalue(), 'bvdata.xlsx')

    with ui.column().classes('items-center justify-center'):
        ui.page_title('EFLM - Biological Variation Database')

        ui.markdown(site_text)

        ui.button('Download BV data',
                  color='green',
                  on_click=download)
