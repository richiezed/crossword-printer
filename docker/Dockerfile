FROM python:3.11-slim

WORKDIR /cw

COPY requirements.txt ./

RUN apt update && apt install -y chromium chromium-driver
#RUN apt update

RUN groupadd -r chrome && useradd -r -g chrome -G audio,video -m -d /home/chrome chrome \
    && mkdir -p /home/chrome/downloads \
    && chown -R chrome:chrome /home/chrome

# Switch to the non-root user
USER chrome

ENV PIP_BREAK_SYSTEM_PACKAGES=1
#RUN pip install PyChromeDevTools && pip install pypdf==3.16.4 && pip install selenium==4.14.0 && pip install webdriver-manager==4.0.1

RUN pip3 install --break-system-packages -r requirements.txt 

COPY *.py ./

# command to run on container start
#CMD [ "python3", "cw.py" ] 
CMD ["/bin/sh"]
#ENTRYPOINT [ "/bin/sh" ]

