# Overview

Kana is a collection of utilities & libraries I use when working with [Bottle](http://bottlepy.org). It's not meant to be 
complete, but _is_ meant to be relatively straight forward to use.

## Contents

Kana currently includes a few different Bottle helpers, including:

- `kana/middleware`: misc. Middleware libraries for bottle, including a session `before_hook` and a simple Database wrapper.
- `kana/login`: a simple login handler with sane-by-default user model.
- `kana/utils`: misc. utils, such as timestamp generation, config-file flattening, and Jinja view helpers.
- `bin/kanacollectstatic`: a simple script to collect static elements from the various modules a bottle app might have.

# License:

Please see the `LICENSE` file for more details.
