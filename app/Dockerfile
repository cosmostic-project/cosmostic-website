FROM python:3.12.2-alpine

# install dependencies
RUN apk add libffi-dev

# upgrade pip
RUN pip install --upgrade pip

# create work user and workdir
RUN adduser -D workuser
RUN mkdir /app && chown -R workuser:workuser /app
WORKDIR /app
USER workuser

# install dependencies
COPY --chown=workuser:workuser requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

# copy all files
COPY --chown=workuser:workuser . .

# run app
EXPOSE 80
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]