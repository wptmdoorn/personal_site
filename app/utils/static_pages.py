from fastapi import Request
from fastapi.responses import FileResponse


# contains static pages functions
# each function name is the url (e.g. tool_vws -> /tool_vws)
def tool_diagnostische_ai(request: Request, template):
    file_path = f"app/static/diagnostisch_ai_funnel_v0.8.pdf"

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        # triggers download, or force inline below
        headers={
            "Content-Disposition": f'inline; filename="Diagnostische AI Funnel (v0.8)"'}
    )
