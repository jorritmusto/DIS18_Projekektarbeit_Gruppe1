FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install luigi

EXPOSE 3333

# Run Luigi scheduler by default when the container launches
CMD ["luigid", "--port", "3333"]

CMD ["python", "-m", "luigi", "--module", "tasks.create_initial_items", "CreateInitialItemsTask"]
