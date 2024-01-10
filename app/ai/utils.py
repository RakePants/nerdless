import re

from app.ai.lm import tokenizer


async def remove_unwanted_characters(text) -> str:
    """Remove unwanted characters from a text string"""

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE
    )
    
    # Find all emojis in the text
    emojis = ''.join(emoji_pattern.findall(text))

    # If there are more than two emojis, remove everything after the first one
    if len(emojis) > 2: text = text[:emoji_pattern.search(text).start() + 1]

    # Define a regex pattern to match CJK characters and the Unicode replacement character
    cjk_pattern = re.compile("[\u4e00-\u9fff\ufffd]+")

    # Remove the matched characters
    text = cjk_pattern.sub("", text)

    # Define a regex pattern to match '))', '((', or '::'
    pattern = re.compile(r"\)\)|\(\(|::")

    # Search for the pattern and get the index of the first match
    match = pattern.search(text)
    if match: text = text[:match.start()]

    return text


async def strip_text(text: str) -> str:
    """Strip text from splitters and unwanted characters."""
    
    pad_token = tokenizer.convert_ids_to_tokens(0)  # <pad>
    token_first = tokenizer.convert_ids_to_tokens(50257)  # @@ПЕРВЫЙ@@
    token_second = tokenizer.convert_ids_to_tokens(50258)  # @@ВТОРОЙ@@
    
    text = text.split(token_second)[-1].replace(token_first, '').replace(pad_token, '').strip()  # Get only the model's generation

    clean_text = await remove_unwanted_characters(text)  # Remove unwanted characters from model answer

    return clean_text
