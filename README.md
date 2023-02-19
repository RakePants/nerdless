# Nerdless
An AI chat bot for Telegram groups with 3 presets and an ability to participate in continious dialogues.

## About
The bot has 3 presets: toxic, sad, vulgar. These can be switched in a chat a by user with a help of commands anytime.

It can automatically respond to random messages.
You can force a conversation with the bot by mentioning it.

To start a dialogue with the bot when it has already written something, use the Reply function of Telegram. The bot will remember all messages of such a chain.
You can also use a command to end such a dialogue with the bot and clear its memory.

## Development
Used raw imageboard dialogues as a dataset https://github.com/Koziev/NLP_Datasets

Filtered dialogues by toxicity, obscenity and sadness using these models:

toxicity: https://huggingface.co/sismetanin/rubert-toxic-pikabu-2ch with `score > 0.93`\
obscenity: https://huggingface.co/apanc/russian-sensitive-topics \
sadness: https://huggingface.co/cointegrated/rubert-tiny2-cedr-emotion-detection with `score > 0.8`

Scoring scripts are available in this repository.

Finetuned https://huggingface.co/tinkoff-ai/ruDialoGPT-medium model on these 3 datasets indepently using `transformers`.\
Colab Notebooks of the process are also available.

Used AIOgram to develop an asynchronous Telegram bot.

## Usage
Available at @nerdless_bot in Telegram

## Creators
Made by: https://github.com/RakePants (Artyom Eryomkin) & https://github.com/PixelPantz
