# Terminal3
## gpt_backend
A gpt-3.5-turbo based backend. This API allows users to interact with the chat system using a provided web3 wallet address and a prompt.

## Endpoints

### POST /chat

Starts a new chat based on the provided wallet address and prompt.

#### Request

**Headers**

- Content-Type: application/json

**Body**

```json
{
  "wallet_address": "string",
  "prompt": "string"
}
```

### Response

Success (HTTP Status Code: 200)
```json
{
  "response": "string"
}
```

Error (HTTP Status Code: 400)
```json
{
  "error": "Invalid request. Provide wallet_address and prompt."
}
```

Error (HTTP Status Code: 500)
```json
{
  "error": "string"
}
```

### Example

```bash
curl -X POST -H "Content-Type: application/json" -d '{"wallet_address": "0x12345", "prompt": "Hello"}' http://localhost:5000/chat
```

### References:
1. https://www.mlq.ai/fine-tuning-gpt-3-question-answer-bot/
2. https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-2-create-qa.ipynb
3. https://platform.openai.com/docs/guides/fine-tuning/advanced-usage
4. https://dagster.io/blog/chatgpt-langchain
5. https://gist.github.com/veekaybee/6f8885e9906aa9c5408ebe5c7e870698
6. https://arxiv.org/abs/2005.14165
7. https://github.com/Vinithavn/Finetune-GPT-3-for-customer-support-chatbot-
8. https://github.com/karpathy/nanoGPT
9. https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-3-train-qa.ipynb
10. https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-1-collect-data.ipynb


