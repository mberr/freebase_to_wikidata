# freebase_to_wikidata
This repository offers translation between [FB15k-237](https://www.microsoft.com/en-us/download/details.aspx?id=52312) IDs to [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) IDs and labels.

## How to create the translation table
* Download [FB15k-237](https://www.microsoft.com/en-us/download/details.aspx?id=52312)
* Create a list of all requested entities using
```bash
unzip -p FB15K-237.2.zip Release/{train,valid,test}.txt | \
dos2unix | awk '{print $1"\n"$2"\n"$3}' | sort | uniq > freebase_ids.csv
```
* Create a file for mapping Wikidata ID <-> Freebase ID and Wikidata ID <-> English label
```bash
wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.bz2 \
-O - | lbzcat -v -n 8 | grep -E "direct/P646|schema.org/name> .*@en \." | tee \
>(grep "direct/P646" | cut -d" " -f1,3- | sed 's/ \.//g' > wikidata.to.freebase.tsv)\
>(grep "<http://schema.org/name>" | cut -d" " -f1,3- | sed 's/@en \.//g' > wikidata.to.label.tsv) \
> /dev/null
``` 
* Run `create_mapping.py` to create JSON file `translation.json`. You can use `--data_root` to specify the directory of the preprocessed files from the previous steps, and `--output_root` to change the output directory (both default to the current working directory).  
```bash
python3 create_mapping.py --data_root=. --output_root=.
```
