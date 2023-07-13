FROM python:3.11.4-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create non-root user 'runtime'
RUN groupadd -r runtime && \
    useradd -r -g runtime runtime

# use 'runtime' users home directory as workdir
WORKDIR /home/runtime

# install python requirements
COPY ./requirements.txt /home/runtime/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy python package and chown to 'runtime' user
COPY --chown=runtime:runtime ./api/ /home/runtime/api/

# run with non-root user
USER runtime