import redis


if __name__ == "__main__":
    r = redis.Redis(host='172.17.0.3', port=6379, decode_responses=True, db=0, password='zaniu', socket_timeout=3)
    print(r.get('zaniu'))
