


require-redis:
        docker run \
        --rm \
        --detach \
        --name redis \
        --publish 6379:6379 \
        redis