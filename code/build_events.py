#!/usr/bin/env python
"""Build BIDS *_events.tsv for nm000180 (Brennan2019 Alice-in-Wonderland EEG).

Per-subject proc.mat 'trl' columns = [start_sample, stop_sample, offset] + varnames
(varnames = [segment, tmin, Order]). Word onset in the continuous EEG is the
FieldTrip event sample = start_sample - offset (offset = -150 = 0.3 s prestim),
so onset_seconds = (start_sample - offset) / 500. Each trial's 'Order' identifies
the word, so we MERGE on Order with AliceChapterOne-EEG.csv (correct for subjects
with rejected trials, not naive row position).
"""
import argparse, glob, json, os, re
import numpy as np
import pandas as pd
from scipy.io import loadmat

SFREQ = 500.0
TASK = "alicelistening"

CSV_MAP = {  # CSV column -> BIDS events column
    "Word": "word", "Sentence": "sentence_id", "Position": "position_in_sentence",
    "Segment": "segment", "IsLexical": "is_lexical", "LogFreq": "log_freq",
    "LogFreq_Prev": "log_freq_prev", "LogFreq_Next": "log_freq_next",
    "SndPower": "sound_power",  # NB: Length -> duration only (no separate word_length; identical column)
    "NGRAM": "ngram_surprisal", "RNN": "rnn_surprisal", "CFG": "cfg_surprisal",
}
COL_ORDER = ["onset", "duration", "trial_type", "word", "stim_file", "word_index",
             "sentence_id", "position_in_sentence", "segment", "is_lexical", "log_freq",
             "log_freq_prev", "log_freq_next", "sound_power",
             "ngram_surprisal", "rnn_surprisal", "cfg_surprisal"]
STIM_FMT = "DownTheRabbitHoleFinal_SoundFile%d.wav"  # BIDS /stimuli/ file per audio segment

def read_trl(matfile):
    p = loadmat(matfile, squeeze_me=True, struct_as_record=True,
                simplify_cells=True)["proc"]
    trl = np.asarray(p["trl"], dtype=float)
    cols = ["start_sample", "stop_sample", "offset"] + list(p["varnames"])
    return pd.DataFrame(trl, columns=cols[:trl.shape[1]])

def find_mat(proc_dir, sxx):
    for pat in (f"**/{sxx}.mat", f"{sxx}.mat"):
        hits = sorted(h for h in glob.glob(os.path.join(proc_dir, pat), recursive=True)
                      if "__MACOSX" not in h)
        if hits:
            return hits[0]
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc-dir", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--bids", required=True)
    a = ap.parse_args()

    story = pd.read_csv(a.csv)
    assert "Order" in story.columns and len(story) == 2129, "bad annotations CSV"

    subs = sorted(d for d in os.listdir(a.bids) if re.fullmatch(r"sub-\d+", d))
    built = skipped = 0
    for sub in subs:
        sxx = "S%02d" % int(sub.split("-")[1])
        mat = find_mat(a.proc_dir, sxx)
        if not mat:
            print(f"  {sub} ({sxx}): no proc .mat -> SKIP"); skipped += 1; continue
        trl = read_trl(mat)
        # true word-onset time (s) in the continuous EEG (FieldTrip event = begsample - offset)
        onset = ((trl["start_sample"] - trl["offset"]) / SFREQ).round(6)
        # merge word annotations by Order (robust to rejected trials); avoid onset/offset name clash
        trl_min = pd.DataFrame({"Order": trl["Order"].astype(int), "eeg_onset": onset})
        m = trl_min.merge(story, on="Order", how="left", validate="one_to_one")
        n_missing = m["Word"].isna().sum()
        ev = pd.DataFrame({"onset": m["eeg_onset"], "trial_type": "word"})
        ev["word_index"] = m["Order"].astype("Int64")
        for c_csv, c_bids in CSV_MAP.items():
            if c_csv in m.columns:
                ev[c_bids] = m[c_csv].values
        ev["duration"] = m["Length"].round(6)
        ev["stim_file"] = [STIM_FMT % int(s) if pd.notna(s) else "n/a" for s in m["Segment"]]
        for c in ("word_index", "sentence_id", "position_in_sentence", "segment", "is_lexical"):
            if c in ev.columns:
                ev[c] = ev[c].round().astype("Int64")   # integer, not '1.000000'
        ev = ev[[c for c in COL_ORDER if c in ev.columns]].sort_values("onset").reset_index(drop=True)
        out = os.path.join(a.bids, sub, "eeg", f"{sub}_task-{TASK}_events.tsv")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        # %.10g (not %.6f): preserves tiny-magnitude sound_power (~1e-9..1e-3) that
        # fixed 6-decimal formatting would flatten to 0.000000; normal cols stay readable.
        ev.to_csv(out, sep="\t", index=False, na_rep="n/a", float_format="%.10g")
        note = f" ({n_missing} words unmatched)" if n_missing else ""
        print(f"  {sub} ({sxx}): {len(ev)} word events{note} -> {out}")
        built += 1

    ejson = {
        "onset": {"Description": "Onset of the spoken word in the continuous EEG recording", "Units": "s"},
        "duration": {"Description": "Spoken duration of the word", "Units": "s"},
        "trial_type": {"Description": "Event category", "Levels": {"word": "A spoken word in the audiobook"}},
        "word": {"Description": "Orthographic form of the spoken word"},
        "stim_file": {"Description": "Audiobook segment (in /stimuli/) during which the word was heard"},
        "word_index": {"Description": "Order of the word in the story (Brennan 'Order'; 1-2150, 2129 annotated)"},
        "sentence_id": {"Description": "Sentence number the word belongs to"},
        "position_in_sentence": {"Description": "Ordinal position of the word within its sentence"},
        "segment": {"Description": "Audio segment (1-12) in which the word occurs"},
        "is_lexical": {"Description": "Open-class/content word (1) vs closed-class/function word (0)",
                        "Levels": {"1": "content/open-class", "0": "function/closed-class"}},
        "log_freq": {"Description": "Log lexical frequency of the word"},
        "log_freq_prev": {"Description": "Log lexical frequency of the preceding word"},
        "log_freq_next": {"Description": "Log lexical frequency of the following word"},
        "sound_power": {"Description": "Acoustic sound power (RMS) at word onset"},
        "ngram_surprisal": {"Description": "Word surprisal from a 3-gram (Markov) language model"},
        "rnn_surprisal": {"Description": "Word surprisal from a recurrent neural-network language model"},
        "cfg_surprisal": {"Description": "Word surprisal from a context-free-grammar (hierarchical) parser"},
    }
    with open(os.path.join(a.bids, f"task-{TASK}_events.json"), "w") as f:
        json.dump(ejson, f, indent=4)
    print(f"\nDONE: events for {built} subjects, {skipped} skipped.")

if __name__ == "__main__":
    main()
