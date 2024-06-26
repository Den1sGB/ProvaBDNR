import aioredis

redis = aioredis.from_url("redis://localhost", decode_responses=True)

async def get_redis():
    return redis
