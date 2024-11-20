FROM python:3.12-slim AS dependencies-builder
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    # psycopg-2 build dependencies
    libpq-dev \
    build-essential \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.prod.txt .
RUN pip install --disable-pip-version-check --prefix=/dependencies --no-cache-dir \
    --force-reinstall -r requirements.prod.txt

FROM dependencies-builder AS runtime

ENV APP_DIR=/app
WORKDIR $APP_DIR
# copying copliled libs to folder where python expects them to be
COPY --from=dependencies-builder /dependencies /usr/local
# copying app files
COPY . .
RUN rm requirements.prod.txt
RUN adduser --system --group --no-create-home app_user
RUN chown -R app_user:app_user $APP_DIR
RUN chmod -R 500 $APP_DIR
USER app_user

CMD ["./docker-entrypoint.sh"]