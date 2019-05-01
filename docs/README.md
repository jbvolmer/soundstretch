
# sound stretch 1.2

This uses the Paulstretch algorithm that is released under Public Domain

## install:

```bash
pip3 install soundstretch
```

## usage:

```python
# import soundstretch
from soundstretch import SoundStretch
# use default settings
success = SoundStretch("input.wav","result.wav")
# use specific stretch factor and window size settings
success = SoundStretch("input.wav", "result.wav", 8.0, 0.25)

```

## requirements
- Numpy
- Scipy
