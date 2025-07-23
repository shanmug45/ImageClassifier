import os
import json
import redis
import psycopg2
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Postgres connection settings
PG_HOST = 'postgres'
PG_PORT = 5432
PG_DB = 'imageclassdb'
PG_USER = 'postgres'
PG_PASS = 'postgres'  # Change as needed

# Model and image settings
img_height = 150
img_width = 150
model = tf.keras.models.load_model('/workspaces/ImageClassifier/model_P3.h5')

def classify_image(img_path):
    img = image.load_img(img_path, target_size=(img_height, img_width))
    img_array = image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    predicted_class = int(tf.round(predictions[0]).numpy().item())
    return predicted_class

def insert_results_to_db(claim_id, results):
    conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS)
    cur = conn.cursor()
    for result in results:
        cur.execute(
            "INSERT INTO image_classification_results (claim_id, image_name, classification) VALUES (%s, %s, %s)",
            (claim_id, result['image'], result['classification'])
        )
    conn.commit()
    cur.close()
    conn.close()

def process_claim(claim_id):
    claim_dir = f'/data/{claim_id}'
    results = []
    for fname in os.listdir(claim_dir):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(claim_dir, fname)
            outcome = classify_image(img_path)
            results.append({'image': fname, 'classification': outcome})
    # Write results to JSON
    with open(f'/data/{claim_id}_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    # Insert results into Postgres
    insert_results_to_db(claim_id, results)
    # Update status in Redis (set key and push to status_updates queue)
    status_key = f"claim_status:{claim_id}"
    redis_client.set(status_key, "processed")
    status_update = {"claim_id": claim_id, "status": "processed"}
    redis_client.rpush('status_updates', json.dumps(status_update))

def main():
    while True:
        # Blocking pop from Redis queue named 'claims'
        _, claim_id = redis_client.blpop('claims')
        claim_id = claim_id.decode()
        process_claim(claim_id)

if __name__ == '__main__':
    main()
