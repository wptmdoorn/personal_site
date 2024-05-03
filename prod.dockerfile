FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN locale-gen nl_NL.UTF-8  
ENV LANG nl_NL.UTF-8  
ENV LANGUAGE nl_NL:nl 
ENV LC_ALL nl_NL.UTF-8  
RUN update-locale LANG=nl_NL.UTF-8

WORKDIR /code
RUN mkdir -p /code/output/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright python -m playwright install --with-deps chromium
 
COPY ./app /code/app
COPY ./app/static /code/static/

CMD ["python", "app/main.py"]
