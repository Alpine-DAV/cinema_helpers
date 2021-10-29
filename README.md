# cinema_helpers
Helper scripts for connecting cinema databases to viewers.

A cinema database provides a parameterized set of assets (files) and associated meta data.

These databases can be created with tools like Ascent, ParaView, and VisIt -- or they can be created with custom scripts.

Learn more about Cinema here:

https://cinemasciencewebsite.readthedocs.io/en/latest/index.html


These helper scripts target Spec D (general CSV) and Cinema Spec A (legacy image) specifications.

The viewers here are derived from the main cinema viewers, modified to avoid any XHR security issues.

The scripts are derived from work done with Ascent.


### cinema_cdb_generate_explorer.py

Given a cinema database, create a stand alone Cinema Explorer to view these files.

```
python cinema_cdb_generate_explorer.py  example_databases/uncertainty_bubbles.cdb _out_explore_bubbles
open _out_explore_bubbles/cinema_explorer/index.html
````

###  cinema_cdb_generate_viewer.py

Given a spec a cinema database, create a stand alone spec a viewer for this database.

```
python cinema_cdb_generate_spec_a_viewer.py example_databases/visit_ex_spec_a.cdb/ _out_spec_a_visit 
open _out_spec_a_visit/cinema_spec_a_viewer/index.html 
````

### cinema_cdb_spec_a_to_spec_d.py
Given a SpecA database, convert to a Spec D CSV style database.

```
python cinema_cdb_convert_spec_a_to_spec_d.py   example_databases/visit_ex_spec_a.cdb/ _convert/visit_ex.cdb
python cinema_cdb_generate_explorer.py  _convert/visit_ex.cdb _out_explore_converted
open _out_explore_converted/cinema_explorer/index.html 
```


