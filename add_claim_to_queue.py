#!/usr/bin/env python3
"""
add_claim_to_queue.py

This script adds a claim ID to the Redis 'claims' queue to trigger processing.
Usage:
    python add_claim_to_queue.py <CLAIM_ID>
"""
import sys
import redis

if len(sys.argv) != 2:
    print("Usage: python add_claim_to_queue.py <CLAIM_ID>")
    sys.exit(1)

claim_id = sys.argv[1]
redis_client = redis.Redis(host='redis', port=6379, db=0)
redis_client.rpush('claims', claim_id)
print(f"Added claim ID '{claim_id}' to the 'claims' queue.")
