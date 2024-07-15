model=TheBloke/zephyr-7B-beta-AWQ
volume=$PWD/data

docker run --gpus all \
--shm-size 1g \
-p 8080:80 \
-v $volume:/data \
ghcr.io/huggingface/text-generation-inference:1.4.0 \
--model-id $model \
--quantize awq \
--max-input-length 8191 \
--max-total-tokens 8192 \
--max-batch-prefill-tokens 8191
