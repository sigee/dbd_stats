import tensorflow as tf
from PIL import Image
import sys
import os


def get_text(image_url):
    image_data = tf.gfile.FastGFile(image_url, 'rb').read()
    label_lines = [line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt")]
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            if score > 80:
                return human_string
                print('%s (score = %.5f)' % (human_string, score))
        return "-= No info =-"


original_image = Image.open("/img/guess.jpg")

rank_image = original_image.crop((80, 700, 180, 810))
rank_image_filename = "rank.jpg"
rank_image.save(rank_image_filename)
#rank_text = get_text(rank_image_filename)
#os.remove(rank_image_filename)


perk1_image = original_image.crop((180, 740, 240, 795))
perk1_image_filename = "perk1.jpg"
perk1_image.save(perk1_image_filename)
#perk1_text = get_text(perk1_image_filename)
#os.remove(perk1_image_filename)


perk2_image = original_image.crop((235, 740, 295, 795))
perk2_image_filename = "perk2.jpg"
perk2_image.save(perk2_image_filename)
#perk2_text = get_text(perk2_image_filename)
#os.remove(perk2_image_filename)

perk3_image = original_image.crop((290, 740, 355, 795))
perk3_image.save("perk3.jpg")
#os.remove(perk1_image_filename)

perk4_image = original_image.crop((345, 740, 405, 795))
perk4_image.save("perk4.jpg")
#os.remove(perk1_image_filename)

killer_image = original_image.crop((480, 740, 530, 795))
killer_image.save("killer.jpg")
#os.remove(perk1_image_filename)


#print("Rank: ", rank_text, " | Perk: ", perk1_text)
