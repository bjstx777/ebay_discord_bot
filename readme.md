# ebay_discord_bot

AWS Lambda bot to scan eBay (later) and post alerts/digests to Discord.

## AWS resources you already created (us-east-1)
### Secrets Manager
- `ebay/keys` (JSON: client_id, client_secret, dev_id optional, environment)
- `discord/webhook/bowman` (JSON: url)
- `discord/webhook/pokemon` (JSON: url)
- `discord/webhook/bowman-bin-digest` (JSON: url)
- `discord/webhook/pokemon-bin-digest` (JSON: url)

### DynamoDB
- `alerts_dedupe` (PK: pk, TTL attribute: ttl_epoch)
- `comps_cache` (PK: signature, TTL attribute: ttl_epoch)

## Lambda IAM role
Role name: `ebay-deal-scanner-lambda-role`
Policies:
- AWSLambdaBasicExecutionRole
- inline `ebay-discord-bot-runtime` (secrets + dynamodb)

## Deploy (manual ZIP upload)
From repo root:

```bash
cd lambda_app
python -m pip install -r requirements.txt -t package
cp app.py package/
cd package
zip -r ../lambda.zip .
```

Upload `lambda_app/lambda.zip` to AWS Lambda.

## Lambda configuration
Runtime: Python 3.12  
Handler: `app.lambda_handler`  
Role: `ebay-deal-scanner-lambda-role`

Environment variables:
- `AWS_REGION=us-east-1`
- `SECRET_EBAY_KEYS=ebay/keys`
- `SECRET_DISCORD_BOWMAN=discord/webhook/bowman`
- `SECRET_DISCORD_POKEMON=discord/webhook/pokemon`
- `SECRET_DISCORD_BOWMAN_DIGEST=discord/webhook/bowman-bin-digest`
- `SECRET_DISCORD_POKEMON_DIGEST=discord/webhook/pokemon-bin-digest`
- `DDB_ALERTS_TABLE=alerts_dedupe`
- `DDB_COMPS_TABLE=comps_cache`

## Test invoke
Use a test event:
```json
{"mode":"test"}
```
You should see a message in the bowman Discord channel.
