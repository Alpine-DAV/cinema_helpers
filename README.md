# cinema_helpers
Helper scripts for connecting cinema databases to viewers.

A Cinema Database provides a parameterized set of assets (files) and associated meta data.

These databases can be created with tools like Ascent, ParaView, and VisIt -- or they can be created with custom scripts.

Learn more about Cinema here:

https://cinemasciencewebsite.readthedocs.io/en/latest/index.html


These helper scripts target Spec D (general CSV) Cinema Spec A (legacy image) specifications.

The viewers here are derived from the main cinema viewers, modified to avoid any XHR security issues.

The scripts are derived from work done with Ascent.


### cinema_cdb_generate_explorer.py

* Given a cinema database, create a stand alone Cinema Explorer to view these files.


###  cinema_cdb_generate_viewer.py

* Given a  cinema database, create a stand alone Spec A viewer for this database.


** Given a cdb (directory) finds Spec A info.json
** Copy Cinema DB files into `_output/cinema_spec_a_viewer_database.cdb`
** Copies spec a viewer html and js to `_output/cinema_spec_a_viewer_resources`
** Creates custom `_output/cinema_spec_a_viewer.html`


### cinema_cdb_spec_a_to_spec_d.py
* Given a SpecA database, convert to a Spec D CSV style database.


