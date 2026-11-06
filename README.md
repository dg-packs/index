# dg pack index

`index.json` lists the [dg](https://github.com/nvcnvn/dg) packs that `dg pack add <name>` and
`dg pack search <text>` can find. The index only finds packs: `dg.hcl` keeps the source a name
resolved to, any git URL installs without it, and users get a source's highest `vX.Y.Z` tag, so
the index holds no versions.

## Adding a pack

Open a pull request that adds one line to `packs`, in sorted order by name:

```json
{"name": "network", "source": "git.example.com/acme/network", "description": "Routers, switches and firewalls", "license": "Apache-2.0"}
```

- `name` is what users type. It is the source's last segment, which becomes the pack's local name
  and the prefix of its kinds, so a pack does not repeat it in its kind names.
- `source` is `<host>/<path>`, or an `https://` or `ssh://` URL, with no version. It ends with
  `//<dir>` only if the repository is a monorepo; `name` is then the last segment of `<dir>`.
- `description` says in one line what the pack draws. `dg pack search` shows it and matches it.
- `license` is the pack's SPDX identifier, or `see NOTICE` when its art has terms of its own.

Run `python3 check.py` before you open the request. It needs only Python 3, and the same check
runs on the request.

## The bar

A pack is listed when its repository has:

- a tag `vX.Y.Z`. A branch cannot be installed, since it moves.
- a `LICENSE` at its root, giving the terms of the pack.
- a `NOTICE` at its root when any art in it is someone else's, with that art's source and terms.
  Publish the art only if those terms allow it; if they do not, ship the kinds and styles without
  it.
- a `spec.hcl`, a `style.hcl` or both that pass `dg check` once installed with `dg pack add`.

A pack is data, and dg runs nothing in it. Listing a pack says nothing more than that it met this
bar: read a pack's license before you use it.

## Writing a pack

See [the guide](https://github.com/nvcnvn/dg/blob/main/docs/packs.md).
