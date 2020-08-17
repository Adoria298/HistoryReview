# History Review

The History Review categorises different URLs by type and age in your Chrome history and outputs them as a BibTeX list of references. Or it will do.

## Format of Chrome's Database

These are my notes and are mostly pure speculation.

### Tables

The following tables refer to each other and deal with downloads (i.e. downloaded files): **`downloads`** stores information about the downloads themselves, **`downloads_url_chains`** stores where the downloads came from (each download has a list (the column `chain_index` stores the order of the items in said list) of the route Chrome took to get this file) and references the `id` column of `downloads` in its own `id` column to link the tables, **`download_slices`** had no contents at time of writing, but I suspect it would refer to the packets Chrome is receiving are saved temporarily, given the existence of the `received_bytes` column.

The two tables **`segments`** and **`segment_usage`** seem to store information about segments. I do not know what segments are, but the `name` column of **`segment`** corresponds to the sources for downloads, so I suspect they are related.

**`keyword_search_terms`**, according to its contents, lists search terms when you tab to search a site in Chrome. I do not know what the difference between `term` and `normalized_term` is - perhaps it is unicode?

Both **`typed_url_sync_metadata`** and **`meta`** created a `sqlite3.OperationalError` when I tried to access them. I do not know why, and am ignoring this for now. Likewise, I do not what the table **`sqlite_sequence`** is. It seems to only contain one entry: `urls:20312`.

Finally, we reach the tables that contain URLs, and so are relevant to this project. **`urls`** is the most obvious place to start. Its `id` field does not connect to any other table, as far as I can tell. **`visits`** appears to track when these URLs were visited. It refers to each URL by a number, which may be referencing **`visit_source`**. The `visit_time` field of **`visits`** is a very large number - this may be a UNIX timestamp. I cannot see how Chrome correlates the two to form its History page.
