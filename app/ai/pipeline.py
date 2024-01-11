import asyncio
import logging
from functools import partial

from app.ai.lm import model_generate, tokenizer
from app.utils.processing import process_output


async def answer(input):
    """Generate text using the LM."""
    
    loop = asyncio.get_event_loop()
    generated_token_ids = await loop.run_in_executor(None, partial(model_generate, input))
    context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
    
    generation = context_with_response[0]
    output = await process_output(generation)

    logging.info(f"Generation: {output}")
    return output
