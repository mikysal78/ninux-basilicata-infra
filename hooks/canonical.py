"""Canonical delle pagine italiane verso la copia su WordPress.

Le stesse pagine sono pubblicate anche su ninux-nnxx.it/guida/ (ruolo guida di
WP-ninux-nnxx.it): senza questo Google vede due copie e sceglie lui quale
mostrare. Le pagine inglesi esistono solo qui e tengono il loro canonical.
"""

import re
from pathlib import PurePosixPath


def on_post_page(output, page, config):
    base = config["extra"].get("canonical_wordpress")
    if not base or page.url.startswith("en/"):
        return output
    nome = PurePosixPath(page.file.src_uri).stem
    url = base if nome == "index" else f"{base}{nome}/"
    return re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', output, count=1)
