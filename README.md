# Nerdless
A conversational AI Telegram bot based on a language model finetuned on a custom dataset.

The bot randomly responds to random messages with a chance set by command.

You can have a conversation with the bot by mentioning it, replying to its message, or texting it privately.

## Model
Used [raw imageboard dialogues data](https://github.com/Koziev/NLP_Datasets) and processed it into a dataset (notebook available at `notebooks/dataset.ipynb`).

Finetuned ruDialoGPT-medium on the dataset (notebook available at `notebooks/finetuning.ipynb`).

The model card is available at [HuggingFace 🤗](https://huggingface.co/rakepants/ruDialoGPT-medium-finetuned-toxic).
## Technologies
- **transformers** - for cleaning the data, finetuning and running the model
- **aiogram 3** - for the Telegram bot
- **asyncio** - for non-blocking generation
- **PostgreSQL** - for keeping records of history and settings for chats
- **SQLAlchemy** - for interacting with the database 
- **Docker** - for keeping the deployment environment consistent
- **docker-compose** - for automating the deployment
## Setup
To run this project:
1. Clone the repository
2. Create a `.env` configuration and fill it in:
   ```env
   # Telegram bot configuration
   TELEGRAM_TOKEN=
   MODE=polling 
   PORT=

   MODEL_MODE=local  # Running the model locally or pulling from HF
   HF_MODEL_NAME=rakepants/ruDialoGPT-medium-finetuned-toxic

   # Database configuration
   DATABASE_HOSTNAME=db
   DATABASE_PORT=5432
   # Put a strong password here  
   DATABASE_PASSWORD=
   DATABASE_NAME=nerdless
   DATABASE_USERNAME=postgres

   # Port that the Docker will use
   POSTGRES_CONTAINER_PORT=5454```
3. If running the model locally, download the [model weights](https://huggingface.co/rakepants/ruDialoGPT-medium-finetuned-toxic) and put them into ./app/ai/model/{model_folder_name}
4. Run `docker-compose up --build` in Terminal.
## Creators
Made by [Artyom Eryomkin](https://github.com/RakePants) & [Mikhail Kuznecov](https://github.com/PixelPantz)
