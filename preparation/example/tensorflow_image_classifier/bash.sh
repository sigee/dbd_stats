docker run --rm -it -v $1:/tf_files -v $2:/img/guess.jpg xblaster/tensor-guess bash

docker run --rm -it -v ./my_training_data:/tf_files -v ./original.jpg:/img/guess.jpg xblaster/tensor-guess bash