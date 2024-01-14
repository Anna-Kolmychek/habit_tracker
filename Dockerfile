FROM python:3

WORKDIR /habit_tracker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .