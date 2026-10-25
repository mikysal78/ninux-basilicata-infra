# ninux-basilicata-infra

🇮🇹 La guida passo passo per ricostruire l'infrastruttura di **NINUX Basilicata**:
Proxmox, DNS, OpenWISP, i moduli per OpenWISP, il firmware OpenWrt con Jenkins
e l'app Android. **👉 https://mikysal78.github.io/ninux-basilicata-infra/**

🇬🇧 Step-by-step guide to rebuild the **NINUX Basilicata** infrastructure:
Proxmox, DNS, OpenWISP, the OpenWISP modules, the OpenWrt firmware with Jenkins
and the Android app. **👉 https://mikysal78.github.io/ninux-basilicata-infra/en/**

## Sviluppo / Development

Il sito è fatto con [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
e pubblicato su GitHub Pages da GitHub Actions a ogni push su `main`. Le pagine
sono in `docs/`: `pagina.md` in italiano, `pagina.en.md` in inglese.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000
mkdocs build --strict   # come la CI
```

Contatti / Contact: [app@ninux-nnxx.it](mailto:app@ninux-nnxx.it)

## Licenza / License

Testi: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
I componenti descritti hanno le loro licenze, nei rispettivi repository.
