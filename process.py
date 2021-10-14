import tensorflow as tf
from PIL import Image
# import sys
import os
# import csv


def get_text(image_url):
    image_data = tf.io.gfile.GFile(image_url, 'rb').read()
    label_lines = [line.rstrip() for line in tf.io.gfile.GFile("retrained_labels.txt")]
    with tf.io.gfile.GFile("retrained_graph.pb", 'rb') as file:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(file.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id] * 100
            if score > 90:
                print('%s (score = %.5f)' % (human_string, score))
                return human_string
            else:
                print('%s (score = %.5f)' % (human_string, score))
        return "-= Nincs információ =-"


print("TensorFlow version:", tf.__version__)

# original_image_url = sys.argv[1]
# original_image_url = 'D:\\work\\github\\dbd_stats\\original_clown.png'
original_image_url = 'D:\\work\\github\\dbd_stats\\original_cenobite.png'
original_image = Image.open(original_image_url)

rank_image = original_image.crop((80, 700, 180, 810))
rank_image_filename = "rank.png"
rank_image.save(rank_image_filename)
rank_text = get_text(rank_image_filename)
os.remove(rank_image_filename)
print('Rank: ' + rank_text)


# perk1_image = original_image.crop((180, 740, 240, 795))
# perk1_image_filename = "perk1.png"
# perk1_image.save(perk1_image_filename)
# perk1_text = get_text(perk1_image_filename)
# os.remove(perk1_image_filename)


# perk2_image = original_image.crop((235, 740, 295, 795))
# perk2_image_filename = "perk2.png"
# perk2_image.save(perk2_image_filename)
# perk2_text = get_text(perk2_image_filename)
# os.remove(perk2_image_filename)

# perk3_image = original_image.crop((290, 740, 355, 795))
# perk3_image_filename = "perk3.png"
# perk3_image.save(perk3_image_filename)
# perk3_text = get_text(perk3_image_filename)
# os.remove(perk3_image_filename)

# perk4_image = original_image.crop((345, 740, 405, 795))
# perk4_image_filename = "perk4.png"
# perk4_image.save(perk4_image_filename)
# perk4_text = get_text(perk4_image_filename)
# os.remove(perk4_image_filename)

killer_image = original_image.crop((480, 740, 530, 795))
killer_image_filename = "killer.png"
killer_image.save(killer_image_filename)
killer_text = get_text(killer_image_filename)
os.remove(killer_image_filename)
print('Killer: ' + killer_text)

# print("Rank: ", rank_text, " | Killer: ", killer_text, " | Perks: ", perk1_text, ", ", perk2_text, ", ", perk3_text, ", ", perk4_text)

# fields = ['rank', 'killer', 'perk1', 'perk2', 'perk3', 'perk4']
# with open(r'stats.csv', 'a') as f:
#      writer = csv.writer(f)
#      writer.writerow(fields)
