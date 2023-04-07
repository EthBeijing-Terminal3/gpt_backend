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



