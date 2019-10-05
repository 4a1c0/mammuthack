FROM gorialis/discord.py

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
ENV DISCORD_HELLO_TOKEN NjI5OTcwMzYzNzA2NjM4MzM3.XZhhgg.NTWrXpo2R_8KzkVutfeRPNAiKAA
CMD ["python", "bot.py"]