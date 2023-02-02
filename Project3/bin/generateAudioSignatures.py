import glob
import os
from getMaxFrequencies import get_signature_from_audio


def create_signatures(filename=None, output_folder="signatures/"):
    if output_folder != '':
        is_exist = os.path.exists(output_folder)
        if not is_exist:
            os.mkdir(output_folder)

    if filename:
        return get_signature_from_audio(filename, f'{output_folder}{filename.split("/")[1][:-4]}.txt')
    else:
        sample_files = [f for f in glob.glob("audio/*.wav")]
        for sample in sample_files:
            get_signature_from_audio(sample, f'{output_folder}{sample[6:-4]}.txt')
        return [f[11:] for f in glob.glob(f"{output_folder}*.txt")]


if __name__ == '__main__':
    create_signatures()
