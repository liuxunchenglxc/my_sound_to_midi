from buzzheavier import BuzzHeavier
import subprocess
import os
import pretty_midi

def main(args):
    bzid = args.bzid
    buzzheavier = BuzzHeavier(bzid)
    dir_id = "petx5xp6bem3"
    src_suffix = "flac"
    res_suffix = "mid"
    src_dict = buzzheavier.find_file_by_suffix(dir_id, "." + src_suffix)
    res_dict = buzzheavier.find_file_by_suffix(dir_id, "." + res_suffix)
    
    def res_to_src(path):
        return path.replace("." + res_suffix, "." + src_suffix)
    
    def src_to_res(path):
        return path.replace("." + src_suffix, "." + res_suffix)
    
    for res_file in res_dict.keys():
        src_file = res_to_src(res_file)
        if src_file in src_dict:
            print(f"Removing {src_file} because {res_file} exists.")
            del src_dict[src_file]
    if src_dict:
        os.makedirs("res", exist_ok=True)
        
        for src_file, src_url in src_dict.items():
            save_path = f"res/{src_file}"
            buzzheavier.download_file(src_url, save_path)
            res_fn = src_to_res(src_file)
            # demucs
            subprocess.run(["demucs", "--flac", save_path])
            subprocess.run(["tree", "separated"])
            # demucs paths
            demucs_dir_path = "separated/htdemucs/" + src_file.removesuffix("." + src_suffix)
            bass_path = os.path.join(demucs_dir_path, "bass.flac")
            drums_path = os.path.join(demucs_dir_path, "drums.flac")
            other_path = os.path.join(demucs_dir_path, "other.flac")
            vocals_path = os.path.join(demucs_dir_path, "vocals.flac")
            # omnizart
            base_model_path = "/usr/lib/python3.14/site-packages/omnizart/checkpoints"
            subprocess.run(["tree", base_model_path])
            # For pop type # music_note_stream music_piano music_piano-v2 music_pop
            subprocess.run(["omnizart", "music", "transcribe", "--model-path", os.path.join(base_model_path, "music", "music_piano-v2"), "--output", src_to_res(other_path), other_path])
            # subprocess.run(["omnizart", "vocal", "transcribe", "--output", src_to_res(vocals_path), vocals_path])
            subprocess.run(["omnizart", "music", "transcribe", "--model-path", os.path.join(base_model_path, "music", "music_note_stream"), "--output", src_to_res(bass_path), bass_path])
            subprocess.run(["omnizart", "music", "transcribe", "--model-path", os.path.join(base_model_path, "music", "music_note_stream"), "--output", src_to_res(drums_path), drums_path])
            # merge midi
            # midi_vocal = pretty_midi.PrettyMIDI(src_to_res(vocals_path))
            midi_music = pretty_midi.PrettyMIDI(src_to_res(other_path))
            midi_bass = pretty_midi.PrettyMIDI(src_to_res(bass_path))
            midi_drums = pretty_midi.PrettyMIDI(src_to_res(drums_path))
            merged = pretty_midi.PrettyMIDI()
            # for inst in midi_vocal.instruments:
            #     merged.instruments.append(inst)
            for inst in midi_music.instruments:
                merged.instruments.append(inst)
            for inst in midi_bass.instruments:
                merged.instruments.append(inst)
            for inst in midi_drums.instruments:
                merged.instruments.append(inst)
            merged.write(res_fn)
            # upload
            if os.path.exists(res_fn):
                buzzheavier.upload_file(dir_id, res_fn)
    print("All tasks completed successfully!")

        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("bzid", help="BuzzHeavier API token")
    args = parser.parse_args()
    main(args)
