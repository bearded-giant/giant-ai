"""
Example target pattern for modern Python async/await usage
Use with: ai-pattern-refactor refactor "asyncio" --target-pattern patterns/async-python-pattern.py
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


async def fetch_user_data(user_id: int) -> Dict[str, Any]:
    """Modern async pattern with proper error handling and concurrency"""
    try:
        # Concurrent operations using asyncio.gather
        user_task = fetch_user(user_id)
        preferences_task = fetch_user_preferences(user_id)
        permissions_task = fetch_user_permissions(user_id)
        
        # Wait for all tasks concurrently
        user, preferences, permissions = await asyncio.gather(
            user_task,
            preferences_task, 
            permissions_task,
            return_exceptions=True  # Don't fail all if one fails
        )
        
        # Handle individual failures
        if isinstance(user, Exception):
            logger.error(f"Failed to fetch user: {user}")
            raise ValueError(f"User {user_id} not found")
            
        # Process results that succeeded
        profile = await build_user_profile(
            user=user if not isinstance(user, Exception) else None,
            preferences=preferences if not isinstance(preferences, Exception) else {},
            permissions=permissions if not isinstance(permissions, Exception) else []
        )
        
        return {
            **profile,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.exception(f"Failed to fetch user data for {user_id}")
        raise


async def retry_async_operation(
    operation,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0
) -> Any:
    """Retry pattern for async operations with exponential backoff"""
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return await operation()
        except asyncio.CancelledError:
            # Don't retry on cancellation
            raise
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = initial_delay * (backoff_factor ** attempt)
                logger.warning(
                    f"Operation failed (attempt {attempt + 1}/{max_retries}), "
                    f"retrying in {delay}s: {e}"
                )
                await asyncio.sleep(delay)
            else:
                logger.error(f"Operation failed after {max_retries} attempts")
    
    raise last_exception


async def process_batch_async(
    items: List[Any],
    processor_func,
    max_concurrent: int = 10
) -> List[Any]:
    """Process items in batches with controlled concurrency"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(item):
        async with semaphore:
            return await processor_func(item)
    
    # Create tasks for all items
    tasks = [
        asyncio.create_task(process_with_semaphore(item))
        for item in items
    ]
    
    # Wait for all tasks with progress tracking
    results = []
    for i, task in enumerate(asyncio.as_completed(tasks)):
        try:
            result = await task
            results.append(result)
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(items)} items")
        except Exception as e:
            logger.error(f"Failed to process item: {e}")
            results.append(None)
    
    return results


@asynccontextmanager
async def async_timed_operation(operation_name: str):
    """Context manager for timing async operations"""
    start_time = asyncio.get_event_loop().time()
    logger.info(f"Starting {operation_name}")
    
    try:
        yield
    finally:
        elapsed = asyncio.get_event_loop().time() - start_time
        logger.info(f"Completed {operation_name} in {elapsed:.2f}s")


# Example usage with proper async context manager
async def fetch_all_users(user_ids: List[int]) -> List[Dict[str, Any]]:
    """Fetch multiple users efficiently with async"""
    async with async_timed_operation("fetch_all_users"):
        return await process_batch_async(
            items=user_ids,
            processor_func=fetch_user_data,
            max_concurrent=20
        )


# Async generator pattern for streaming data
async def stream_user_updates(user_id: int):
    """Async generator for streaming updates"""
    async with connect_to_updates_stream(user_id) as stream:
        async for update in stream:
            try:
                processed = await process_update(update)
                yield processed
            except Exception as e:
                logger.error(f"Failed to process update: {e}")
                # Continue processing other updates
                continue