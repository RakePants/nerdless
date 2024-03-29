# Nerdless
A conversational AI Telegram bot based on a language model finetuned on a custom dataset.

The bot randomly responds to random messages with a chance set by command.

You can talk to the bot by mentioning it, replying to its message, or texting it privately.

## Model
Used [raw imageboard dialogues data](https://github.com/Koziev/NLP_Datasets) and processed it into a dataset (notebook available at `notebooks/dataset.ipynb`).

Finetuned ruDialoGPT-medium on the dataset (notebook available at `notebooks/finetuning.ipynb`).

The model card is available at [HuggingFace 🤗](https://huggingface.co/rakepants/ruDialoGPT-medium-finetuned-toxic).
## Technologies
- **transformers** - for cleaning the data, finetuning and running the model
- **aiogram 3** - for the Telegram bot
- **asyncio** - for non-blocking response generation
- **PostgreSQL** - for keeping records of history and settings for chats
- **SQLAlchemy** - for interacting with the database 
- **Docker** - for a consistent and safe deployment 
## Launch
To run the Telegram bot application:
1. Clone the repository
2. Switch to the repository directory
3. Create a `.env` configuration and fill it in:
   ```env
   # Telegram bot configuration
   TELEGRAM_TOKEN=
   MODE=polling  # 'webhook' for webhook mode
   PORT=

   # Language model configuration
   MODEL_MODE=local  # Running the model locally; to pull from HF, put in anything else
   HF_MODEL_NAME=rakepants/ruDialoGPT-medium-finetuned-toxic  # Used for pulling the model when running non-locally

   # Database configuration
   DATABASE_HOSTNAME=db
   DATABASE_NAME=
   DATABASE_USERNAME=
   DATABASE_PASSWORD=
   DB_CONTAINER_PORT=5454  # Exposed database container port
   ```
4. If running the model locally instead of pulling from HuggingFace, download the [model weights](https://huggingface.co/rakepants/ruDialoGPT-medium-finetuned-toxic) and put them into *./app/ai/model/ruDialoGPT-medium-finetuned-toxic*
5. Run `docker-compose up --build`.
## Creators
Made by [Artyom Eryomkin](https://github.com/RakePants) & [Mikhail Kuznecov](https://github.com/PixelPantz)
