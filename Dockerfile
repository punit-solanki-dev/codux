# Use the official Python image as a base
FROM python:3.12.4-alpine

# Set work directory
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/compiler-project
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN apk update 
RUN apk add \
    # build-essential \
    openjdk17 \
    bash \
    libpq \
    libgcc \ 
    libstdc++ \
    postgresql-dev \
    libc-dev \
    gcc \
    g++ \
    python3-dev \
    musl-dev \
    linux-headers \
    pcre-dev \
    build-base \
    libffi-dev

RUN java -version
# Copy requirements and install dependencies
# Install dependencies
COPY ./requirements.txt $APP_HOME/requirements.txt
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv env
RUN source env/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.prod.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Expose the port that Gunicorn will run on
EXPOSE 8080

# Start Gunicorn server
ENTRYPOINT ["sh", "./entrypoint.sh"]
