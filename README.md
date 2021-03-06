# ud2pos

[![CircleCI](https://circleci.com/gh/tpimentelms/ud2pos.svg?style=svg&circle-token=d3f2433d9576bb5413356b1ef77c50272d22de8d)](https://circleci.com/gh/tpimentelms/ud2pos)

This code creates a map from wordform to part-of-speech using UD data.

## Using this simple part-of-speech tagger

To use the ud2pos tagger, first install this repository and then instantiate the UdTagger class.

### Install Repository

To install the code in this repository run:
```bash
$ pip install -e .
```

### Use code

To use the ud2pos tagger, add the following to your script:
```python
import ud2pos
language = 'english'
tagger = ud2pos.UdTagger(language)
print('Pos tag is: %s' % tagger('Hi'))
```
This pos tagger will return 'UNK' for words not in the universal dependencies.


## Adding new languages

To process ud data for new languages, run the following commands:

### Install Dependencies

Create a conda environment with
```bash
$ conda env create -f environment.yml
```

### Download and parse universal dependencies (UD) data

You can easily download UD data with the following command
```bash
$ make get_ud
```

You can then get the embeddings for a language with command
```bash
$ make process LANGUAGE=<language>
```
As languages, you should be able to experiment on any in UD. For instance: 'english'; 'czech'; 'basque'; 'finnish'; 'turkish'; 'arabic'; 'japanese'; 'tamil'; 'korean'; 'marathi'; 'urdu'; 'telugu'; 'indonesian'.

## Upload new data to PyPi


Upgrade the repository version in `setup.py`. Then run:
```bash
$ python setup.py sdist
$ twine upload dist/*
```


## Extra Information

#### Contact

To ask questions or report problems, please open an [issue](https://github.com/tpimentelms/ud2pos/issues).
