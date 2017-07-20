.. :changelog:

History
-------
0.1.7 (2017-07-20)
++++++++++++++++++
* bugfix summary.summarize_entity_person 


0.1.6 (2017-07-20)
++++++++++++++++++
* add summary.summarize_entity_person function

0.1.5 (2017-07-18)
++++++++++++++++++
* bugfix, normalize_region_name
* pack region data with code

0.1.4 (2017-07-17)
++++++++++++++++++
* add module wikify with wikidata_search, wikidata_get
* update module core with json_dict_copy
* update modele entity with get_primary_entity
* add one more district in region, add strict_mode for skipping exit() on error

0.1.1 (2017-06-22)
++++++++++++++++++
* add module entity with SimpleEntity.ner( text )
* add module region with RegionEntity.guess_all( [address, name])

0.1.0 (2017-06-19)
++++++++++++++++++

* initial PyPI release
* add module json, table(excel), web for data manipulation
* provide cli ui via misc.main_subtask
* connect to travis CI
