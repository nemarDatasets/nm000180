[![DOI](https://img.shields.io/badge/DOI-10.82901%2Fnemar.nm000180-blue)](https://doi.org/10.82901/nemar.nm000180)

Brennan2019: EEG during Naturalistic Listening to Alice in Wonderland
====================================================================

Overview
--------
Scalp EEG recorded while participants listened to a 12.4-minute audiobook
recording of the first chapter of *Alice's Adventures in Wonderland* (Lewis
Carroll). This is a naturalistic auditory language-comprehension paradigm
designed to study how the brain builds **hierarchical syntactic structure** and
makes **rapid, incremental linguistic predictions** during continuous listening.

This BIDS dataset contains **45 participants** (`sub-001` … `sub-048`). The
original study by Brennan & Hale (2019) recorded 49 participants (S01–S49) and
analyzed 33 after quality-control exclusions; the mapping from `sub-XXX` to the
original `SXX` identifiers is preserved in the per-subject filenames.

Task
----
- **Task label:** `alicelistening`
- Passive listening to continuous naturalistic speech (an audiobook), presented
  over insert earphones (Etymotic ER-2) at 45 dB above each participant's
  individually determined hearing threshold.
- The ~12.4-minute audio was divided into **12 segments**; a digital trigger was
  sent at the onset of each segment. (Note: segment triggers are absent from the
  re-hosted continuous `.vmrk`; word onsets in `events.tsv` are reconstructed
  from the original per-subject preprocessing output — see *Events*.)
- The audiobook segments are provided in **`stimuli/`**
  (`DownTheRabbitHoleFinal_SoundFile1–12.wav`, 16-bit mono 44.1 kHz), and each word
  event references its segment via the `stim_file` column of `events.tsv`.
- After listening, participants answered multiple-choice comprehension
  questions (8 for most subjects; 4 for an early subset — see the
  `comprehension_n_total` column). Per-subject scores are in `participants.tsv`
  (`sourcedata/comprehension-scores.txt`).

Recording Setup
---------------
- **Amplifier:** BrainVision actiCHamp (Brain Products GmbH)
- **Electrodes:** 61-channel equidistant montage (easyCAP M10), of which **60
  scalp EEG channels** are retained here, plus **1 bipolar vertical EOG (VEOG)**
  over the left eye and **1 audio channel (AUD)** carrying a digitized copy of
  the acoustic stimulus.
- **Sampling rate:** 500 Hz
- **Online filter:** 0.01–200 Hz
- **Reference:** average reference (offline)
- Data collected March 2015 – December 2016 at the University of Michigan
  Computational Neurolinguistics Lab (CNL Lab).

Events and Linguistic Annotations
---------------------------------
The scientific value of this dataset is the alignment of the continuous EEG to
the **word-by-word linguistic structure** of the narrative. Per-subject
`*_events.tsv` files provide one event per spoken word (2129 words), with onsets
in the subject's own EEG time base, and are annotated with the predictors used
in Brennan & Hale (2019):

| Column | Description |
|---|---|
| `onset`, `duration` | Word onset/duration in the EEG recording (seconds) |
| `trial_type` | `word` |
| `word` | The spoken word (orthographic form) |
| `word_index` | Order of the word in the story (Brennan `Order`; 1–2150, 2129 annotated with 21 gaps) |
| `sentence_id` | Sentence number the word belongs to |
| `position_in_sentence` | Ordinal position of the word within its sentence |
| `segment` | Audio segment (1–12) the word occurs in |
| `is_lexical` | 1 = open-class/content word, 0 = closed-class/function word |
| `log_freq` | Log lexical frequency of the word |
| `log_freq_prev`, `log_freq_next` | Log frequency of the preceding / following word |
| `sound_power` | Acoustic sound power at word onset |
| `ngram_surprisal` | Surprisal from a 3-gram language model (`NGRAM`) |
| `rnn_surprisal` | Surprisal from a recurrent neural-network language model (`RNN`) |
| `cfg_surprisal` | Surprisal from a context-free-grammar parser (`CFG`) |

The `ngram_surprisal`, `rnn_surprisal`, and `cfg_surprisal` predictors index
progressively more hierarchical linguistic structure and are the core measures
tested in the paper. Annotations derive from `AliceChapterOne-EEG.csv` (word list
+ predictors) joined to the per-subject `proc.mat` word-onset samples.

Source Data
-----------
`sourcedata/` re-hosts the upstream annotation and preprocessing files from the
Deep Blue Data record (v2, DOI `10.7302/746w-g237`):
- `AliceChapterOne-EEG.csv` — 2129-word linguistic annotations
- `proc/` — per-subject preprocessing outputs (`SXX.mat`; word-onset `trl`)
- `easycapM10-acti61_elec.sfp` — electrode template positions
- `comprehension-questions.doc`, `comprehension-scores.txt` — behavioral task
- `datasets.mat` — subject index

How to cite
-----------
> Brennan, J. R., & Hale, J. T. (2019). Hierarchical structure guides rapid
> linguistic predictions during naturalistic listening. *PLoS ONE*, 14(1),
> e0207741. https://doi.org/10.1371/journal.pone.0207741

> Brennan, J. R. (2023). EEG Datasets for Naturalistic Listening to "Alice in
> Wonderland" (v2). University of Michigan – Deep Blue Data.
> https://doi.org/10.7302/746w-g237

Related
-------
> Bhattasali, S., Brennan, J., Luh, W.-M., Franzluebbers, B., & Hale, J. (2020).
> The Alice datasets: fMRI & EEG observations of natural language comprehension.
> *LREC 2020*. https://aclanthology.org/2020.lrec-1.15/

> Brennan, J. R., & Martin, A. E. (2020). Phase synchronization varies
> systematically with linguistic structure composition. *Phil. Trans. R. Soc. B*,
> 375. https://doi.org/10.1098/rstb.2019.0305

BIDS references
---------------
Appelhoff, S., et al. (2019). MNE-BIDS. *JOSS* 4:1896. https://doi.org/10.21105/joss.01896

Pernet, C. R., et al. (2019). EEG-BIDS. *Scientific Data* 6:103. https://doi.org/10.1038/s41597-019-0104-8
