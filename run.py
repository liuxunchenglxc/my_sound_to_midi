from buzzheavier import BuzzHeavier
import subprocess
import os

def main(args):
    bzid = args.bzid
    buzzheavier = BuzzHeavier(bzid)
    dir_id = "petx5xp6bem3"
    src_suffix = "flac"
    res_suffix = "mid"
    src_dict = buzzheavier.find_file_by_suffix(dir_id, "." + src_suffix)
    res_dict = buzzheavier.find_file_by_suffix(dir_id, "." + res_suffix)
    for res_file in res_dict.keys():
        src_file = res_file.replace("." + res_suffix, "." + src_suffix)
        if src_file in src_dict:
            print(f"Removing {src_file} because {res_file} exists.")
            del src_dict[src_file]
    if src_dict:
        os.makedirs("res", exist_ok=True)
        
        for src_file, src_url in src_dict.items():
            save_path = f"res/{src_file}"
            buzzheavier.download_file(src_url, save_path)
            res_fn = src_file.replace("." + src_suffix, "." + res_suffix)
            # demucs
            subprocess.run(["demucs", "--flac", save_path])
            subprocess.run(["tree", "separated"])
            # demucs paths
            demucs_dir_path = "separated/htdemucs/" + src_file.removesuffix("." + src_suffix)
            bass_path = os.path.join(demucs_dir_path, "bass.flac")
            drums_path = os.path.join(demucs_dir_path, "drums.flac")
            other_path = os.path.join(demucs_dir_path, "other.flac")
            vocals_path = os.path.join(demucs_dir_path, "vocals.flac")
            if os.path.exists(res_fn):
                buzzheavier.upload_file(dir_id, res_fn)
    print("All tasks completed successfully!")

        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("bzid", help="BuzzHeavier API token")
    args = parser.parse_args()
    main(args)
