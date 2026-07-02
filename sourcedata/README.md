# sourcedata — upstream files from Deep Blue Data (v2, DOI 10.7302/746w-g237)

Re-hosted, unmodified, from the original release
(https://deepblue.lib.umich.edu/data/concern/data_sets/bn999738r):

- `AliceChapterOne-EEG.csv` — 2129-word linguistic annotations (onset/offset, LogFreq,
  IsLexical, Length, SndPower, Position, Sentence, and NGRAM/RNN/CFG surprisal predictors).
- `proc/SXX.mat` — per-subject preprocessing output (FieldTrip). `proc.trl` gives each
  retained word's onset sample; `proc.varnames = [segment, tmin, Order]`. Used to build the
  per-subject `*_events.tsv` (word onset = (start_sample - offset)/500, merged to the CSV on `Order`).
- `easycapM10-acti61_elec.sfp` — easyCAP M10 electrode template positions.
- `comprehension-questions.doc`, `comprehension-scores.txt` — post-listening comprehension task.
- `datasets.mat` — subject index.
