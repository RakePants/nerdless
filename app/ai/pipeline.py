import asyncio
from functools import partial
from app.ai.lm import model_generate, tokenizer
from app.ai.utils import strip_text


async def answer(input):
    """Generate text using the LM."""
    
    loop = asyncio.get_event_loop()
    generated_token_ids = await loop.run_in_executor(None, partial(model_generate, input))
    context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
    
    generation = context_with_response[0]
    print(generation)

    answer = await strip_text(generation)

    return answer
