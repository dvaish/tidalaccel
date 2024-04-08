# Contents

- `gemmini-rocc-tests` contains the benchmarks to be run
- `tidalsim` contains the existing TidalSim scripts
- `gemmini_extraction.py` parses the Spike trace looking for Gemmini instructions

# Setup

You must generate the Spike trace in order to get the committed instructions. 

```
spike -l --extension=gemmini gemmini-rocc-tests/build/mlps/lab2_mlp_baseline-baremetal 2> log.log
```

# Running the script

```
python -i gemmini_extraction.py
```