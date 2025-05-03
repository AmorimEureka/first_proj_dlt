FROM quay.io/astronomer/astro-runtime:12.8.0

USER root

WORKDIR "/usr/local/airflow"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements.txt

RUN chown -R astro:astro /usr/local/airflow && \
chmod -R 775 /usr/local/airflow

USER astro