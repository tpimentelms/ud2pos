LANGUAGE := marathi
DATA_DIR := ./data
SCRIPT_DIR := ./ud2pos
CHECKPOINT_DIR := ./checkpoints

UD_DIR_BASE := $(DATA_DIR)/ud

UDURL := https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3226/ud-treebanks-v2.6.tgz

UD_DIR := $(UD_DIR_BASE)/ud-treebanks-v2.6
UD_FILE := $(UD_DIR_BASE)/ud-treebanks-v2.6.tgz

PROCESSED_DIR := $(SCRIPT_DIR)/data/
PROCESSED_FILE := $(PROCESSED_DIR)/$(LANGUAGE)-ud_lemmas.tsv

# TRAIN_DIR := $(CHECKPOINT_DIR)/$(TASK)/$(LANGUAGE)
# TRAIN_MODEL := $(TRAIN_DIR)/$(MODEL)/$(REPRESENTATION)/finished.txt

all: get_ud process
	echo "Finished everything"

process: $(PROCESSED_FILE)

get_ud: $(UD_DIR)

# Preprocess data
$(PROCESSED_FILE):
	echo "Process language in ud " $(LANGUAGE)
	mkdir -p $(PROCESSED_DIR)
	python src/h01_data/process.py --language $(LANGUAGE) --ud-path $(UD_DIR) --output-file $(PROCESSED_FILE)

# Get Universal Dependencies data
$(UD_DIR):
	echo "Get ud data"
	mkdir -p $(UD_DIR_BASE)
	wget -P $(UD_DIR_BASE) $(UDURL)
	tar -xvzf $(UD_FILE) -C $(UD_DIR_BASE)
