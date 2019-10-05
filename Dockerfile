FROM gorialis/discord.py

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
#ENV DISCORD_HELLO_TOKEN XXXXXX
CMD ["python", "bot.py"]