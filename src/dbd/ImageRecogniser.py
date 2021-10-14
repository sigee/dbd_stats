import tensorflow as tf


class DbdImageRecogniser:
    def __init__(self):
        self.label_lines = [line.rstrip() for line in tf.io.gfile.GFile("retrained_labels.txt")]
        with tf.io.gfile.GFile("retrained_graph.pb", 'rb') as file:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(file.read())
            _ = tf.import_graph_def(graph_def, name='')
        self.sess = tf.compat.v1.Session()

    def get_text(self, image_url):
        image_data = tf.io.gfile.GFile(image_url, 'rb').read()
        softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')
        predictions = self.sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = self.label_lines[node_id]
            score = predictions[0][node_id] * 100
            if score > 25:
                return human_string
        return "-= No info =-"
