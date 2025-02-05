## OpenAI Details
OPENAI_MODEL = "gpt-4-0125-preview"
OPENAI_API_KEY = ""

## MistralAI Details
MISTRALAI_MODEL = "mistral-large-latest"
MISTRALAI_API_KEY = ""

## AnthropicAI Details
ANTHROPICAI_MODEL = "claude-3-opus-20240229"
ANTHROPICAI_API_KEY = ""

## Choose Your Provider: openai, mistral or anthropic
PROVIDER = "mistral"

## Generation Details
OUTPUT_FILE_PATH = "dataset.jsonl"
NUM_WORKERS = 4

NUM_TURNS = (
    1  ## Need to be at-least 2 for multi-turn. 1 makes it a single quesion-answer pair.
)
