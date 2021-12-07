from tensorflow.keras.models import load_model
from bento_service import MnistService
import h5py
from tensorflow.python.lib.io import file_io
import argparse

def get_args():
    parser = argparse.ArgumentParser()
  
    parser.add_argument(
        '--model_path',
        type=str,
        required=True)

    args = parser.parse_args()
    return args

def main():
    args = get_args()
    model_path = args.model_path
    print("model path :", model_path)

    with file_io.FileIO(args.model_path, mode='rb') as model_file:
        model_gcs = h5py.File(model_file, 'r')
        model = load_model(model_gcs)

    mnist_svc = MnistService()
    mnist_svc.pack("model", model)

    saved_path = mnist_svc.save()
    print(f"saved_path : {saved_path}")

if __name__ == '__main__':
  main()