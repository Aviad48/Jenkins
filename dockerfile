FROM python:latest as compiler
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN python -m venv venv
# Enable venv
ENV PATH="/app/venv/bin:$PATH"
COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:alpine as runner
WORKDIR /app/
COPY --from=compiler /app/venv /app/venv

# Enable venv
ENV PATH="/app/venv/bin:$PATH"
ENV AWS_ACCESS_KEY=
ENV AWS_SECRET_KEY=
ENV SLEEP_INTERVAL=300
COPY . /app/
CMD ["python", "aws-filter.py"]
