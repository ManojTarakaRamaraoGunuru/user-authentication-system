import redis.asyncio as redis
from app.config import config

JTI_EXPIRY = 36000  # seconds

class RedisClient:
    def __init__(self):
        self.client = None
    
    async def initialize(self):
        """Initialize Redis connection"""
        self.client = await redis.from_url(
            f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True
        )
    
    async def add_to_blocklist(self, jti: str) -> None:
        print("Adding jti to the blocklist", jti)
        ## redis store everything as stings, more precisely binary strings
        await self.client.setex(
            f"blocklist:{jti}",
            JTI_EXPIRY,
            True
        )
    
    async def is_blocklisted(self, jti: str) -> bool:
        result = await self.client.get(f"blocklist:{jti}")
        return result == "1"  ## true in the addition will be stored as "1"
    
    async def close(self):

        if self.client:
            await self.client.close()

# Create global Redis client instance
redis_client = RedisClient()

# Convenience functions
async def add_jti_to_blocklist(jti: str) -> None:
    await redis_client.add_to_blocklist(jti)

async def is_jti_blocklisted(jti: str) -> bool:
    return await redis_client.is_blocklisted(jti)